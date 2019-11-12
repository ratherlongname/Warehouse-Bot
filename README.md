# Warehouse-Bot

## Setup
1. Flash [Raspbian Buster](https://www.raspberrypi.org/downloads/raspbian/) on SD card following instructions [here](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)

2. Get Wifi working following instructions [here](https://www.electronicshub.org/setup-wifi-raspberry-pi-2-using-usb-dongle/)

3. Install OpenCV by following instructions [here](https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/)

4. For using qr code, install pyzbar from deps folder
```
sudo apt install libzbar0 # linux only

pip3 install --user pyzbar-0.1.8-py2.py3-none-any.whl # linux/macos
pip3 install --user pyzbar-0.1.8-py2.py3-none-win_amd64.whl # windows 64 bit
pip3 install --user pyzbar-0.1.8-py2.py3-none-win32.whl # windows 32 bit

```
## TODO

-[] Block nodes.