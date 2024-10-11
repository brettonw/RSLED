import requests
from typing import Any
from .const import *
from .interpolate import interpolate, XYPair
from .utility import clamp

# the different models have slightly different balance between the white and blue leds, so we just
# use the tables Red Sea published on their website for the different color temperatures
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

# when posting messages to the different APIs, the lights are sensitive to extraneous fields. we use
# these lists to dictate what fields are included in the posted request data.
fields_mask = {
    MANUAL: {BLUE, WHITE, MOON},
    MODE: {MODE}
}


class RsLedApi:
    def __init__(self, host: str) -> None:
        self.host: str = host

        # declare the state dictionary and update it
        self._state: dict[str, Any] = {}
        device_info = self._get_endpoint(DEVICE_INFO)
        if device_info is not None:
            self._state[HW_MODEL] = device_info[HW_MODEL]
        self.update()

    def _get_endpoint(self, endpoint: str) -> dict[str, Any] | None:
        try:
            r = requests.get(f"http://{self.host}/{endpoint}")
            # we take any "successful" response code in the range 200-299
            status_code = int(r.status_code / 100)
            if status_code == 2:
                return r.json()
            print(f"_get_endpoint failure: {status_code} {r.text}")
        except requests.exceptions.ConnectTimeout:
            pass
        return None

    def _update_state(self, endpoint: str) -> None:
        result = self._get_endpoint(endpoint)
        if result is not None:
            self._state.update(result)

    def update(self):
        self._update_state(MANUAL)
        self._update_state(MODE)

    def _set_endpoint(self, endpoint: str, post: dict[str, Any]) -> dict[str, Any] | None:
        try:
            r = requests.post(f"http://{self.host}/{endpoint}", json=post)
            # we take any "successful" response code in the range 200-299
            status_code = int(r.status_code / 100)
            if status_code == 2:
                return r.json()
            print(f"_set_endpoint failure: {status_code} {r.text} on {post}")
        except requests.exceptions.ConnectTimeout:
            pass
        return None

    def _set_state_values(self, values: dict[str, Any], endpoint: str, success_field: str, success_value: Any) -> bool:
        state = {k: v for k, v in self._state.items() if k in fields_mask[endpoint]}
        state.update(values)
        result = self._set_endpoint(endpoint, state)
        if (result is not None) and (result[success_field] == success_value):
            self._state.update(state)
            return True
        else:
            print(f"  failure, result: {result}")
            return False

    def _set_state_values_manual(self, values: dict[str, Any]) -> None:
        # in addition to setting the values, requested, a successful call should set the mode to
        # MANUAL - this saves us having to update() from the device
        if self._set_state_values(values, MANUAL, SUCCESS, True):
            self._state[MODE] = MANUAL

    @property
    def hw_model(self) -> str:
        return self._state[HW_MODEL]

    @property
    def blue(self) -> int:
        return self._state[BLUE]

    def set_blue(self, blue: int):
        self._set_state_values_manual({BLUE: blue})

    @property
    def white(self) -> int:
        return self._state[WHITE]

    def set_white(self, white: int):
        self._set_state_values_manual({WHITE: white})

    @property
    def moon(self) -> int:
        return self._state[MOON]

    def set_moon(self, moon: int):
        self._set_state_values_manual({MOON: moon})

    @property
    def mode(self) -> int:
        return self._state[MODE]

    def reset_mode(self):
        self._set_state_values({MODE: AUTO}, MODE, MODE, AUTO)
        self._update_state(MANUAL)

    def set_blue_white(self, blue: int, white: int):
        self._set_state_values_manual({BLUE: blue, WHITE: white})

    def set_max(self):
        self._set_state_values_manual({BLUE: 100, WHITE: 100})

    def set_min(self):
        self._set_state_values_manual({BLUE: 0, WHITE: 0})

    def set_off(self):
        self._set_state_values_manual({BLUE: 0, WHITE: 0, MOON: 0})

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
        self._set_state_values_manual({BLUE: y[0], WHITE: y[1]})

    def normalize(self):
        # set the blue/white components to the brightest possible setting that maintains the color
        y = self._normalized_bw()
        self._set_state_values_manual({BLUE: y[0], WHITE: y[1]})

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
        # set the color temperature in the range of the lights
        color_table = color_tables[self.hw_model]
        interpolated = interpolate(color_table, color_temperature)
        y = [int(clamp((y * brightness) / 100, 0, 100) + 0.5) for y in interpolated]
        self._set_state_values_manual({BLUE: y[0], WHITE: y[1]})
