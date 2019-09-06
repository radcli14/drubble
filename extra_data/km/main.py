from kivy.app import App
from kivy.uix.button import Button
from kivy.utils import platform
if platform == 'android':
    from kivmob import KivMob, TestIds
elif platform == 'ios':
    from pyobjus import autoclass


class KivMobTest(App):
    adSwitchSuccessful = False

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
        elif platform == 'ios':
            return Button(text='Show Banner', on_release=lambda a: self.show_banner())

    def on_start(self):
        if platform == 'ios':
            try:
                self.banner_ad = autoclass('adSwitch').alloc().init()
                self.adSwitchSuccessful = True
            except:
                print('adSwitch did not load')

    def show_banner(self):
        if self.adSwitchSuccessful:
            # Show ads
            self.banner_ad.show_ads()

    def hide_banner(self):
        if self.adSwitchSuccessful:
            # Hide ads
            self.banner_ad.hide_ads()

    def on_resume(self):
        if platform == 'android':
            self.ads.request_interstitial()


KivMobTest().run()