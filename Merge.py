from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.button import ButtonBehavior, Button
# from kivy.core.window import Window
from kivy.properties import ColorProperty
from kivy.uix.label import Label
from kivy.metrics import dp
# from argon2 import low_level, Type
import base64
import platform
import hashlib
from kivy.core.text import LabelBase
from kivy.config import Config

# Config.set('graphics', 'width', '450')
# Config.set('graphics', 'height', '800')
# Config.set('graphics', 'resizable', '0')

LabelBase.register(name="Roboto", fn_regular="JetBrainsMono-Medium.ttf")

info = platform.uname()   
OS = str(info.system).lower()
sys=str(platform.system()).lower()

if (OS == 'windows') or (OS == 'linux') or (OS == 'macos') or (OS == 'osx'):
    print('Desktop:'+OS)
    print('\nNigger42069:'+sys)
    # Builder.load_file('test.kv')
    Builder.load_file('mobile.kv')
    # Builder.load_file('desktop.kv')
else:
    print('\nNigger42069:'+sys)
    print('Mobile:'+OS)
    Builder.load_file('mobile.kv')

def Hash(password, Salt, Time_Cost, Memory_Cost, Parallelism, hash_length):
    """
    Hashes a password using scrypt.
    
    Args:
        password (str): The password to hash.
        Salt (str): The salt value.
        Time_Cost (int): Used to derive scrypt's 'n' parameter (n = 2**Time_Cost).
        Memory_Cost (int): Desired memory usage in KiB. Used here to compute 'r' so that:
                           memory ≈ n * r * 128 bytes ≈ Memory_Cost * 1024.
        Parallelism (int): scrypt's parallelization factor, 'p'.
        hash_length (int): Desired length of the derived key in bytes.
    
    Returns:
        str: Hexadecimal string representation of the hash.
    """
    # Convert password and salt to bytes.
    password_bytes = password.encode('utf-8')
    salt_bytes = Salt.encode('utf-8')
    
    # Map Time_Cost to n. (n must be a power of 2.)
    n = 2 ** Time_Cost

    # Compute r such that: n * r * 128 ≈ Memory_Cost * 1024.
    # r = (Memory_Cost * 1024) / (n * 128) = (Memory_Cost * 8) / n.
    r = max(1, int((Memory_Cost * 8) / n))
    
    # Parallelism maps directly.
    p = Parallelism
    # Compute scrypt hash.
    result_bytes = hashlib.scrypt(password_bytes, salt=salt_bytes, n=n, r=r, p=p, dklen=hash_length)
    return result_bytes.hex()

CHAR_SETS = [
    # Set 1: Alphanumeric (62 characters)
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "abcdefghijklmnopqrstuvwxyz",
    "0123456789",
    "!@#$%^&*()_+-=",
    "[]\\{}|;',./<>? "
]

def generate_password(enable_sets, hex_input):

    # Validate inputs
    if not isinstance(enable_sets, (list, tuple)) or len(enable_sets) != 5:
        raise ValueError("enable_sets must be a list of 3 booleans")
        
    allowed_sets = [CHAR_SETS[i] for i, enabled in enumerate(enable_sets) if enabled]
    
    if not allowed_sets:
        raise ValueError("At least one character set must be enabled")
    
    # Convert hex input to bytes
    if isinstance(hex_input, str):
        hex_str = hex_input.strip().lower()
        if len(hex_str) % 2 != 0:
            raise ValueError("Hex string must have even length")
        try:
            data = bytes.fromhex(hex_str)
        except ValueError:
            raise ValueError("Invalid hexadecimal characters in input")
    elif isinstance(hex_input, bytes):
        data = hex_input
    else:
        raise TypeError("hex_input must be string or bytes")

    password = []
    for i, byte in enumerate(data):
        # Determine which character set to use
        set_index = i % len(allowed_sets)
        current_set = allowed_sets[set_index]
        
        # Calculate character index using modulo operation
        char_index = byte % len(current_set)
        password.append(current_set[char_index])
    
    return ''.join(password)


class GlobalVars:
    username = StringProperty('')
    password = StringProperty('')

