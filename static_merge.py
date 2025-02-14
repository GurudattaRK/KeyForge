# Added static type imports
from typing import Final, Tuple, List, Union, Optional, TypedDict
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.vkeyboard import VKeyboard
from kivy.metrics import dp
from argon2 import low_level, Type
import base64

# TypedDict for items in the inventory
class Item(TypedDict):
    name: str
    email: str
    checks: Tuple[bool, bool, bool, bool, bool]
    slider_value: int

# Constants with Final type and explicit tuple sizing
CHAR_SETS: Final[Tuple[str, str, str, str, str]] = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "abcdefghijklmnopqrstuvwxyz",
    "0123456789",
    "!@#$%^&*()_+-=",
    "[]\\{}|;',./<>? "
)

def Argon2i_Hash(
    password: str,
    Salt: str,
    Time_Cost: int,
    Memory_Cost: int,
    Parallelism: int,
    hash_length: int
) -> str:
    """Generate Argon2i hash with static typing"""
    password_bytes: bytes = password.encode('utf-8')
    salt_bytes: bytes = Salt.encode('utf-8')
    
    # Type annotated variables
    hash_bytes: bytes = low_level.hash_secret(
        secret=password_bytes,
        salt=salt_bytes,
        time_cost=Time_Cost,
        memory_cost=Memory_Cost,
        parallelism=Parallelism,
        hash_len=hash_length,
        type=Type.I,
        version=19
    )
    
    hash_str: str = hash_bytes.decode('utf-8')
    base64_hash: str = hash_str.split('$')[-1]
    
    # Fixed length padding calculation
    missing_padding: int = len(base64_hash) % 4
    if missing_padding:
        base64_hash += '=' * (4 - missing_padding)
    
    hash_bytes = base64.urlsafe_b64decode(base64_hash)
    hex_hash: str = hash_bytes.hex()
    
    return hex_hash

def generate_password(
    enable_sets: Tuple[bool, bool, bool, bool, bool],  # Fixed size tuple
    hex_input: Union[str, bytes]
) -> str:
    """Generate password with strict type checks"""
    # Validate input types
    if not isinstance(enable_sets, tuple) or len(enable_sets) != 5:
        raise ValueError("enable_sets must be a tuple of 5 booleans")
        
    # Tuple comprehension for allowed sets
    allowed_sets: Tuple[str, ...] = tuple(
        CHAR_SETS[i] for i, enabled in enumerate(enable_sets) if enabled
    )
    
    if not allowed_sets:
        raise ValueError("At least one character set must be enabled")
    
    # Type narrowing for hex input
    data: bytes
    if isinstance(hex_input, str):
        hex_str: str = hex_input.strip().lower()
        if len(hex_str) % 2 != 0:
            raise ValueError("Hex string must have even length")
        data = bytes.fromhex(hex_str)
    elif isinstance(hex_input, bytes):
        data = hex_input
    else:
        raise TypeError("hex_input must be string or bytes")

    password: List[str] = []
    for i, byte in enumerate(data):
        set_index: int = i % len(allowed_sets)
        current_set: str = allowed_sets[set_index]
        char_index: int = byte % len(current_set)
        password.append(current_set[char_index])
    
    return ''.join(password)

