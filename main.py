from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
from kivymd.toast import toast
import requests
from configparser import ConfigParser
import pyperclip as pc
import os

# Testing stuff


config = ConfigParser()
config.read('config.ini')
api_key = config.get('CONFIG', 'key')

class URLApp(MDApp):
    def open_config(self, *args):
        config_dir = os.path.realpath('config.ini')
        try:
            os.startfile(config_dir)
        except WindowsError:
            toast('Failed to open "config.ini".')

    # Copy shortened url to clipboard
    def copy_to_clipboard(self, args):
        try:
            pc.copy(shortened_url)
            toast("Copied to clipboard!")
        except NameError:
            toast("Nothing to copy! Try generating a URL first.")

    # Clear fields
    def clear(self):
        self.label.text = ""
        self.converted.text = ""
        self.input.text = ""
        self.converted.opacity = 0

    # Use cutt.ly to shorten the URL
    def convert(self, *args):
        url = self.input.text
        api_url = f"https://cutt.ly/api/api.php?key={api_key}&short={url}"
        data = requests.get(api_url).json()["url"]
        if data["status"] == 7:
            global shortened_url
            shortened_url = data["shortLink"]
            self.converted.text = shortened_url
            self.label.text = "Shortened URL:"
            self.converted.opacity = 1
        elif data["status"] == 4:
            toast("Somethings not right... double check your API key!")
        else:
            toast("Invalid URL! Try again.")
            

    def build(self):
        self.title = "URL-CUTT"
        self.icon = "./assets/icon.ico"
        screen = MDScreen()
        
        # Top toolbar
        self.toolbar = MDToolbar(title="")
        self.toolbar.pos_hint = {"top": 1}
        self.toolbar.elevation = 10
        self.toolbar.right_action_items = [
            ["refresh", lambda x: self.clear(), "Reset"], [
                "file-edit", lambda y: self.open_config(), "Edit config file"]]
        
        # App logo
        self.logo = Image(
            source="./assets/logo.png",
            pos_hint = {"center_x": 0.5, "center_y": 0.7}
        )
        
        # Url entry field
        self.input = MDTextField(
            hint_text = "Paste or type a URL here",
            color_mode = "primary",
            halign="center",
            size_hint = (0.8,1),
            pos_hint = {"center_x": 0.5, "center_y": 0.5},
            font_size = 22
        )
        
        # Converted url label
        self.label = MDLabel(
            halign="center",
            pos_hint = {"center_x": 0.5, "center_y": 0.35},
            theme_text_color = "Secondary"
        )

        # Converted url textfield
        self.converted = MDTextField(
            halign="center",
            pos_hint = {"center_x": 0.5, "center_y": 0.3},
            size_hint = (0.8,1),
            color_mode = "primary",
            font_size = 32,
            opacity = 0
        )
        
        # Generate button
        self.generate_button = MDFillRoundFlatButton(
            text="Generate!",
            font_size = 17,
            pos_hint = {"center_x": 0.42, "center_y": 0.2},
            on_press = self.convert
        )
        
        # Copy url button
        self.copy_text = MDFillRoundFlatButton(
            text="Copy URL",
            font_size = 17,
            pos_hint = {"center_x": 0.58, "center_y": 0.2},
            on_press = self.copy_to_clipboard
        )

        # Add elements to window
        screen.add_widget(self.toolbar)
        screen.add_widget(self.copy_text)
        screen.add_widget(self.label)
        screen.add_widget(self.converted)
        screen.add_widget(self.input)
        screen.add_widget(self.generate_button)
        screen.add_widget(self.logo)

        return screen

if __name__ == '__main__':
    URLApp().run()
