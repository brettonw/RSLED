import requests_mock

from unittest import TestCase
from rsled_api import RsLedApi
from rsled_api.const import *

MOCKHOST = "mockhost"
RSLED90 = "RSLED90"
MANUAL_SUCCESS = {"success":True, "message":"manual mode enabled successfully"}


class TestRsledApi(TestCase):
    def test_rsled_api(self):
        with requests_mock.Mocker() as mock:
            # get through the initialization of the api
            mock.get(f"http://{MOCKHOST}/{DEVICE_INFO}", json={HW_MODEL: RSLED90})
            mock.get(f"http://{MOCKHOST}/{MANUAL}", json={BLUE: 15, "blue_pwm": 43*15, WHITE: 5, "white_pwm": 43*5, MOON: 10, "moon_pwm": 43*10, "fan": 15, "temperature": 85.6})
            mock.get(f"http://{MOCKHOST}/{MODE}", json={MODE: AUTO})
            api = RsLedApi(MOCKHOST)
            assert api.blue == 15
            assert api.white == 5
            assert api.moon == 10
            assert api.mode == AUTO
            assert api.hw_model == RSLED90

            mock.post(f"http://{MOCKHOST}/{MANUAL}", status_code=202, json=MANUAL_SUCCESS)
            api.set_blue(100)
            assert api.blue == 100
            assert api.white == 5
            assert api.mode == MANUAL
            assert mock.called
            last_request = mock.last_request
            assert last_request.method == "POST"
            assert last_request.json() == {BLUE: 100, WHITE: 5, MOON: 10}

            # keep going...