# Rest of the Builder.load_string remains the same as it's UI definition
Builder.load_string('''
<RoundedButton@Button>:
    background_normal: ''
    background_color: (0.1, 0.5, 0.8, 1)
    size_hint: None, None
    size: dp(120), dp(40)
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10,]
                    
<WelcomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        
        Label:
            text: 'Welcome!'
            font_size: '20sp'
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(40)
            spacing: 5
            
            TextInput:
                id: username_input
                hint_text: 'Username'
                multiline: False
                size_hint_x: 0.7
                write_tab: False
                on_focus: root.toggle_keyboard()
                
            RoundedButton:
                text: 'Why username?'
                size_hint_x: 0.3
                on_press: root.manager.current = 'username_explanation'
        
        TextInput:
            id: password_input
            hint_text: 'Password'
            password: True
            multiline: False
            size_hint_y: None
            height: dp(40)
            write_tab: False
            on_focus: root.toggle_keyboard()
        
        RoundedButton:
            text: 'Know more about login'
            on_press: root.manager.current = 'login_info'
        
        RoundedButton:
            text: 'Submit'
            on_press: root.check_password()

        Widget:
            id: keyboard_placeholder
            size_hint_y: None
            height: 0

<UsernameExplanationScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        
        Label:
            text: 'Username Explanation'
            font_size: '20sp'
            
        Label:
            text: 'Username helps us personalize your experience and keep your data secure. Please use a unique username that others can\\'t easily guess.'
            halign: 'center'
            valign: 'middle'
            text_size: self.size
        
        Button:
            text: 'Back'
            size_hint_y: None
            height: '40sp'
            on_press: root.manager.current = 'welcome'                   

<LoginInfoScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        
        Label:
            text: 'Login Information'
            font_size: '20sp'
            
        Label:
            text: 'For security reasons:\\n- Use a strong password\\n- Don\\'t share your credentials\\n- Virtual keyboard helps prevent keyloggers'
            halign: 'center'
        
        Button:
            text: 'Back'
            size_hint_y: None
            height: '40sp'
            on_press: root.manager.current = 'welcome'
                    
<ListScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        RecycleView:
            id: rv
            viewclass: 'ItemRow'
            scroll_type: ['bars', 'content']
            
            RecycleBoxLayout:
                orientation: 'vertical'
                default_size: None, dp(50)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
        
        BoxLayout:
            size_hint_y: None
            height: '40sp'
            spacing: 5
            
            Button:
                text: 'Add New Item'
                on_press: root.manager.current = 'add_item'
            
            Button:
                text: 'Logout'
                on_press: app.logout()

<ItemRow>:
    orientation: 'horizontal'
    size_hint_y: None
    height: '40sp'
    spacing: 5
    
    Label:
        text: root.name
        size_hint_x: 0.3
        
    Label:
        text: root.email if root.email else '-'
        size_hint_x: 0.25
    
    Button:
        text: 'Play'
        size_hint_x: 0.15
        on_press: app.play_item(root.index)
        
    Button:
        text: 'Edit'
        size_hint_x: 0.15
        on_press: app.edit_item(root.index)
    
    Button:
        text: 'Delete'
        size_hint_x: 0.15
        on_press: app.delete_item(root.index)

<AddItemScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        
        Label:
            text: 'Add New Item'
            font_size: '20sp'
            
        TextInput:
            id: name_input
            hint_text: 'App/Website name (required)'
            multiline: False
            size_hint_y: None
            height: dp(40)
            
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(40)
            spacing: 10
            
            TextInput:
                id: email_input
                hint_text: 'App/Website password (optional)'
                multiline: False
                size_hint_x: 0.8
                
            RoundedButton:
                text: 'Know More'
                size_hint_x: 0.2
                on_press: root.manager.current = 'additional_info'
        
        Label:
            text: 'Choose which characters do you want to include in your password:'
            size_hint_y: None
            height: dp(30)
        
        GridLayout:
            cols: 2
            rows: 5
            size_hint_y: None
            height: dp(80)
            
            CheckBox:
                id: check1
                active: True
            Label:
                text: 'Uppercase Alphabets (Capital letters)'
            
            CheckBox:
                id: check2
                active: True
            Label:
                text: 'Lowercase Alphabets (Small letters)'
            
            CheckBox:
                id: check3
                active: True
            Label:
                text: 'Numbers'
            
            CheckBox:
                id: check4
                active: True
            Label:
                text: 'Special characters like ! @ # $ % ^ & * ( ) _ + - = '
            
            CheckBox:
                id: check5
                active: True
            Label:
                text: "Special characters like [ ] \\\ { } | ; ' , . / < > ? (also includes space)"
        
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(60)
            spacing: 5
            
            Label:
                text: f'Password Length: {2**(int(root.slider_value))*(8)}'
                size_hint_y: None
                height: dp(20)
                
            Slider:
                id: slider
                min: 1
                max: 4
                step: 1
                value: 2
                value_normalized: (self.value - self.min) / (self.max - self.min)
                on_value: root.slider_value = int(self.value)
        
        RoundedButton:
            text: 'Add Item'
            on_press: root.add_item()
                    
        RoundedButton:
            text: 'Back'
            size_hint_y: None
            height: '40sp'
            on_press: root.manager.current = 'list'

<EditItemScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        
        Label:
            text: 'Edit Item'
            font_size: '20sp'
            
        TextInput:
            id: name_input
            hint_text: 'App/Website name (required)'
            multiline: False
            size_hint_y: None
            height: dp(40)
            
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(40)
            spacing: 10
            
            TextInput:
                id: email_input
                hint_text: 'App/Website password (optional)'
                multiline: False
                size_hint_x: 0.8
                
            RoundedButton:
                text: 'Know More'
                size_hint_x: 0.2
                on_press: root.manager.current = 'additional_info'
        
        Label:
            text: 'Choose which characters do you want to include in your password:'
            size_hint_y: None
            height: dp(30)
        
        GridLayout:
            cols: 2
            rows: 5
            size_hint_y: None
            height: dp(80)
            
            CheckBox:
                id: check1
                active: True
            Label:
                text: 'Uppercase Alphabets (Capital letters)'
            
            CheckBox:
                id: check2
                active: True
            Label:
                text: 'Lowercase Alphabets (Small letters)'
            
            CheckBox:
                id: check3
                active: True
            Label:
                text: 'Numbers'
            
            CheckBox:
                id: check4
                active: True
            Label:
                text: 'Special characters like ! @ # $ % ^ & * ( ) _ + - = '
            
            CheckBox:
                id: check5
                active: True
            Label:
                text: "Special characters like [ ] \\\ { } | ; ' , . / < > ? (also includes space)"

        
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(60)
            spacing: 5
            
            Label:
                text: f'Password Length: {2**(int(root.slider_value))*(8)}'
                size_hint_y: None
                height: dp(20)
                
            Slider:
                id: slider
                min: 1
                max: 4
                step: 1
                value: root.slider_value
                value_normalized: (self.value - self.min) / (self.max - self.min)
                on_value: root.slider_value = int(self.value)

        RoundedButton:
            text: 'Save Changes'
            on_press: root.save_item()
                    
        RoundedButton:
            text: 'Back'
            size_hint_y: None
            height: '40sp'
            on_press: root.manager.current = 'list'

<AdditionalInfoScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        
        Label:
            text: 'Additional Information'
            font_size: '20sp'
            
        Label:
            text: 'Email field is optional.\\nIf provided, it will be used along with name for processing.'
            halign: 'center'
        
        Button:
            text: 'Back'
            size_hint_y: None
            height: '40sp'
            on_press: root.manager.current = 'add_item'

<ResultScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
                    
        Label:
            id: result_message
            text: 'Generating password....'
            font_size: '20sp'
        
        TextInput:
            id: result_input
            text: ''
            password: True
            readonly: True
            multiline: False
            size_hint_y: None
            height: '40sp'
            
        Button:
            text: 'Copy to Clipboard'
            size_hint_y: None
            height: '40sp'
            on_press: root.copy_to_clipboard()
        
        Button:
            text: 'Back to List'
            size_hint_y: None
            height: '40sp'
            on_press: root.manager.current = 'list'
''')

