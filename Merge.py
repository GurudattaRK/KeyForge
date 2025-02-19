from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.metrics import dp
# from argon2 import low_level, Type
import base64
import platform
import pyargon2

def Argon2i_Hash(password, Salt, Time_Cost, Memory_Cost, Parallelism, hash_length):
    """
    Hashes a password using Argon2i via pyargon2.
    
    Args:
        password (str): The password to hash
        Salt (str): The salt value
        Time_Cost (int): Number of iterations
        Memory_Cost (int): Memory usage in KiB
        Parallelism (int): Number of parallel threads
        hash_length (int): Desired length of the hash in bytes
    
    Returns:
        str: Hexadecimal string representation of the hash
    """
    password_bytes = str(password)
    salt_bytes = str(Salt)
    
    # Generate the hash using pyargon2
    result = pyargon2.hash(
        password=password_bytes,
        salt=salt_bytes,
        time_cost=Time_Cost,
        memory_cost=Memory_Cost,
        parallelism=Parallelism,
        hash_len=hash_length,
        variant='i'  # Argon2i (data-independent)
    )
                                    # pyargon2.hash()
    # Get the raw hash bytes directly from the result
    # hash_bytes = result['hash']
    
    # Convert to hexadecimal string
    print("\nhash:",result)
    # hex_hash = result.hex()   
    
    return result

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
            radius: [22,]
                    
<ButtonLabel@ButtonBehavior+Label>:
    color: (0.1, 0.5, 0.8, 1)
    underline: True
    font_size: '14sp'
    size_hint: (None, None)
    size: self.texture_size
    canvas.before:
        Line:
            points: [self.x, self.y, self.right, self.y] if self.underline else []
            width: 1
                    
<MyTextInput@BoxLayout>:
    size_hint: .85, None
    height: dp(40)
    pos_hint: {'center_x': 0.5, "center_y": 0.5}
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # White background
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [22,]
        Color:
            rgba: 0.8, 0.8, 0.8, 1  # Border color
        Line:
            rounded_rectangle: [self.x, self.y, self.width, self.height, 22]
            width: 1
                                         
<WelcomeScreen>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # White background
        Rectangle:
            pos: self.pos
            size: self.size
                    
    BoxLayout:
        orientation: 'vertical'
        padding: [10, 20]
        spacing: 10
        
        Label:
            text: 'Welcome!'
            font_size: '20sp'
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(40)
            spacing: 20
            

            MyTextInput:
                TextInput:
                    id: username_input
                    hint_text: 'User ID'
                    password: False
                    background_normal: ''
                    background_active: ''
                    background_color: 0, 0, 0, 0
                    foreground_color: 0, 0, 0, 1
                    hint_text_color: 0.6, 0.6, 0.6, 1
                    size_hint_y: None
                    height: dp(40)
                    padding: [15, 10]
                    size_hint: 1, 1
                    font_size: '18sp'
                    multiline: False
                    on_focus: root.toggle_keyboard()
            
            RoundedButton:
                id: toggle_password_btn
                text: 'Hide User ID'
                size_hint_x: 0.2
                on_press: 
                    username_input.password = not username_input.password
                    self.text = 'User ID'
                
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(40)
            spacing: 20
                    
            MyTextInput:
                TextInput:
                    id: password_input
                    hint_text: 'Password'
                    password: True
                    background_normal: ''
                    background_active: ''
                    background_color: 0, 0, 0, 0
                    foreground_color: 0, 0, 0, 1
                    hint_text_color: 0.6, 0.6, 0.6, 1
                    size_hint_y: None
                    height: dp(40)
                    padding: [15, 10]
                    size_hint: 1, 1
                    font_size: '18sp'
                    multiline: False
                    on_focus: root.toggle_keyboard()
                
            RoundedButton:
                id: toggle_password_btn
                text: 'Show password'
                size_hint_x: 0.2
                on_press: 
                    password_input.password = not password_input.password
                    self.text = 'Show password'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(40)
            spacing: 100
            
            RoundedButton:
                text: 'Submit'
                on_press: root.check_password()
                    
        ButtonLabel:
            text: 'Click here to understand what is this User ID and password and how this app works'
            size_hint: (None, None)
            size: self.texture_size
            padding: [0, 0]
            pos_hint: {'center_x': 0.5}
            on_press: root.manager.current = 'login_info'

        Widget:
            id: keyboard_placeholder
            size_hint_y: None
            pos_hint: {'center_x': 0.5, "center_y": 0.5}        
            height: 10
                 

