import logging
import pychromecast
import zeroconf
import time
import threading

logging.basicConfig(format="%(asctime)s: %(message)s", datefmt="%m/%d/%Y %H:%M:%S", level=logging.DEBUG)

"""
For metadata, see:
    https://developers.google.com/cast/docs/reference/messages#MediaData

"""
def get_cast(name):
    cast = None
    event = threading.Event()
    def callback(chromecast):
        #print(chromecast)
        #chromecast.connect()
        #print(chromecast)
        if chromecast.device.friendly_name == name:
            #chromecast.connect()
            nonlocal cast
            cast = chromecast
            event.set()
    event.clear()
    browser = pychromecast.get_chromecasts(blocking=False, callback=callback)
    event.wait(2) # if not found within 2 secs, it's not there!
    pychromecast.stop_discovery(browser)
    return cast

def print_casts(casts):
    for cast in casts:
        print(cast.device.friendly_name,"\t", cast.cast_type)

def print_cast(cast):
    cast.start()
    print()
    print(cast.device)
    time.sleep(1)
    print()
    print(cast.status)
    print()
    print(cast.media_controller.status)
    print()

def kill_cast(cast):
    if not cast.is_idle:
        print("Killing current running app")
        cast.quit_app()

def play_cast(cast, media, mimetype):
    print("Playing media", media)
    cast.play_media(media, mimetype)
    print("Media status", cast.media_controller.status)

def pause_cast(cast):
    print("Sending pause command")
    cast.media_controller.pause()

def resume_cast(cast):
    print("Sending play command")
    cast.media_controller.play()

def stop_cast(cast):
    print("Sending stop command")
    cast.media_controller.stop()

def get_hosts():
    # discover_chromecasts() waits for a timeout to gather cast hosts, but then closes the zeroconf Service,
    # which unfortunately adds delay.
    return pychromecast.discover_chromecasts(timeout=3)

def get_host(name):
    return next(filter(lambda h: h[4] == name, get_hosts()))

def test1():
    # Discover AND gather status from each cast device (requires connection):
    casts, browser = pychromecast.get_chromecasts()
    print_casts(casts)
    pychromecast.stop_discovery(browser)

    global cast
    #cast = get_cast("Kitchen and Deck")
    cast = get_cast("Kitchen")
    cast.connect()
    cast.set_volume(0.2)
    print(cast)

def test2():
    # Discover without connecting (and give it only 2 secs):
    services, browser = pychromecast.discover_chromecasts(timeout=2)
    model_order = {
        "BRAVIA 4K UR2": 6,
        "Chromecast": 5,
        "Chromecast Audio": 1,
        "Google Cast Group": 10,
        "SmartCast Speaker 50-D5": 1
    }

    services.sort(key=lambda c: (model_order.get(c[2], 5), c[3]))

    for service in services:
        svcs, uuid, model_name, friendly_name, ip, port = service
        print(model_name, friendly_name, ip, port)

    name = "Kitchen"
    cast = None
    for service in services:
        svcs, uuid, model_name, friendly_name, ip, port = service
        if friendly_name == name:
            cast = pychromecast.get_chromecast_from_service(service, browser.zc)
            break
    print(cast)

    # # No worker thread:
    # print("Threads before connecting:", list(threading.enumerate()))
    # cast.connect()
    # print(cast.status)
    # print(cast.status.volume_level)
    # cast.disconnect()
    # print("Threads after disconnecting:", list(threading.enumerate()))

    cast.wait()
    print(cast.status)
    print(cast.status.volume_level)

    pychromecast.stop_discovery(browser)

def test3():
    # def callback(uuid, name):
    #     print(uuid, name)
    listener = pychromecast.CastListener()
    browser = pychromecast.start_discovery(listener, zeroconf.Zeroconf())
    time.sleep(2)
    pychromecast.stop_discovery(browser)
    devices = listener.devices
    print(devices)
    devices.sort(key=lambda d: (d[2] == "Google Cast Group", d[3]))
    print(",".join(map(lambda d: d[3], devices)))
    print(next(filter(lambda d: d[3] == "Kitchen", devices)))

if __name__ == "__main__":
    test3()