class GlobalVars:
    username: str = StringProperty('')
    password: str = StringProperty('')

class WelcomeScreen(Screen):
    keyboard: Optional[VKeyboard] = None  # Explicit optional type
    
    def check_password(self) -> None:
        GlobalVars.username = self.ids.username_input.text
        GlobalVars.password = self.ids.password_input.text
        self.ids.username_input.text = ''
        self.ids.password_input.text = ''
        
        if GlobalVars.password != "":
            self.manager.current = 'list'

        print(f"\nLogin:\nname:{GlobalVars.username}\npassword:{GlobalVars.password}")
        if len(GlobalVars.username) < 8:
            GlobalVars.username = Argon2i_Hash(GlobalVars.username, "H4!?|](hb)", 4, 10, 1, 16)
            print(f"\nLogin:\nname:{GlobalVars.username}\npassword:{GlobalVars.password}")



    def toggle_keyboard(self) -> None:
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
    
    def on_keyboard_input(self, keyboard: VKeyboard, key: str, *args: any) -> None:
        if self.ids.username_input.focus:
            self.ids.username_input.text += key
        elif self.ids.password_input.focus:
            self.ids.password_input.text += key

    def on_keyboard_input(self, keyboard: VKeyboard, key: str, *args: any) -> None:
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
            # Handle regular keys
            self.handle_regular_key(key)
    
    def handle_backspace(self) -> None:
        """Handle backspace key with type annotations"""
        if self.ids.username_input.focus:
            self.ids.username_input.text = self.ids.username_input.text[:-1]
        elif self.ids.password_input.focus:
            self.ids.password_input.text = self.ids.password_input.text[:-1]
    
    def handle_enter(self) -> None:
        """Handle enter key with type annotations"""
        # Simulate pressing the Submit button
        self.check_password()
    
    def handle_space(self) -> None:
        """Handle spacebar key with type annotations"""
        if self.ids.username_input.focus:
            self.ids.username_input.text += ' '
        elif self.ids.password_input.focus:
            self.ids.password_input.text += ' '
    
    def handle_regular_key(self, key: str) -> None:
        """Handle regular key input with type annotations"""
        if self.ids.username_input.focus:
            self.ids.username_input.text += key
        elif self.ids.password_input.focus:
            self.ids.password_input.text += key

