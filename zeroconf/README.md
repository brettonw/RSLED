# zeroconf

## lights
ReefLED lights show up in zeroconf queries like so:
```
add (RSLED90-xxxxxx)
  address: xx.xx.xx.xx
  host: rsled90-xxxxxx
  properties:
    hwid: xxxxxxxxxx
    firmware_version: 2.1.1
    hw_model: RSLED90
    hw_type: reef-lights
```
The "hw_model" field is a reliable indicator of the device type, and the "hwid" field seems to be a unique identifier that can be used for autodiscovery within Home Assistant.

## browser
This is a simple python tool to browse zeroconf entities on your network and print out the details for ReefLED lights.

```
browser.py
```
