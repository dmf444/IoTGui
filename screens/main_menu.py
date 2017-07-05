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

        # Next Page buttons
        self.button_back = CustomWidgets.build_button("", 0, 166, [33, 117], [-50, 0], "resources/backButton.png")
        self.button_back.bind(on_press=self.page_changer(-1))
        self.add_widget(self.button_back)
        self.button_next = CustomWidgets.build_button("", 767, 166, [33, 117], [-50, 0], "resources/forwardButton.png")
        self.button_next.bind(on_press=self.page_changer(+1))
        self.add_widget(self.button_next)

        # Set first button page
        self.page = 0
        self.button_widgets = []
        self.change_page(0)

        # Make things look nice
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

    # event handler factory
    # For magic page changing
    def page_changer(self, p):
        obj = self
        def evt_handler(self):
            obj.page += p
            if obj.page < 0:
                obj.page = 0
            if obj.page > int(len(obj.get_button_list())/8): obj.page -= 1
            obj.change_page(obj.page)
        return evt_handler

    def hide_pagination(self):
        pass # todo

    def change_page(self, to_page):
        for i in self.button_widgets:
            self.remove_widget(i)

        page_number = to_page * 8
        buttons = self.get_button_list()
        for j, buttonI in enumerate(buttons.keys()):
            if j < page_number:
                continue
            if j > page_number + 7:
                continue
            x_pos = (63, 243, 424, 604)[j % 4]
            y_pos = (230, 70)[int(j / 4) % 2]
            button = CustomWidgets.build_button(buttonI, x_pos, y_pos, [144, 144], [-50, 0], "resources/button.png")
            button.bind(on_press=buttons[buttonI])
            self.button_widgets.append(button)
            self.add_widget(button)
        self.hide_pagination()

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
