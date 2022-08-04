import logging
import pychromecast
import zeroconf
import time

logging.basicConfig(format="%(asctime)s: %(message)s", datefmt="%m/%d/%Y %H:%M:%S", level=logging.DEBUG)

"""
For metadata, see:
    https://developers.google.com/cast/docs/reference/messages#MediaData

"""
class MyStatusListener():
    """Listener for receiving cast status events."""
    def new_cast_status(self, status):
        """Updated cast status."""
        print(f"volume level: {status.volume_level * 100}%")

def get_cast(browser, name):
    device = next(filter(lambda d: d.friendly_name == name, browser.devices.values()))
    cast = pychromecast.get_chromecast_from_cast_info(device, browser.zc)
    cast.wait()
    return cast

def test():
    browser = pychromecast.CastBrowser(pychromecast.SimpleCastListener(), zeroconf.Zeroconf())
    browser.start_discovery()
    time.sleep(2)
    #browser.stop_discovery()

    devnames = list(map(lambda d: d.friendly_name, browser.devices.values()))
    print("\nDevice names:\n", devnames)

    cast = get_cast(browser, "Kitchen")
    print(f"Cast volume level: {cast.status.volume_level * 100}%")
    print(f"Cast type: {cast.cast_info.cast_type}")
    print(f"Manufacturer: {cast.cast_info.manufacturer}")

    cast2 = get_cast(browser, "DiningRoom")
    print(f"Cast volume level: {cast2.status.volume_level * 100}%")
    print(f"Cast type: {cast2.cast_info.cast_type}")
    print(f"Manufacturer: {cast2.cast_info.manufacturer}")

    # listen for status changes:
    cast.register_status_listener(MyStatusListener())
    time.sleep(10)

    browser.stop_discovery()

if __name__ == "__main__":
    test()