<LoginInfoScreen>:
                    
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # White background
        Rectangle:
            pos: self.pos
            size: self.size
                    
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        
        Label:
            text: 'Login Information'
            color: 0,0,0,1
            font_size: '20sp'
            
        Label:
            text: 'For security reasons:\\n- Use a strong password\\n- Don\\'t share your credentials\\n- Virtual keyboard helps prevent keyloggers'       
            color: 0,0,0,1
            halign: 'center'
        
        Button:
            text: 'Back'
            size_hint_y: None
            height: '40sp'
            on_press: root.manager.current = 'welcome'
                    
<ListScreen>:
                    
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # White background
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        
        RecycleView:
            id: rv
            viewclass: 'ItemRow'
            scroll_type: ['bars', 'content']
            color: 0,0,0,1
            
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
        color: 0,0,0,1
        size_hint_x: 0.3
        
    Label:
        text: root.email if root.email else '-'
        color: 0,0,0,1
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
                    
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # White background
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 5
        
        Label:
            text: 'Add New Item'
            color: 0,0,0,1
            font_size: '20sp'

        MyTextInput:                
            TextInput:
                id: name_input
                hint_text: 'App/Website name (required)'
                multiline: False
                size_hint_y: None
                height: dp(40)
                background_normal: ''
                background_active: ''
                background_color: 0, 0, 0, 0
                foreground_color: 0, 0, 0, 1
                hint_text_color: 0.6, 0.6, 0.6, 1
                size_hint_y: None
                height: dp(40)
                padding: [15, 10]
                size_hint: 1, 1
                font_size: '18sp'
                multiline: False
            
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(40)
            spacing: 10
            
            MyTextInput:
                TextInput:
                    id: email_input
                    hint_text: 'App/Website password (optional)'
                    password: True
                    multiline: False
                    size_hint_x: 0.8
                    background_normal: ''
                    background_active: ''
                    background_color: 0, 0, 0, 0
                    foreground_color: 0, 0, 0, 1
                    hint_text_color: 0.6, 0.6, 0.6, 1
                    size_hint_y: None
                    height: dp(40)
                    padding: [15, 10]
                    size_hint: 1, 1
                    font_size: '18sp'
                    multiline: False
            
            RoundedButton:
                id: toggle_password_btn
                text: 'Show Password'
                size_hint_x: 0.2
                on_press: 
                    email_input.password = not email_input.password
                    self.text = 'Show Password'
                    
                    
        ButtonLabel:
            text: 'click here to know more about how to use all these options'
            color: 0,0,0.8,1
            size_hint: (None, None)
            size: self.texture_size
            padding: [0, 0]
            pos_hint: {'center_x': 0.5}
            on_press: root.manager.current = 'additional_info'
        
        Label:
            text: 'Choose which characters do you want to include in your password:'
            color: 0,0,0,1
            size_hint_y: None
            height: dp(30)
                    
        GridLayout:
            cols: 2
            rows: 5
            size_hint_y: None
            height: dp(100)  # Reduced height
            spacing: [0, 5]  # No horizontal spacing
            col_default_width: root.width * 0.7  # Allocate 45% width for each column

            # Checkbox items
            Label:
                text: 'Uppercase Alphabets (Capital letters)'
                color: 0,0,0,1
                halign: 'right'
                valign: 'middle'
                text_size: self.width, None
                padding: [0, 0, 5, 0]  # Right padding only
            CheckBox:
                id: check1
                active: True
                size_hint: None, None
                size: dp(25), dp(25)
                pos_hint: {'x': 0}  # Align left in column

            Label:
                text: 'Lowercase Alphabets (Small letters)'
                color: 0,0,0,1
                halign: 'right'
                valign: 'middle'
                text_size: self.width, None
                padding: [0, 0, 5, 0]
            CheckBox:
                id: check2
                active: True
                size_hint: None, None
                size: dp(25), dp(25)
                pos_hint: {'x': 0}

            Label:
                text: 'Numbers'
                color: 0,0,0,1
                halign: 'right'
                valign: 'middle'
                text_size: self.width, None
                padding: [0, 0, 5, 0]
            CheckBox:
                id: check3
                active: True
                size_hint: None, None
                size: dp(25), dp(25)
                pos_hint: {'x': 0}

            Label:
                text: 'Special characters like ! @ # $ % ^ & * ( ) _ + - = '
                color: 0,0,0,1
                halign: 'right'
                valign: 'middle'
                text_size: self.width, None
                padding: [0, 0, 5, 0]
            CheckBox:
                id: check4
                active: True
                size_hint: None, None
                size: dp(25), dp(25)
                pos_hint: {'x': 0}

            Label:
                text: "Special characters like [ ] \\\ { } | ; ' , . / < > ? (also includes space)"
                color: 0,0,0,1
                halign: 'right'
                valign: 'middle'
                text_size: self.width, None
                padding: [0, 0, 5, 0]
            CheckBox:
                id: check5
                active: True
                size_hint: None, None
                size: dp(25), dp(25)
                pos_hint: {'x': 0}

        Widget:
            size_hint_y: None
            height: dp(80)  # Space between last checkbox and slider

        BoxLayout:
            orientation: 'vertical'
            size_hint: 0.9, None
            height: dp(50)
            pos_hint: {'center_x': 0.5}
            spacing: dp(15)
                    
            Label:
                text: "Set the length of your password on this slider"
                color: 0,0,0,1
                size_hint_y: None
                height: dp(20)
                halign: 'center'

                
            Slider:
                id: slider
                min: 1
                max: 4
                step: 1
                value: root.slider_value  # Two-way binding
                on_value: root.slider_value = int(self.value)  # Update property
                canvas:
                    Color:
                        rgba: 0.8, 0.8, 0.8, 1  # Light gray background track
                    Rectangle:
                        pos: self.x, self.center_y - dp(2)
                        size: self.width, dp(4)
                    
                    Color:
                        rgba: 0, 0, 0, 1  # Black progress bar
                    Rectangle:
                        pos: self.x, self.center_y - dp(2)
                        size: self.value_pos[0] - self.x, dp(4)

        Label:
            text: f'Password Length: {2**(int(root.slider_value))*(8)}'
            color: 0,0,0,1
            size_hint_y: None
            height: dp(20)
            halign: 'center'
                    
        Widget:
            size_hint_y: None
            height: dp(80)  # Space between last slider and button

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(40)
            spacing: 500

            RoundedButton:
                text: 'Add Item'
                on_press: root.add_item()
                        
            RoundedButton:
                text: 'Back'
                size_hint_y: None
                height: '40sp'
                on_press: root.manager.current = 'list'

