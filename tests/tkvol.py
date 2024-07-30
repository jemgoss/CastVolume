import tkinter as tk
from tkinter import font
import pychromecast
import zeroconf

class Application(tk.Frame, pychromecast.discovery.AbstractCastListener):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("Volume")
        #self.master.geometry('250x150')
        self.master.option_add("*Font", font.Font(family="Helvetica", size=24))

        self.volumeval = tk.StringVar(self.master)
        tk.Label(self, text="Vol", textvariable=self.volumeval).grid(row=0, sticky=tk.W, padx=10, pady=10)

        tk.Button(self, text='Up', command=self.up).grid(row=1, column=0, sticky=tk.W)
        tk.Button(self, text='Down', command=self.down).grid(row=2, column=0, sticky=tk.W)
        tk.Button(self, text='Quit', command=self.quit).grid(row=3, column=0, sticky=tk.W)

        self.pack()

        self.cast = None
        # self.browser = pychromecast.CastBrowser(pychromecast.SimpleCastListener(), zeroconf.Zeroconf())
        self.browser = pychromecast.CastBrowser(self, zeroconf.Zeroconf())
        self.browser.start_discovery()
        self.after(2000, self.complete_discovery)
        self._job = None

    def doVol(self, val):
        self.cast.set_volume(val, 2.0)
        self._job = None

    def up(self):
        if self._job:
            self.after_cancel(self._job)
        self._job = self.after(500, self.doVol, 0.2)
        # self.cast.set_volume(0.2, 2.0)

    def down(self):
        if self._job:
            self.after_cancel(self._job)
        self._job = self.after(500, self.doVol, 0.1)
        # self.cast.set_volume(0.1, 2.0)

    def add_cast(self, uuid, service):
        print("add_cast", uuid, service)
        pass

    def remove_cast(self, uuid, service, cast_info):
        print("remove_cast", uuid, service, cast_info)
        pass

    def update_cast(self, uuid, service):
        print("update_cast", uuid, service)
        pass

    def complete_discovery(self):
        print(list(map(lambda d: d.friendly_name, self.browser.devices.values())))
        target = "Kitchen"
        device = next(filter(lambda d: d.friendly_name == target, self.browser.devices.values()))
        self.cast = pychromecast.get_chromecast_from_cast_info(device, self.browser.zc)
        self.cast.wait()
        self.cast.register_status_listener(self)

    def new_cast_status(self, status):
        """ Called when a new status received from the Chromecast. """
        if status:
            print("new_cast_status", status)
            if self._job is None:
                self.volumeval.set(str(status.volume_level * 100))

app = Application()
app.mainloop()