class WelcomeScreen(Screen):
    keyboard = None
    
    def check_password(self):
        GlobalVars.username = self.ids.username_input.text
        GlobalVars.password = self.ids.password_input.text
        self.ids.username_input.text = ''
        self.ids.password_input.text = ''
        
        if GlobalVars.password != "":
            self.manager.current = 'list'
        
        print(f"\nLogin:\nname:{GlobalVars.username}\npassword:{GlobalVars.password}")
        if len(GlobalVars.username) < 8:
            GlobalVars.username = Hash(GlobalVars.username,"H4!?|](hb)",4,8,1,16)
            print(f"\nLogin:\nname:{GlobalVars.username}\npassword:{GlobalVars.password}")

    # def toggle_show(self):
    #     self.ids.toggle_icon
    # def toggle_hide(self):

    
    def toggle_keyboard(self):
        if self.keyboard:
            self.remove_widget(self.keyboard)
            self.keyboard = None
            self.ids.keyboard_placeholder.height = 0
        else:
            self.keyboard = VKeyboard(
                size_hint_y=None,
                height=dp(300),
                layout='qwerty'
            )
            self.keyboard.bind(on_key_up=self.on_keyboard_input)
            self.ids.keyboard_placeholder.height = dp(300)
            self.add_widget(self.keyboard)
    
    def on_keyboard_input(self, keyboard, key, *args):
        if self.ids.username_input.focus:
            self.ids.username_input.text += key
        elif self.ids.password_input.focus:
            self.ids.password_input.text += key

    def on_keyboard_input(self, keyboard, key, *args):
        # Handle special keys
        if key == 'backspace':
            self.handle_backspace()
        elif key == 'enter':
            self.handle_enter()
        elif key == 'spacebar':
            self.handle_space()
        elif key in ['tab', 'shift', 'capslock', 'layout', 'escape']:
            # Ignore these keys
            return
        else:
            self.handle_regular_key(key)
    
    def handle_backspace(self):
        if self.ids.username_input.focus:
            self.ids.username_input.text = self.ids.username_input.text[:-1]
        elif self.ids.password_input.focus:
            self.ids.password_input.text = self.ids.password_input.text[:-1]
    
    def handle_enter(self):
        # Simulate pressing the Submit button
        self.check_password()
    
    def handle_space(self):
        if self.ids.username_input.focus:
            self.ids.username_input.text += ' '
        elif self.ids.password_input.focus:
            self.ids.password_input.text += ' '
    
    def handle_regular_key(self, key):
        if self.ids.username_input.focus:
            self.ids.username_input.text += key
        elif self.ids.password_input.focus:
            self.ids.password_input.text += key

class UsernameExplanationScreen(Screen):
    pass

class ButtonLabel(ButtonBehavior,Label):
    pass

class LoginInfoScreen(Screen):
    pass

class RoundedButton(Button):
    normal_color = ColorProperty([0.2, 0.7, 1, 1])  # Default blue
    pressed_color = ColorProperty([0, 0.4, 0.8, 1])  # Darker blue

class ListScreen(Screen):
    def on_enter(self):
        self.ids.rv.data = [
            {'name': item['name'], 'email': item.get('email', ''), 'index': i}
            for i, item in enumerate(App.get_running_app().items)
        ]

class AddItemScreen(Screen):
    slider_value = NumericProperty(2)  
    
    def on_enter(self):
        self.ids.check1.active = True
        self.ids.check2.active = True
        self.ids.check3.active = True
        self.ids.check4.active = True
        self.ids.check5.active = True
        self.slider_value = 2
        self.ids.slider.value = 2
        self.ids.name_input.text = ''
        self.ids.app_password_input.text = ''

    def add_item(self):
        name = self.ids.name_input.text.strip()
        if not name:
            return
        
        email = self.ids.app_password_input.text.strip()
        checks = [
            self.ids.check1.active,
            self.ids.check2.active,
            self.ids.check3.active,
            self.ids.check4.active,
            self.ids.check5.active
        ]
        

        App.get_running_app().items.append({
            'name': name,
            'email': email,
            'checks': checks,
            'slider_value': self.slider_value
        })

        print(f"\nAdding:\nname:{name}\nemail:{email}\nchecks:{checks}\nslider:{self.slider_value}")
        
        # Clear input fields
        self.ids.name_input.text = ''
        self.ids.app_password_input.text = ''
        self.manager.current = 'list'

class EditItemScreen(Screen):
    edit_index = NumericProperty(-1)
    slider_value = NumericProperty(2)
    
    def on_enter(self):
        app = App.get_running_app()
        if 0 <= self.edit_index < len(app.items):
            item = app.items[self.edit_index]
            self.ids.name_input.text = item['name']
            self.ids.app_password_input.text = item.get('email', '')
            
            # Set checkbox states
            for i in range(5):
                self.ids[f'check{i+1}'].active = item.get('checks', [True, True, True, True, True])[i]


            self.slider_value = item.get('slider_value', 2)
    
    def save_item(self):
        name = self.ids.name_input.text.strip()
        if not name:
            return
        
        email = self.ids.app_password_input.text.strip()
        checks = [
            self.ids.check1.active,
            self.ids.check2.active,
            self.ids.check3.active,
            self.ids.check4.active,
            self.ids.check5.active
        ]
        
        app = App.get_running_app()
        if 0 <= self.edit_index < len(app.items):
            app.items[self.edit_index] = {
                'name': name,
                'email': email,
                'checks': checks,
                'slider_value': self.slider_value 
            }
            self.manager.current = 'list'

        print(f"\nEditing:\nname:{name}\nemail:{email}\nchecks:{checks}\nslider:{self.slider_value}")

