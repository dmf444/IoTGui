from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, RiseInTransition

from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from screens.main_menu import MainScreen
from backend.wemo import wemo
from screens.wemo_menu import WemoScreen
from screens.weather_menu import WeatherScreen


class IOTApp(App):
    def __init__(self, **kwargs):
        super(IOTApp, self).__init__(**kwargs)
        self.screen_manager = ScreenManager(transition=RiseInTransition())
        self.screen_manager.transition.duration = .2

        self.screen_manager.add_widget(MainScreen(name='main'))
        self.screen_manager.add_widget(WemoScreen(name='Wemo'))
        self.screen_manager.add_widget(WeatherScreen(name='Weather'))
        self.screen_manager.current = "main"

    def build(self):
        return self.screen_manager

if __name__ == "__main__":
    Config.set('graphics', 'borderless', '1')
    Config.set('graphics', 'height', str(SCREEN_HEIGHT))
    Config.set('graphics', 'width', str(SCREEN_WIDTH))
    Config.set('graphics', 'window_state', 'visible')
    Config.set('graphics', 'resizable', '0')
    wemo.scan_for_devices()

    app = IOTApp()
    app.run()
