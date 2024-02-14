import pychromecast

def list_chromecasts():
    chromecasts, browser = pychromecast.discover_chromecasts(timeout=2)
    browser.stop_discovery()
    print("Devices:")
    for c in filter(lambda c: c.cast_type != "group", chromecasts):
        print("\t", c.friendly_name)
    print("Groups:")
    for c in filter(lambda c: c.cast_type == "group", chromecasts):
        print("\t", c.friendly_name)

def list_chromecasts2():
    chromecasts, browser = pychromecast.discover_chromecasts(timeout=2)
    browser.stop_discovery()
    print("Devices:")
    for c in sorted(chromecasts, key=lambda c: str(c.cast_type)):
        print("\t", c.cast_type, "\t", c.friendly_name)

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
    list_chromecasts2()