class AdditionalInfoScreen(Screen):
    pass

class ResultScreen(Screen):

    def copy_to_clipboard(self):
        text = self.ids.result_input.text
        result_screen = self.manager.get_screen('result')
        result_screen.ids.result_message.text = f"Password Copied\nIt will be deleted & clipboard will be cleared in 10 seconds!"
        system = platform.system()
        
        try:
            if system == 'Linux':
                Clipboard.copy(text)

            else:
                Clipboard.put(text)
        except Exception as e:
            print(f"Clipboard error: {e}")
            try:
                Clipboard.put(text.encode('utf-8'))
            except Exception as e:
                print(f"Fallback clipboard error: {e}")
                result_screen.ids.result_message.text = "Error copying to clipboard"
                return

        Clock.schedule_once(lambda dt: self.clear_clipboard(), 10)
        print(f"\nPlay result:\nname:{text}")

    def clear_clipboard(self):
        system = platform.system()
        try:
            if system == 'Linux':
                Clipboard.copy('')
            else:
                Clipboard.put('')
        except Exception as e:
            print(f"Error clearing clipboard: {e}")
        result_screen = self.manager.get_screen('result')
        result_screen.ids.result_message.text = f"Clipboard cleared & copied password is deleted "
        print("Clipboard content erased after 10 seconds")

class ItemRow(RecycleDataViewBehavior, BoxLayout):
    index = NumericProperty()
    name = StringProperty()
    email = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.name = data['name']
        self.email = data.get('email', '')
        return super().refresh_view_attrs(rv, index, data)

class KeyForge(App):
    items = ListProperty()

    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginInfoScreen(name='login_info'))
        sm.add_widget(ListScreen(name='list'))
        sm.add_widget(AddItemScreen(name='add_item'))
        sm.add_widget(EditItemScreen(name='edit_item'))
        sm.add_widget(AdditionalInfoScreen(name='additional_info'))
        sm.add_widget(ResultScreen(name='result'))
        return sm

    def logout(self):
        # Clear all credentials and data
        GlobalVars.username = ''
        GlobalVars.password = ''
        self.items = []
        self.root.current = 'welcome'

    def delete_item(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]
            self.root.get_screen('list').on_enter()

    def play_item(self, index):
        # Switch to the ResultScreen first
        result_screen = self.root.get_screen('result')
        result_screen.ids.result_message.text = "Generating Password ..."
        result_screen.ids.result_input.text = ""

        self.root.current = 'result'
        
        # Schedule the processing to start after the screen transition
        Clock.schedule_once(lambda dt: self.process_item(index), 0.6)

    def process_item(self, index):
        if 0 <= index < len(self.items):
            item = self.items[index]
            result_screen = self.root.get_screen('result')
            
            App_name = item['name']
            App_password = item.get('email', '')
            character_set = item['checks']
            w = item['slider_value']
            hash_len = (2**w)*8

            if len(App_password)< 16:
                tmp_salt = "HardC0d3d 541ts5HardC0d3d 541ts5HardC0d3d 541ts5HardC0d3d 541ts5"
                App_password = Hash(App_password,tmp_salt,4,1024,1,64)

            
            master_hash = Hash(GlobalVars.password,GlobalVars.username,15,10240,1,64)

            App_hash = Hash(App_name,App_password,14,10240,1,64)

            app_master_hash = Hash(master_hash,App_hash,15,10240,1,hash_len)

            App_key= generate_password(character_set,app_master_hash)


            print(f"\nPlay:\nname:{App_name}\nemail:{App_password}\nchecks:{character_set}\nslider:{w}\nHash length:{hash_len}\nHash:{app_master_hash}\nApp password:{App_key}")

            result_screen.ids.result_input.text = App_key
            
            result_screen.ids.result_message.text = f"Password generated for {item['name']}"

    def edit_item(self, index):
        if 0 <= index < len(self.items):
            edit_screen = self.root.get_screen('edit_item')
            edit_screen.edit_index = index
            edit_screen.on_enter()
            self.root.current = 'edit_item'
            

if __name__ == '__main__':
    KeyForge().run()