<EditItemScreen>:
                    
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # White background
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        
        Label:
            text: 'Edit Item'
            color: 0,0,0,1
            font_size: '20sp'
            
        MyTextInput:                
            TextInput:
                id: name_input
                hint_text: 'App/Website name (required)'
                multiline: False
                size_hint_y: None
                height: dp(40)
                background_normal: ''
                background_active: ''
                background_color: 0, 0, 0, 0
                foreground_color: 0, 0, 0, 1
                hint_text_color: 0.6, 0.6, 0.6, 1
                size_hint_y: None
                height: dp(40)
                padding: [15, 10]
                size_hint: 1, 1
                font_size: '18sp'
                multiline: False
            
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(40)
            spacing: 10
            
            MyTextInput:
                TextInput:
                    id: email_input
                    hint_text: 'App/Website password (optional)'
                    password: True
                    multiline: False
                    size_hint_x: 0.8
                    background_normal: ''
                    background_active: ''
                    background_color: 0, 0, 0, 0
                    foreground_color: 0, 0, 0, 1
                    hint_text_color: 0.6, 0.6, 0.6, 1
                    size_hint_y: None
                    height: dp(40)
                    padding: [15, 10]
                    size_hint: 1, 1
                    font_size: '18sp'
                    multiline: False
            
            RoundedButton:
                id: toggle_password_btn
                text: 'Show Password'
                size_hint_x: 0.2
                on_press: 
                    email_input.password = not email_input.password
                    self.text = 'Show Password'
                    
        ButtonLabel:
            text: 'click here to know more about how to use all these options'
            color: 0,0,0.8,1
            size_hint: (None, None)
            size: self.texture_size
            padding: [0, 0]
            pos_hint: {'center_x': 0.5}
            on_press: root.manager.current = 'additional_info'
        
        Label:
            text: 'Choose which characters do you want to include in your password:'
            color: 0,0,0,1
            size_hint_y: None
            height: dp(30)
                    
        GridLayout:
            cols: 2
            rows: 5
            size_hint_y: None
            height: dp(100)  # Reduced height
            spacing: [0, 5]  # No horizontal spacing
            col_default_width: root.width * 0.7  # Allocate 45% width for each column

            # Checkbox items
            Label:
                text: 'Uppercase Alphabets (Capital letters)'
                color: 0,0,0,1
                halign: 'right'
                valign: 'middle'
                text_size: self.width, None
                padding: [0, 0, 5, 0]  # Right padding only
            CheckBox:
                id: check1
                active: True
                size_hint: None, None
                size: dp(25), dp(25)
                pos_hint: {'x': 0}  # Align left in column

            Label:
                text: 'Lowercase Alphabets (Small letters)'
                color: 0,0,0,1
                halign: 'right'
                valign: 'middle'
                text_size: self.width, None
                padding: [0, 0, 5, 0]
            CheckBox:
                id: check2
                active: True
                size_hint: None, None
                size: dp(25), dp(25)
                pos_hint: {'x': 0}

            Label:
                text: 'Numbers'
                color: 0,0,0,1
                halign: 'right'
                valign: 'middle'
                text_size: self.width, None
                padding: [0, 0, 5, 0]
            CheckBox:
                id: check3
                active: True
                size_hint: None, None
                size: dp(25), dp(25)
                pos_hint: {'x': 0}

            Label:
                text: 'Special characters like ! @ # $ % ^ & * ( ) _ + - = '
                color: 0,0,0,1
                halign: 'right'
                valign: 'middle'
                text_size: self.width, None
                padding: [0, 0, 5, 0]
            CheckBox:
                id: check4
                active: True
                size_hint: None, None
                size: dp(25), dp(25)
                pos_hint: {'x': 0}

            Label:
                text: "Special characters like [ ] \\\ { } | ; ' , . / < > ? (also includes space)"
                color: 0,0,0,1
                halign: 'right'
                valign: 'middle'
                text_size: self.width, None
                padding: [0, 0, 5, 0]
            CheckBox:
                id: check5
                active: True
                size_hint: None, None
                size: dp(25), dp(25)
                pos_hint: {'x': 0}

        Widget:
            size_hint_y: None
            height: dp(80)  # Space between last checkbox and slider

        BoxLayout:
            orientation: 'vertical'
            size_hint: 0.9, None
            height: dp(50)
            pos_hint: {'center_x': 0.5}
            spacing: dp(15)
                    
            Label:
                text: "Set the length of your password on this slider"
                color: 0,0,0,1
                size_hint_y: None
                height: dp(20)
                halign: 'center'

                
            Slider:
                id: slider
                min: 1
                max: 4
                step: 1
                value: root.slider_value  # Two-way binding
                on_value: root.slider_value = int(self.value)  # Update property
                canvas:
                    Color:
                        rgba: 0.8, 0.8, 0.8, 1  # Light gray background track
                    Rectangle:
                        pos: self.x, self.center_y - dp(2)
                        size: self.width, dp(4)
                    
                    Color:
                        rgba: 0, 0, 0, 1  # Black progress bar
                    Rectangle:
                        pos: self.x, self.center_y - dp(2)
                        size: self.value_pos[0] - self.x, dp(4)

        Label:
            text: f'Password Length: {2**(int(root.slider_value))*(8)}'
            color: 0,0,0,1
            size_hint_y: None
            height: dp(20)
            halign: 'center'
                    
        Widget:
            size_hint_y: None
            height: dp(80)  # Space between last slider and button

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(40)
            spacing: 500

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
                    
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # White background
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
                    
        Label:
            id: result_message
            text: 'Generating password....'
            color: 0,0,0,1
            font_size: '20sp'
                    
        MyTextInput:                
            TextInput:
                id: result_input
                text: ''
                password: True
                readonly: True
                multiline: False
                size_hint_y: None
                height: '40sp'
                background_normal: ''
                background_active: ''
                background_color: 0, 0, 0, 0
                foreground_color: 0, 0, 0, 1
                hint_text_color: 0.6, 0.6, 0.6, 1
                size_hint_y: None
                height: dp(40)
                padding: [15, 10]
                size_hint: 1, 1
                font_size: '18sp'
                multiline: False
                    
        BoxLayout:
            orientation: 'horizontal'
            padding: 20
            spacing: 10
            
            RoundedButton:
                id: toggle_result_password_btn
                text: 'Show Password'
                size_hint_x: 0.2
                on_press: 
                    result_input.password = not result_input.password
                    self.text = 'Show Password'
                        
            RoundedButton:
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
            GlobalVars.username = Argon2i_Hash(GlobalVars.username,"H4!?|](hb)",4,10,1,16)
            print(f"\nLogin:\nname:{GlobalVars.username}\npassword:{GlobalVars.password}")


    
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
        self.ids.email_input.text = ''

    def add_item(self):
        name = self.ids.name_input.text.strip()
        if not name:
            return
        
        email = self.ids.email_input.text.strip()
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
        self.ids.email_input.text = ''
        self.manager.current = 'list'

