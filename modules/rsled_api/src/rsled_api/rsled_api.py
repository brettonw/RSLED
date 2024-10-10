import requests
from typing import Any
from .const import *
from .interpolate import interpolate, XYPair
from .utility import clamp

color_tables = {
    "RSLED50": [
        XYPair(9000, [0, 100]),
        XYPair(12000, [100, 100]),
        XYPair(15000, [100, 50]),
        XYPair(20000, [100, 25]),
        XYPair(23000, [100, 5]),
    ],
    "RSLED90": [
        XYPair(9000, [0, 100]),
        XYPair(12000, [75, 100]),
        XYPair(15000, [100, 100]),
        XYPair(20000, [100, 50]),
        XYPair(23000, [100, 10]),
    ],
    "RSLED160S": [
        XYPair(9000, [0, 100]),
        XYPair(12000, [80, 100]),
        XYPair(15000, [100, 100]),
        XYPair(20000, [100, 50]),
        XYPair(23000, [100, 10]),
    ]
}


class RsLedApi:
    def __init__(self, host: str) -> None:
        self.host: str = host

        # declare the state dictionary and update it
        self._state: dict[str, Any] = {}
        device_info = self._get_endpoint("device-info")
        if device_info is not None:
            self._state[HW_MODEL] = device_info[HW_MODEL]
        self.update()

    def _get_endpoint(self, endpoint: str) -> dict[str, Any] | None:
        try:
            r = requests.get(f"http://{self.host}/{endpoint}", timeout=10)
            if r.status_code == 200:
                return r.json()
        except requests.exceptions.ConnectTimeout:
            pass
        return None

    def update(self):
        manual = self._get_endpoint(MANUAL)
        if manual is not None:
            self._state.update(manual)
        auto = self._get_endpoint(AUTO)
        if auto is not None:
            self._state.update(auto)

    def _set_endpoint(self, endpoint: str, post: dict[str, Any]) -> dict[str, Any] | None:
        try:
            r = requests.post(f"http://{self.host}/{endpoint}", json=post, timeout=10)
            if r.status_code == 200:
                return r.json()
        except requests.exceptions.ConnectTimeout:
            pass
        return None

    def _set_state_values(self, values: dict[str, Any], endpoint: str):
        state = self._state.copy()
        state.update(values)
        result = self._set_endpoint(endpoint, state)
        if result is not None:
            self._state.update(result)

    @property
    def hw_model(self) -> str:
        return self._state[HW_MODEL]

    @property
    def blue(self) -> int:
        return self._state[BLUE]

    def set_blue(self, blue: int):
        self._set_state_values({BLUE: blue}, MANUAL)

    @property
    def white(self) -> int:
        return self._state[WHITE]

    def set_white(self, white: int):
        self._set_state_values({WHITE: white}, MANUAL)

    @property
    def moon(self) -> int:
        return self._state[MOON]

    def set_moon(self, moon: int):
        self._set_state_values({MOON: moon}, MANUAL)

    @property
    def mode(self) -> int:
        return self._state[MODE]

    def reset_mode(self):
        self._set_state_values({MODE: AUTO}, MODE)

    def set_blue_white(self, blue: int, white: int):
        self._set_state_values({BLUE: blue, WHITE: white}, MANUAL)

    def set_max(self):
        self._set_state_values({BLUE: 100, WHITE: 100}, MANUAL)

    def set_min(self):
        self._set_state_values({BLUE: 0, WHITE: 0}, MANUAL)

    def set_off(self):
        self._set_state_values({BLUE: 0, WHITE: 0, MOON: 0}, MANUAL)

    @property
    def brightness(self) -> int:
        # the brightest of blue and white is the current brightness
        return max(self.blue, self.white)

    def _normalized_bw(self, brightness: int = 100) -> list[int]:
        # normalizes the blue/white components to the target brightness. valid brightness and blue/
        # white values are [0..100], so the scale is performed in integer space (just leave the
        # parenthesis where they are to ensure order of operation)
        return [int(((x * brightness) / self.brightness) + 0.5) for x in [self.blue, self.white]]

    def set_brightness(self, brightness: int):
        # set the blue/white components to the requested brightness setting
        y = self._normalized_bw(brightness)
        self._set_state_values({BLUE: y[0], WHITE: y[1]}, MANUAL)

    def normalize(self):
        # set the blue/white components to the brightest possible setting that maintains the color
        y = self._normalized_bw()
        self._set_state_values({BLUE: y[0], WHITE: y[1]}, MANUAL)

    @property
    def color_temperature(self) -> int:
        # compute a normalized color, so one of the blue or white values is saturated
        max_value = max(self.blue, self.white)
        scale = 100.0 / max_value
        y = [int((self.blue * scale) + 0.5), int((self.white * scale) + 0.5)]

        # search the color tables for the best match in blue and white, whichever is more precise
        if y[0] == 100:
            if y[1] == 100:
                # find the inflection point
                pass
            else:
                # search on y[1] for the most precise lookup
                pass
        else:  # y[1] == 100
            assert y[1] == 100
            # search on y[0] for the most precise lookup

        # nyi
        return 0

    def set_color_temperature(self, color_temperature: int, brightness: int) -> None:
        color_table = color_tables[self.hw_model]
        interpolated = interpolate(color_table, color_temperature)
        y = [int(clamp((y * brightness) / 100, 0, 100) + 0.5) for y in interpolated]
        self._set_state_values({BLUE: y[0], WHITE: y[1]}, MANUAL)
