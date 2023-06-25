import pychromecast
from pychromecast.controllers.media import STREAM_TYPE_LIVE, STREAM_TYPE_BUFFERED, METADATA_TYPE_GENERIC
import time
import sys

def playfor(title, url, target, volume, duration):
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[target])
    if not chromecasts:
        print(f"No chromecast with name \"{target}\" discovered")
        sys.exit(1)

    cast = chromecasts[0]
    # Start socket client's worker thread and wait for initial status update
    cast.wait()

    browser.stop_discovery()

    print(f"Found chromecast with name \"{target}\", attempting to play \"{url}\"")

    cast.media_controller.play_media(
        url,
        "audio/mp3",
        stream_type=STREAM_TYPE_LIVE,
        autoplay=True,
        metadata = {
            "metadataType" : METADATA_TYPE_GENERIC,
            "title" : title,
        }
    )
    cast.media_controller.block_until_active()
    level = volume / 100.0
    cast.set_volume(level)
    cast.media_controller.play() # just in case it paused for some reason
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        pass
    cast.wait()
    cast.quit_app()
    cast.disconnect()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "Kitchen"

    title = "The River"
    url = "https://nebcoradio.com:8443/WXRV"
    volume = 15 # %
    secs = 60 * 60 * 2 # 2 hrs
    playfor(title, url, target, volume, secs)
