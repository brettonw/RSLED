import requests_mock

from unittest import TestCase
from rsled_api import RsLedApi
from rsled_api.const import *

MOCKHOST = "mockhost"
RSLED90 = "RSLED90"
MANUAL_SUCCESS = {"success":True, "message":"manual mode enabled successfully"}
MANUAL_FAILURE = {"success":False, "message":"whatever"}
MANUAL_AUTO = {BLUE: 15, "blue_pwm": 43*15, WHITE: 5, "white_pwm": 43*5, MOON: 10, "moon_pwm": 43*10, "fan": 15, "temperature": 85.6}


class TestRsledApi(TestCase):
    def test_rsled_api(self):
        with requests_mock.Mocker() as mock:
            # get through the initialization of the api
            mock.get(f"http://{MOCKHOST}/{DEVICE_INFO}", json={HW_MODEL: RSLED90})
            mock.get(f"http://{MOCKHOST}/{MANUAL}", json=MANUAL_AUTO)
            mock.get(f"http://{MOCKHOST}/{MODE}", json={MODE: AUTO})
            api = RsLedApi(MOCKHOST)
            assert api.blue == 15
            assert api.white == 5
            assert api.moon == 10
            assert api.mode == AUTO
            assert api.hw_model == RSLED90

            # set blue
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_blue(100)
            assert api.blue == 100
            assert api.white == 5
            assert api.moon == 10
            assert api.mode == MANUAL
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 100, WHITE: 5, MOON: 10}

            # do a reset
            RESET_MODE = {MODE: AUTO}
            mock.post(f"http://{MOCKHOST}/{MODE}", status_code=202, json=RESET_MODE)
            mock.get(f"http://{MOCKHOST}/{MANUAL}", json=MANUAL_AUTO)
            api.reset_mode()
            assert api.mode == AUTO
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "GET"

            # set a color temperature
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_color_temperature(15000, 100)
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 100, WHITE: 100, MOON: 10}
            assert api.blue == 100
            assert api.white == 100
            assert api.moon == 10
            assert api.mode == MANUAL

            # set a color temperature
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_color_temperature(8000, 100)
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 0, WHITE: 100, MOON: 10}
            assert api.blue == 0
            assert api.white == 100
            assert api.moon == 10
            assert api.mode == MANUAL

            # set a color temperature
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_color_temperature(25000, 100)
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 100, WHITE: 0, MOON: 10}
            assert api.blue == 100
            assert api.white == 0
            assert api.moon == 10
            assert api.mode == MANUAL

            # set a color temperature with lower brightness
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_color_temperature(15000, 50)
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 50, WHITE: 50, MOON: 10}
            assert api.blue == 50
            assert api.white == 50
            assert api.moon == 10
            assert api.mode == MANUAL

            # change the brightness
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_brightness(75)
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 75, WHITE: 75, MOON: 10}
            assert api.blue == 75
            assert api.white == 75
            assert api.moon == 10
            assert api.mode == MANUAL

            # change the brightness
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_brightness(25)
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 25, WHITE: 25, MOON: 10}
            assert api.blue == 25
            assert api.white == 25
            assert api.moon == 10
            assert api.mode == MANUAL

            # do a manual post
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_blue(50)
            assert api.blue == 50
            assert api.white == 25
            assert api.moon == 10
            assert api.mode == MANUAL
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 50, WHITE: 25, MOON: 10}

            # change the brightness
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_brightness(100)
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 100, WHITE: 50, MOON: 10}
            assert api.blue == 100
            assert api.white == 50
            assert api.moon == 10
            assert api.mode == MANUAL

            # white
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_white(100)
            assert api.blue == 100
            assert api.white == 100
            assert api.moon == 10
            assert api.mode == MANUAL
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 100, WHITE: 100, MOON: 10}

            # blue_white
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_blue_white(20, 20)
            assert api.blue == 20
            assert api.white == 20
            assert api.moon == 10
            assert api.mode == MANUAL
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 20, WHITE: 20, MOON: 10}

            # min
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_min()
            assert api.blue == 0
            assert api.white == 0
            assert api.moon == 10
            assert api.mode == MANUAL
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 0, WHITE: 0, MOON: 10}

            # max
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_max()
            assert api.blue == 100
            assert api.white == 100
            assert api.moon == 10
            assert api.mode == MANUAL
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 100, WHITE: 100, MOON: 10}

            # off
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_off()
            assert api.blue == 0
            assert api.white == 0
            assert api.moon == 0
            assert api.mode == MANUAL
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 0, WHITE: 0, MOON: 0}

            # moon
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_moon(30)
            assert api.blue == 0
            assert api.white == 0
            assert api.moon == 30
            assert api.mode == MANUAL
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 0, WHITE: 0, MOON: 30}

            # normalized
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_color_temperature(20000, 50)
            assert api.blue == 50
            assert api.white == 25
            assert api.moon == 30
            assert api.mode == MANUAL
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 50, WHITE: 25, MOON: 30}
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.normalize()
            assert api.blue == 100
            assert api.white == 50
            assert api.moon == 30
            assert api.mode == MANUAL
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 100, WHITE: 50, MOON: 30}

            # test error conditions for get
            mock.get(f"http://{MOCKHOST}/{MANUAL}", status_code=500, json={"blah": "blah"})
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=500, json=MANUAL_FAILURE)
            mock.get(f"http://{MOCKHOST}/{MODE}", status_code=500, json={"blah": "blah"})
            api.update()
            assert api.blue == 100
            assert api.white == 50
            assert api.moon == 30
            assert api.mode == MANUAL
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "GET"

            # test error conditions for post
            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=500, json=MANUAL_FAILURE)
            api.set_blue(50)
            assert api.blue == 100
            assert api.white == 50
            assert api.moon == 30
            assert api.mode == MANUAL
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 50, WHITE: 50, MOON: 30}


            # test error conditions for init
            mock.get(f"http://{MOCKHOST}/{DEVICE_INFO}", status_code=500, json={"blah": "blah"})
            mock.get(f"http://{MOCKHOST}/{MANUAL}", status_code=500, json={"blah": "blah"})
            mock.get(f"http://{MOCKHOST}/{MODE}", status_code=500, json={"blah": "blah"})
            api = RsLedApi(MOCKHOST)
            assert api.blue == 100
            assert api.white == 50
            assert api.moon == 30
            assert api.mode == MANUAL
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 50, WHITE: 50, MOON: 30}
