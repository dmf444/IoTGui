from kivy.animation import Animation
from kivy.app import App
from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from collections import OrderedDict


from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from screens.widget import custom_widgets as CustomWidgets


class MainScreenLayout(GridLayout):
    screen = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainScreenLayout, self).__init__(**kwargs)
        with self.canvas.before:
            self.rect= Rectangle(source='resources/background.png', size=[SCREEN_WIDTH, SCREEN_HEIGHT], pos=self.pos)
        self.page = 0
        buttons = self.get_button_list()
        keys = list(buttons.keys())
        page_number = self.page * 8

        if(page_number + 0 < len(keys)):
            self.button_1 = CustomWidgets.build_button(keys[page_number + 0], 63,230, [144, 144], [-50,0], "resources/button.png")
            self.button_1.bind(on_press=buttons[keys[page_number + 0]])
            self.add_widget(self.button_1)

        if(page_number + 1 < len(keys)):
            self.button_2 = CustomWidgets.build_button(keys[page_number + 1], 243, 230, [144, 144], [-50,0], "resources/button.png")
            self.button_2.bind(on_press=buttons[keys[page_number + 1]])
            self.add_widget(self.button_2)

        if(page_number + 2 < len(keys)):
            self.button_3 = CustomWidgets.build_button(keys[page_number + 2], 424, 230, [144, 144], [-50,0], "resources/button.png")
            self.button_3.bind(on_press=buttons[keys[page_number + 2]])
            self.add_widget(self.button_3)

        if(page_number + 3 < len(keys)):
            self.button_4 = CustomWidgets.build_button(keys[page_number + 3], 604, 230, [144, 144], [-50,0], "resources/button.png")
            self.button_4.bind(on_press=buttons[keys[page_number + 3]])
            self.add_widget(self.button_4)

        if(page_number + 4 < len(keys)):
            self.button_5 = CustomWidgets.build_button(keys[page_number + 4], 63, 70, [144,144], [-50, 0], "resources/button.png")
            self.button_5.bind(on_press=buttons[keys[page_number + 4]])
            self.add_widget(self.button_5)

        if(page_number + 5 < len(keys)):
            self.button_6 = CustomWidgets.build_button(keys[page_number + 5], 243, 70, [144, 144], [-50,0], "resources/button.png")
            self.button_6.bind(on_press=buttons[keys[page_number + 5]])
            self.add_widget(self.button_6)

        if(page_number + 6 < len(keys)):
            self.button_7 = CustomWidgets.build_button(keys[page_number + 6], 424,70, [144, 144], [-50,0], "resources/button.png")
            self.button_7.bind(on_press=buttons[keys[page_number + 6]])
            self.add_widget(self.button_7)

        if(page_number + 7 < len(keys)):
            self.button_8 = CustomWidgets.build_button(keys[page_number + 7], 604, 70, [144, 144], [-50,0], "resources/button.png")
            self.button_8.bind(on_press=buttons[keys[page_number + 7]])
            self.add_widget(self.button_8)

        self.title_image = CustomWidgets.build_label("Raspberry Pi IoT", 90, 420, [264, 79], [-140, 35], "resources/TitleBar.png")
        self.add_widget(self.title_image)

        self.top_bar = Image(source='resources/barDesign.png', size=[694, 48], pos=[self.title_image.x - 20, 365 + 35])
        self.top_bar.color[3] = 0.0
        self.add_widget(self.top_bar)
        self.bottom_bar = Image(source='resources/bottombar.png', size=[768, 33], pos=[17, 10])
        self.bottom_bar.color[3] = 0.0
        self.add_widget(self.bottom_bar)

        self.run_startup_animations()

    def get_button_list(self):
        button_dict = OrderedDict()
        button_dict["Wemo Switches"] = self.wemo_devices
        button_dict["Weather Report"] = self.wemo_devices
        button_dict["IFTTT"] = self.wemo_devices
        button_dict["Garage Doors"] = self.wemo_devices
        button_dict["Sprinkler System"] = self.wemo_devices
        button_dict["Computer Controls"] = self.wemo_devices
        button_dict["Sonos Speakers"] = self.wemo_devices
        button_dict["Exit"] = self.exit_button_handler
        button_dict["Samsung TVs"] = self.wemo_devices


        return button_dict

    def run_startup_animations(self):
        animation = Animation(y=365, duration=1)
        animation2 = Animation(pos=[self.title_image.rect.pos[0], 365 + 35], duration=1)
        animation.start(self.title_image)
        animation2.start(self.title_image.rect)

        animation2.bind(on_complete=self.run_fadein_animations)

    def run_fadein_animations(self, *args):
        top_bar_in = Animation(color=[1.0, 1.0, 1.0, 1.0], duration=0.5)
        bottom_bar_in = Animation(color=[1.0, 1.0, 1.0, 1.0], duration=0.5)
        top_bar_in.start(self.top_bar)
        bottom_bar_in.start(self.bottom_bar)

    def exit_button_handler(self, *args):
        App.get_running_app().stop()

    def wemo_devices(self, *args):
        self.screen.manager.current = "Wemo"


class MainScreen(Screen):
    def __init__(self, **kw):
        super(MainScreen, self).__init__(**kw)

        self.add_widget(MainScreenLayout(screen=self))