class UsernameExplanationScreen(Screen):
    pass  # No additional logic, so no typing needed

class LoginInfoScreen(Screen):
    pass  # No additional logic, so no typing needed

class ListScreen(Screen):
    def on_enter(self) -> None:
        """Type-annotated method to populate RecycleView data"""
        app: InventoryApp = App.get_running_app()
        self.ids.rv.data = [
            {'name': item['name'], 'email': item.get('email', ''), 'index': i}
            for i, item in enumerate(app.items)
        ]

class AddItemScreen(Screen):
    slider_value: int = NumericProperty(2)  # Explicit type annotation
    
    def on_enter(self) -> None:
        """Reset screen state with type annotations"""
        self.ids.check1.active = True
        self.ids.check2.active = True
        self.ids.check3.active = True
        self.ids.check4.active = True
        self.ids.check5.active = True
        self.slider_value = 2
        self.ids.slider.value = 2
        self.ids.name_input.text = ''
        self.ids.email_input.text = ''

    def add_item(self) -> None:
        """Add new item with type checking"""
        name: str = self.ids.name_input.text.strip()
        if not name:
            return
        
        email: str = self.ids.email_input.text.strip()
        checks: Tuple[bool, bool, bool, bool, bool] = (
            self.ids.check1.active,
            self.ids.check2.active,
            self.ids.check3.active,
            self.ids.check4.active,
            self.ids.check5.active
        )
        
        app: InventoryApp = App.get_running_app()
        app.items.append({
            'name': name,
            'email': email,
            'checks': checks,
            'slider_value': self.slider_value
        })

        self.ids.name_input.text = ''
        self.ids.email_input.text = ''
        self.manager.current = 'list'

class EditItemScreen(Screen):
    edit_index: int = NumericProperty(-1)
    slider_value: int = NumericProperty(2)
    
    def on_enter(self) -> None:
        """Load item data with type annotations"""
        app: InventoryApp = App.get_running_app()
        if 0 <= self.edit_index < len(app.items):
            item: Item = app.items[self.edit_index]
            self.ids.name_input.text = item['name']
            self.ids.email_input.text = item.get('email', '')
            
            for i in range(5):
                self.ids[f'check{i+1}'].active = item.get('checks', (True, True, True, True, True))[i]

            self.slider_value = item.get('slider_value', 2)
    
    def save_item(self) -> None:
        """Save edited item with type checking"""
        name: str = self.ids.name_input.text.strip()
        if not name:
            return
        
        email: str = self.ids.email_input.text.strip()
        checks: Tuple[bool, bool, bool, bool, bool] = (
            self.ids.check1.active,
            self.ids.check2.active,
            self.ids.check3.active,
            self.ids.check4.active,
            self.ids.check5.active
        )
        
        app: InventoryApp = App.get_running_app()
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
    pass  # No additional logic, so no typing needed

