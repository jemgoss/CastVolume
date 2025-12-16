import pychromecast
import time
import logging

logging.basicConfig(format="%(asctime)s: %(message)s", datefmt="%m/%d/%Y %H:%M:%S", level=logging.INFO)

def print_cc(cc):
    ci = cc.cast_info
    # print(f"{cc.cast_type:10}{ci.friendly_name}")
    model = ci.model_name
    if ci.manufacturer:
        model = model + f" ({ci.manufacturer})"
    print(f"{cc.cast_type:10}{ci.friendly_name:30}{model:35}{ci.host}:{ci.port}")

def deprecated_list_chromecasts():
    chromecasts, browser = pychromecast.get_chromecasts(timeout=2)
    browser.stop_discovery()
    for cc in sorted(chromecasts, key=lambda cc: str(cc.cast_type)):
        print_cc(cc)

def list_chromecasts():
    browser = pychromecast.get_chromecasts(timeout=2, blocking=False, callback=print_cc)
    time.sleep(2)
    browser.stop_discovery()

# TXT Data: "id=e371205a-c7fb-436c-864d-6da6690a300f" "cd=e371205a-c7fb-436c-864d-6da6690a300f" "rm=575F7C677D9F3196"
#   "ve=05" "md=Google Cast Group" "ic=/setup/icon.png" "fn=Living Room pair" "ca=199332"
#   "st=0" "bs=FA8FCA69A8FB" "nf=1" "rs="
# TXT Data: "id=87bafeaad1d01c6751db0ca3b720b444" "cd=BAC4543046CAAF66999DA1DFD3520BB4" "rm=575F7C677D9F3196"
#   "ve=05" "md=Nest Audio" "ic=/setup/icon.png" "fn=Living Room L speaker" "ca=199428"
#   "st=0" "bs=FA8FCA69A8FB" "nf=1" "rs="
# TXT Data: "id=2fee5ef45daaf5ccc1837154ed1f8e3e" "cd=8AE8B8B9D4E6DD3122268B4E1F3B6156" "rm=CDEBB04973AAF214"
#   "ve=05" "md=Nest Audio" "ic=/setup/icon.png" "fn=Living Room R speaker" "ca=199428"
#   "st=2" "bs=FA8FCA8B69FE" "nf=1" "rs="

if __name__ == '__main__':
    # import sys
    # verbose = len(sys.argv) > 1 and sys.argv[1] == "-v"
    list_chromecasts()
