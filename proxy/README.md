# Proxy

## finding the endpoints
I configured a web proxy using mitmproxy/mitmdump on a docker container and pointed my iPhone at it. See the `proxy/docker-compose.yml` file for details of the proxy deployment.

Once the proxy was up and running, I followed the directions at https://blog.sayan.page/mitm-proxy-on-ios/, which I summarize here:

* Select Settings -> WiFi and then tap on the (i) icon beside the network you are connected to.

* Scroll down to the bottom and tap on “Configure Proxy”.

* Select Manual, enter the proxy server IP and port ("yourproxyhost:8080"), and save.

* Use Safari on the iPhone and open [mitm.it](https://mitm.it). Choose the CA certificates for your phone and follow the directions.

* In iPhone settings, a "downloaded profiles" option appears at the root level. Click into the option and install the profile.

* Go to Settings -> General -> About and scroll down to the bottom of the page. You will see a menu item titled “Certificate Trust Settings”. Tap on it and enable the certificate for "mitmproxy" in the following page.

* On a computer, open the proxy service site at http://yourproxyhost:8081, you'll see the UI showing requests.

* Open the Red Sea app, and proceed into the app to the Manual settings...
