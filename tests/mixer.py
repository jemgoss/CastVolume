import logging
import pychromecast
import zeroconf
import time
import threading

#logging.basicConfig(format="%(asctime)s: %(message)s", datefmt="%m/%d/%Y %H:%M:%S", level=logging.DEBUG)
logging.basicConfig(format="%(asctime)s: %(message)s", datefmt="%m/%d/%Y %H:%M:%S", level=logging.INFO)

def mixer(name):
    global device, cast
    devices, browser = pychromecast.discover_chromecasts(timeout=5)
    print("Speakers:")
    print("---------")
    for d in filter(lambda d: d.cast_type == None, devices):
        #print(d.friendly_name, d.cast_type, d.model_name, d.manufacturer, d.host, d.port)
        model = d.model_name
        if d.manufacturer:
            model = model + f" ({d.manufacturer})"
        print(f"{d.friendly_name:30}{model:35}{d.host}:{d.port}")
    print()
    print("Groups:")
    print("-------")
    for d in filter(lambda d: d.cast_type == "group", devices):
        model = d.model_name
        if d.manufacturer:
            model = model + f" ({d.manufacturer})"
        print(f"{d.friendly_name:30}{model:35}{d.host}:{d.port}")

    #device = next(filter(lambda c: c.friendly_name == name, devices))

    #cast = pychromecast.get_chromecast_from_cast_info(device, browser.zc)

    #cast.wait()

    #browser.stop_discovery()

if __name__ == "__main__":
    mixer("Indoor")