class EditItemScreen(Screen):
    edit_index = NumericProperty(-1)
    slider_value = NumericProperty(2)
    
    def on_enter(self):
        app = App.get_running_app()
        if 0 <= self.edit_index < len(app.items):
            item = app.items[self.edit_index]
            self.ids.name_input.text = item['name']
            self.ids.email_input.text = item.get('email', '')
            
            # Set checkbox states
            for i in range(5):
                self.ids[f'check{i+1}'].active = item.get('checks', [True, True, True, True, True])[i]

            self.slider_value = item.get('slider_value', 2)
    
    def save_item(self):
        name = self.ids.name_input.text.strip()
        if not name:
            return
        
        email = self.ids.email_input.text.strip()
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
                
        if system == 'Linux':
            Clipboard.copy(text)


        try:
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
        result_screen.ids.result_message.text = f"Copied password is deleted & Clipboard cleared"
        print("\nclipboard data:", Clipboard.get())
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

class InventoryApp(App):
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
                App_password = Argon2i_Hash(App_password,tmp_salt,1,1024,1,64)

            
            master_hash = Argon2i_Hash(GlobalVars.password,GlobalVars.username,20,102400,1,64)

            App_hash = Argon2i_Hash(App_name,App_password,20,102400,1,64)

            app_master_hash = Argon2i_Hash(master_hash,App_hash,20,102400,1,hash_len)

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
    InventoryApp().run()