class ResultScreen(Screen):
    def copy_to_clipboard(self) -> None:
        """Copy password to clipboard with type annotations"""
        text: str = self.ids.result_input.text
        result_screen: ResultScreen = self.manager.get_screen('result')
        result_screen.ids.result_message.text = ("Password Copied\nIt will be deleted & clipboard will be cleared in 10 seconds!")

        Clipboard.put(text)
        Clock.schedule_once(lambda dt: self.clear_clipboard(), 10)
        print(f"\nPlay result:\nname:{text}")


    def clear_clipboard(self) -> None:
        """Clear clipboard with type annotations"""
        Clipboard.put('')
        result_screen: ResultScreen = self.manager.get_screen('result')
        result_screen.ids.result_message.text = "Copied password is deleted & Clipboard cleared"
        print("\nclipboard data:",Clipboard.get())
        print("Clipboard content erased after 5 seconds")

class ItemRow(RecycleDataViewBehavior, BoxLayout):
    index: int = NumericProperty()
    name: str = StringProperty()
    email: str = StringProperty()

    def refresh_view_attrs(self,rv,index: int,data: dict) -> None:
        """Update view attributes with type annotations"""
        self.index = index
        self.name = data['name']
        self.email = data.get('email', '')
        return super().refresh_view_attrs(rv, index, data)

class InventoryApp(App):
    items: List[Item] = ListProperty()  # Explicitly typed as List[Item]

    def build(self) -> ScreenManager:
        """Build the app's screen manager with type annotations."""
        sm: ScreenManager = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(UsernameExplanationScreen(name='username_explanation'))
        sm.add_widget(LoginInfoScreen(name='login_info'))
        sm.add_widget(ListScreen(name='list'))
        sm.add_widget(AddItemScreen(name='add_item'))
        sm.add_widget(EditItemScreen(name='edit_item'))
        sm.add_widget(AdditionalInfoScreen(name='additional_info'))
        sm.add_widget(ResultScreen(name='result'))
        return sm

    def logout(self) -> None:
        """Clear all credentials and data with type annotations."""
        GlobalVars.username = ''
        GlobalVars.password = ''
        self.items = []
        self.root.current = 'welcome'

    def delete_item(self, index: int) -> None:
        """Delete an item from the list with type checking."""
        if 0 <= index < len(self.items):
            del self.items[index]
            self.root.get_screen('list').on_enter()

    def play_item(self, index: int) -> None:
        """Switch to the ResultScreen and schedule password generation."""
        self.root.current = 'result'
        Clock.schedule_once(lambda dt: self.process_item(index), 0.75)

    def process_item(self, index: int) -> None:
        """Process an item to generate a password with type annotations."""
        if 0 <= index < len(self.items):
            item: Item = self.items[index]
            result_screen: ResultScreen = self.root.get_screen('result')
            
            App_name: str = item['name']
            App_password: str = item.get('email', '')
            character_set: Tuple[bool, bool, bool, bool, bool] = item['checks']
            w: int = item['slider_value']
            hash_len: int = (2**w) * 8

            # Ensure App_password meets minimum length requirement
            if len(App_password) < 4:
                App_password = "HardC0d3d 541t"
            
            # Generate master hash
            master_hash: str = Argon2i_Hash(GlobalVars.password, GlobalVars.username, 20, 102400, 1, 64)

            # Generate app-specific hash
            App_hash: str = Argon2i_Hash(App_name, App_password, 20, 102400, 1, 64)

            # Generate final app master hash
            app_master_hash: str = Argon2i_Hash(master_hash, App_hash, 20, 102400, 1, hash_len)

            # Generate the final password
            App_key: str = generate_password(character_set, app_master_hash)

            # Log the results
            print(
                f"\nPlay:\nname:{App_name}\nemail:{App_password}\nchecks:{character_set}\n"
                f"slider:{w}\nHash length:{hash_len}\nHash:{app_master_hash}\n"
                f"App password:{App_key}"
            )

            # Update the result screen
            result_screen.ids.result_input.text = App_key

            result_screen.ids.result_message.text = f"Password generated for {item['name']}"

    def edit_item(self, index: int) -> None:
        """Navigate to the edit screen for a specific item with type checking."""
        if 0 <= index < len(self.items):
            edit_screen: EditItemScreen = self.root.get_screen('edit_item')
            edit_screen.edit_index = index
            edit_screen.on_enter()
            self.root.current = 'edit_item'

if __name__ == '__main__':
    InventoryApp().run()

