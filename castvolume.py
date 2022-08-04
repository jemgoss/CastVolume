import tkinter as tk
from tkinter import ttk
from tkinter import font
from argparse import ArgumentParser
import logging
import pychromecast
import zeroconf
import json
import threading
import sys
import os

DEFAULT_CONFIG_FILE=os.path.expanduser("~/.config/castVolume.conf")

DEFAULT_CONFIG = {
    "discoveryTimeout": 2000,
    "RememberLastTarget": True,
    "InitializeTarget": True
}

class Application(tk.Frame):
    def __init__(self, config, debug, master=None):
        self.config = config

        tk.Frame.__init__(self, master)
        self.master.title("Volume")
        #self.master.geometry('250x150')
        self.master.option_add("*Font", font.Font(family="Helvetica", size=24))

        self._job = None

        #tk.Label(self, text="Target:", font=('', 24)).grid(row=0, sticky=tk.W)
        tk.Label(self, text="Target:").grid(row=0, sticky=tk.W, padx=10, pady=10)
        self.targetval = tk.StringVar(self.master)
        self.targetval.set("Loading...")
        self.target = ttk.Combobox(self,
            textvariable=self.targetval,
            #values=("foo", "bar", "baz"),
            state='readonly',
            #font=('', 24),
            width=19)
        self.target.grid(row=1, sticky=tk.W, padx=10)
        self.target.current()
        #self.target.index(0)
        self.target.bind('<<ComboboxSelected>>', self.onTargetSelected)
        #self.target.pack()

        self.volumeval = tk.IntVar(self.master)
        self.volume = tk.Scale(self,
            from_=0, to=100,
            variable=self.volumeval,
            orient=tk.HORIZONTAL,
            #orient=tk.VERTICAL,
            command=self.onUpdateVolume,
            label="Volume:",
            #font=('', 24),
            length=200,
            width=20)
        self.volume.grid(row=2, sticky=tk.W, padx=10, pady=10)
        #self.slider.pack()
        #self.slider.bind("<MouseWheel>", self.OnMouseWheel)
        self.volume.bind('<Button-4>', self.onMouseWheel)
        self.volume.bind('<Button-5>', self.onMouseWheel)
        self.volume.configure(state="disabled")

        tk.Button(self, text='Quit', command=self.quit).grid(row=3, column=0, sticky=tk.W)
        if debug:
            tk.Button(self, text='Threads', command=self.print_threads).grid(row=3, sticky=tk.E)

        self.pack()

        self.cast = None
        self.browser = pychromecast.CastBrowser(self, zeroconf.Zeroconf())
        # This allows us to connect to the initial device as soon as it's discovered.
        self.connect_on_discovery = None
        if config.get("InitializeTarget"):
            self.connect_on_discovery = config.get("LastTarget")
        self.browser.start_discovery()
        self.after(self.config.get("discoveryTimeout"), self.complete_discovery)

    def add_cast(self, uuid, service):
        if self.connect_on_discovery:
            device = self.browser.devices[uuid]
            if device.friendly_name == self.connect_on_discovery:
                self.targetval.set(device.friendly_name)
                self.connectDevice(device)

    def remove_cast(self, uuid, service, cast_info):
        # print("remove_cast", uuid, service, cast_info)
        pass

    def update_cast(self, uuid, service):
        # print("update_cast", uuid, service)
        pass

    def complete_discovery(self):
        # Called a short while after discovery was started.
        # We could stop the discovery, but would then have to create a new ZC instance for the cast listener.
        #self.browser.stop_discovery()
        # TODO: sort so Groups are at the end?
        self.target['values'] = list(map(lambda d: d.friendly_name, self.browser.devices.values()))

        # # Groups at the end
        # self.devices.sort(key=lambda d: (d[2] == "Google Cast Group", d[3]))
        # self.target['values'] = list(map(lambda d: d[3], self.devices))

        if self.cast is None:
            # No target selected during discovery: replace "Loading..." with prompt:
            self.targetval.set("[Select device]")

    def onTargetSelected(self, event):
        #print("onTargetSelected", event, event.widget.get(), self.targetval.get())
        target = event.widget.get()
        device = next(filter(lambda d: d.friendly_name == target, self.browser.devices.values()))
        self.connectDevice(device)

    def connectDevice(self, device):
        if self.cast:
            self.cast.disconnect()
        self.cast = pychromecast.get_chromecast_from_cast_info(device, self.browser.zc)
        self.cast.wait()
        self.volume.configure(state="normal")
        self.volumeval.set(self.cast.status.volume_level * 100)
        self.cast.register_status_listener(self)
        if self.config.get("RememberLastTarget"):
            self.config["LastTarget"] = device.friendly_name

    def new_cast_status(self, status):
        """ Called when a new status received from the Chromecast. """
        if status:
            self.volumeval.set(status.volume_level * 100)

    def onMouseWheel(self, event):
        #print("scroll", event.num)
        incr = 1 if event.num == 4 else -1
        #self.volume.set(self.volume.get() + incr)
        #self.slider.set(self.slider.get() + incr)
        event.widget.set(event.widget.get() + incr)

    def onUpdateVolume(self, event):
        if self._job:
            self.after_cancel(self._job)
        self._job = self.after(500, self.doUpdateVolume)

    def doUpdateVolume(self):
        self._job = None
        #print("setVolume:", self.volume.get(), self.volumeval.get())
        self.cast.set_volume(self.volumeval.get() / 100.0)

    def print_threads(self):
        print(",".join(map(lambda x: x.name, threading.enumerate())))

if __name__ == "__main__":
    parser = ArgumentParser(description="CastVolume")
    parser.add_argument("--config", "-c", default=DEFAULT_CONFIG_FILE, help="configuration file")
    parser.add_argument("--debug", "-d", action='store_true', help="enable debug")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(format="%(asctime)s: %(message)s", datefmt="%m/%d/%Y %H:%M:%S", level=logging.DEBUG)
    if os.path.exists(args.config):
        with open(args.config) as f:
            config = json.load(f)
    else:
        config = DEFAULT_CONFIG
    app = Application(config, args.debug)
    app.mainloop()
    with open(args.config, "w") as f:
        json.dump(config, f, indent=2)
