# RSLED
This is a Home Assistant integration for controlling [Red Sea ReefLED lights](https://g1.redseafish.com/hardware/lighting/).

## introduction
Each RSLED unit includes a 23,000 Kelvin "REEF-SPEC" blue light, a 9,000 Kelvin white light, and a moon light.


## finding the endpoints
I configured a mitmproxy/mitmdump on a docker container and pointed my iphone at it. My docker-compose file:

```
services:
  mitmweb:
    image: mitmproxy/mitmproxy
    tty: true
    ports:
      - 8080:8080
      - 8081:8081
    command: mitmweb --web-host 0.0.0.0
    restart: always

  mitmdump:
    image: mitmproxy/mitmproxy
    command: mitmdump -nC /home/mitmproxy/flows
    volumes:
      - ./mitmproxy:/home/mitmproxy/
    restart: always
```

Once the proxy is up and running (I followed these directions at https://blog.sayan.page/mitm-proxy-on-ios/):

* Settings > WiFi and then tap on the (i) icon beside the network your are connected to.

* Scroll down to the bottom and tap on “Configure Proxy”.

* Select Manual, put the proxy server IP and port ("yourproxyhost:8080"), and save.

* Open Safari on the iOS device and open [mitm.it](https://mitm.it). Choose the CA certificates for your phone and follow the directions.

* In settings, a "downloaded profiles" option appears at the root level. Click into the option and install the profile.

* Go to Settings > General > About and scroll down to the bottom of the page. You will see a menu item titled “Certificate Trust Settings”. Tap on it and enable the certificate for "mitmproxy" in the following page.

* Open the proxy service site at http://yourproxyhost:8081, you'll see the UI.

* Open the Red Sea app, and proceed into the app to the Manual settings...

## documenting the endpoints

For my RSLED90 lights, I observed the following command endpoints through proxy using the manual setting in the app (when you send the given payload in the POST body):

### MANUAL
This sets the lights to the requested color. The lights stay that color until the mode call is issued. It returns the same structure with two additional values: fan and temperature - but does not seem to respond to trying to set either of them (i.e. you can't turn the fan on and off). The light color parameters are a value between 0 and 100.
```
manual : {
    "blue": 100,
    "moon": 0,
    "white": 100
}
```

### MODE
This restores the light to the automatic mode configured in the app. I did not try to chase down all of the ways to set a program, but there are endpoints for getting and setting them if you want to do that. It returns the current mode (auto, timer, or manual - in my limited testing).
```
mode : {
    mode: auto
}
```

### TIMER
This sets the light colors for the requested duration in minutes. It also returns a structure with the timer status and time remaining.
```
timer: {
    "blue": 100,
    "duration": 30,
    "moon": 0,
    "white": 100
}
```

### OTHER
I also saw two other endpoints, which might respond to commands:
```
moonphase
acclimation
```

## plan
For my purposes, I really only want the MANUAL and MODE endpoints for this integration. The plan is to create three entities for each of the lights that have brightness values, and include a service call to set the effective color temperature and brightness using the blue and white lights. I'll also build up a "photo mode", which is probably just setting a full white light for some time period. I also plan to mimic the moon phase on the third LED (probably using something from HA to get the actual moon phase).

Of note, the Red Sea website says their research suggests you basically want a 12-hour on and 12-hour off cycle, and the moon phase is included in that (though I admit to giving that some side-eye).

## testing the lights manually

Example curl commands (replace xx.xx.xx.xx with the IP address of your light):

```
curl -i -X POST -H 'Content-Type: application/json' -d '{"white": 100, "blue":50, "moon": 0 }' http://xx.xx.xx.xx/manual
curl -i -X POST -H 'Content-Type: application/json' -d '{"mode": "auto" }' http://xx.xx.xx.xx/mode
curl -i -X POST -H 'Content-Type: application/json' -d '{"white": 100, "blue":50, "moon": 0, "duration": 1 }' http://xx.xx.xx.xx/timer
```

## zeroconf
RSLED lights show up in zeroconf queries like so:
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

## disclaimer
This is integration is not supported by or affiliated with Red Sea.
