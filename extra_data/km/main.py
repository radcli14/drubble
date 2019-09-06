from kivy.app import App
from kivy.uix.button import Button
from kivy.utils import platform
if platform == 'android':
    from kivmob import KivMob, TestIds


class KivMobTest(App):
    banner_ad = None

    def build(self):
        if platform == 'android':
            self.ads = KivMob(TestIds.APP)
            self.ads.new_interstitial(TestIds.INTERSTITIAL)
            self.ads.request_interstitial()

            self.ads.new_banner(TestIds.BANNER, top_pos=True)
            self.ads.request_banner()
            self.ads.show_banner()
            return Button(text='Show Interstitial',
                          on_release=lambda a: self.ads.show_interstitial())
        else:
            return Button(text='Show Banner', on_release=self.show_banner)

    def on_start(self):
        if platform == 'ios':
            from pyobjus import autoClass
            self.banner_ad = autoClass('adSwitch').alloc().init()

    def show_banner(self):
        # Show ads
        self.banner_ad.show_ads()

    def hide_banner(self):
        # Hide ads
        self.banner_ad.hide_ads()

    def on_resume(self):
        self.ads.request_interstitial()


KivMobTest().run()