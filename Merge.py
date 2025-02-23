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
from kivy.core.window import Window
from kivy.properties import ColorProperty
from kivy.uix.label import Label
from kivy.metrics import dp
# from argon2 import low_level, Type
import base64
import platform
import hashlib
from kivy.core.text import LabelBase

LabelBase.register(name="Roboto", fn_regular="JetBrainsMono-Medium.ttf")

Builder.load_string('''
                    
<RoundedButton>:
    background_color: 0, 0, 0, 0
    background_normal: ""
    canvas.before:
        Color:
            rgba: self.normal_color if self.state in ('normal', '') else self.pressed_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [20]
                    
<ButtonLabel@ButtonBehavior+Label>:
    color: (0.1, 0.5, 0.8, 1)
    underline: True
    font_size: '14sp'
    size_hint: (None, None)
    size: self.texture_size
    halign: 'center'

    text_size: 300, None
    size_hint_y: None
    height: self.texture_size[1]
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
    # White background
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Use AnchorLayout to center everything
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'

        # This BoxLayout is your centered content
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(20)
            padding: [dp(20), dp(20)]
            size_hint: 0.9, None
            height: self.minimum_height

            # A welcome label at the top
            Label:
                text: 'Welcome!'
                font_size: '24sp'
                color: 0, 0, 0, 1
                halign: 'center'
                size_hint_y: None
                height: dp(40)

            # Row for User ID
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
                    id: toggle_userid_btn
                    text: 'Hide User ID'
                    size_hint_x: 0.22
                    on_press:
                        username_input.password = not username_input.password
                        self.text = 'Show User ID' if username_input.password else 'Hide User ID'

            # Row for Password
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
                    size_hint_x: 0.22
                    on_press:
                        password_input.password = not password_input.password
                        self.text = 'Show password' if password_input.password else 'Hide password'

            # Row for the Submit button
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(40)
                spacing: 100

                RoundedButton:
                    text: 'Submit'
                    size_hint_x: 0
                    on_press: root.check_password()
                    pos_hint: {'center_x': 0}

            Widget:
                size_hint_y: None
                height: dp(80)  # Space between last checkbox and slider

            # Link / Info
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
            halign: 'center'
            valign: 'top'
            
        Label:
            text: ( 'User ID:\\n User ID can be anything that is unique to only you. It can be your phone number, any unique government identification number, birthday etc. Primary role of this User ID is to help generate passwords and keys that unique to you as two or more people may set same login password and as a result it may lead to app generating same password for your apps & websites.You are free to set a User ID that is not unique and easy to as long as you keep you login password a secret.\\n \\nPassword:\\n This login password is the main key to protecting & generating all your other passwords & keys for your apps & websites.\\n\\nHiding your input:\\n the "User ID" & "Hide password" buttons hide or unhide the password & user ID you are typing to prevent it from reaching any spying eyes. As mentioned before User ID and password can be anything hence they can be same too,so , to protect your password from leaking you can hide password & user ID while typing. Optionally, you can choose type using the virtual keyboard that pops up to prevent any keyloggers from stealing your data(virtual keyboard might not be supported on mobile devices)' )      
            color: 0,0,0,1
            font_size: '14sp'        # adjust as needed
            halign: 'center'
            valign: 'top'
            # --- Key wrapping properties ---
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1]

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
        padding: 50
        
        RecycleView:
            id: rv
            viewclass: 'ItemRow'
            scroll_type: ['bars', 'content']
            color: 0,0,0,1
            
            RecycleBoxLayout:
                orientation: 'vertical'
                default_size: None, dp(50)
                default_size_hint: 1, None
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
        
        BoxLayout:
            size_hint_y: None
            height: '40sp'
            spacing: 5
            
            RoundedButton:
                text: 'Add New Item'
                pos_hint: {'x': 0, 'y':0.5}
                on_press: root.manager.current = 'add_item'
                radius: [2,]
            
            RoundedButton:
                text: 'Logout'
                normal_color: (0.7, 0.2, 0, 1)
                pressed_color: (0.4, 0.1, 0, 1)
                pos_hint: {'x': 1, 'y':0.5}
                on_press: app.logout()
                radius: [2,]


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
    
    RoundedButton:
        text: 'Generate'
        normal_color: (0, 0.8, 0.4, 1)
        pressed_color: (0, 0.6, 0.3, 1) 
        size_hint_x: 0.15
        on_press: app.play_item(root.index)
        radius: [3]
        
    RoundedButton:
        text: 'Edit'
        normal_color: (0, 0.8, 0.8, 1)
        pressed_color: (0, 0.4, 0.4, 1) 
        size_hint_x: 0.15
        on_press: app.edit_item(root.index)
        radius: [3]
    
    RoundedButton:
        text: 'Delete'
        normal_color: (0.8, 0.3, 0, 1)
        pressed_color: (0.4, 0.1, 0, 1)
        size_hint_x: 0.15
        on_press: app.delete_item(root.index)
        radius: [3]

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
            size_hint_x:0.22 
            size_hint_y:0.4
            text: 'Show Password'
            pos_hint: {'center_x': 0.5}
            radius : [20]
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
            text: 'Choose which sets of characters do you want to include in your password:'
            color: 0,0,0,1
            height: dp(30)
            halign: 'center'
            
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1]

        Widget:
            size_hint_y: None
            height: dp(80)  # Space between last checkbox and slider
                    
        AnchorLayout:
            anchor_x: 'center'
            # anchor_y: 'center'

            GridLayout:
                cols: 2
                rows: 5
                spacing: dp(10)
                # The key: let the grid expand horizontally
                size_hint: (0.8, None)
                height: self.minimum_height

                # 1st row
                CheckBox:
                    id: check1
                    active: True
                    size_hint: None, None
                    size: dp(25), dp(25)
                Label:
                    text: 'Uppercase Alphabets (Capital letters)'
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    # Let the label wrap if needed
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

                # 2nd row
                CheckBox:
                    id: check2
                    active: True
                    size_hint: None, None
                    size: dp(25), dp(25)
                Label:
                    text: 'Lowercase Alphabets (Small letters)'
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

                # 3rd row
                CheckBox:
                    id: check3
                    active: True
                    size_hint: None, None
                    size: dp(25), dp(25)
                Label:
                    text: 'Numbers'
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

                # 4th row
                CheckBox:
                    id: check4
                    active: True
                    size_hint: None, None
                    size: dp(25), dp(25)
                Label:
                    text: '! @ # $ % ^ & * ( ) _ + - = '
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

                # 5th row
                CheckBox:
                    id: check5
                    active: True
                    size_hint: None, None
                    size: dp(25), dp(25)
                Label:
                    text: "(including space) [ ] \\\ { } | ; ' , . / < > ?"
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

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
            spacing: 100

            RoundedButton:
                pos_hint: {'x': 0}
                text: 'Add Item'
                on_press: root.add_item()
                        
            RoundedButton:
                text: 'Back'
                size_hint_y: None
                pos_hint: {'x': 1}
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
            size_hint_x:0.22 
            size_hint_y:0.4
            text: 'Show Password'
            pos_hint: {'center_x': 0.5}
            radius : [20]
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
            text: 'Choose which sets of characters do you want to include in your password:'
            color: 0,0,0,1
            height: dp(30)
            halign: 'center'
            
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1]

        Widget:
            size_hint_y: None
            height: dp(80)  # Space between last checkbox and slider
                    
        AnchorLayout:
            anchor_x: 'center'
            # anchor_y: 'center'

            GridLayout:
                cols: 2
                rows: 5
                spacing: dp(10)
                # The key: let the grid expand horizontally
                size_hint: (0.8, None)
                height: self.minimum_height

                # 1st row
                CheckBox:
                    id: check1
                    active: True
                    size_hint: None, None
                    size: dp(25), dp(25)
                Label:
                    text: 'Uppercase Alphabets (Capital letters)'
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    # Let the label wrap if needed
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

                # 2nd row
                CheckBox:
                    id: check2
                    active: True
                    size_hint: None, None
                    size: dp(25), dp(25)
                Label:
                    text: 'Lowercase Alphabets (Small letters)'
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

                # 3rd row
                CheckBox:
                    id: check3
                    active: True
                    size_hint: None, None
                    size: dp(25), dp(25)
                Label:
                    text: 'Numbers'
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

                # 4th row
                CheckBox:
                    id: check4
                    active: True
                    size_hint: None, None
                    size: dp(25), dp(25)
                Label:
                    text: '! @ # $ % ^ & * ( ) _ + - = '
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

                # 5th row
                CheckBox:
                    id: check5
                    active: True
                    size_hint: None, None
                    size: dp(25), dp(25)
                Label:
                    text: "(including space) [ ] \\\ { } | ; ' , . / < > ?"
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]

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
            spacing: 100

            RoundedButton:
                pos_hint: {'x': 0}
                text: 'Save Changes'
                on_press: root.save_item()
                        
            RoundedButton:
                text: 'Back'
                size_hint_y: None
                pos_hint: {'x': 1}
                height: '40sp'
                on_press: root.manager.current = 'list'

<AdditionalInfoScreen>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # White background
        Rectangle:
            pos: self.pos
            size: self.size

    ScrollView:
        size_hint: (1, 1)
        do_scroll_x: False
        do_scroll_y: True
        bar_width: dp(10)  # Makes scrollbar more visible
        
        GridLayout:
            cols: 1
            size_hint_y: None  # Critical for scrolling
            height: self.minimum_height  # Expands to contain children
            padding: dp(20)
            spacing: dp(10)

            Label:
                text: 'Additional Information'
                font_size: '20sp'
                size_hint_y: None
                height: self.texture_size[1]

            Label:
                text: ("App/Website name:\\nEnter the App or Website name that you want the password for, this can be anything as long as you remember it. It is case sensitive so make sure you don't mistype any characters. If you have multiple account on same website/App you can generate unique password seperately for all of those just make sure you either give them unique 'App/Website name' or Unique 'App/Website password'.\\n Here are some example about how you can you can manage multiple accounts of same app/website:\\n Lets say you have two accounts on Google, User1 and User2. To get passwords for each account you can type 'google-user1' and this will generate password for user1. You can make any combination that easy to remember for you like- google1,user1-google, googleuser1 etc. You can set same password in 'App/website password' for all accounts, just make sure you remember it or you leave password empty.\\n\\nApp/website password:\\nThis field is optional as the whole purpose of KeyForge is that you don't have to remember passwords for all apps but this option is provided if you want to add more security. Also, this option can be used to add uniqueness to your generated passwords.\\nFor example: if your somehow your login User ID & password is same as someone else or if they get leaked the App/website password can still protect your passwords because it makes your password unique. Also you can have same App/Website name and different App/Website passwords which will generate different password that you can use for different accounts on same App/Website, like:\\nApp/Website: Google\\nApp/Website password: google-user1\\n this will give unique password for user1 on google\\n\\nChoosing which characters to include in your generated password:\\nBy default all 5 options(5 character sets) are selected but you can unselect the options or edit them later. Before generating any password for any App/Website check what kind of characters do they accept and according to their rules you can choose in KeyForge which characters you want in your generate password/key.\\n\\nPassword Length:By default length of password is set to 32 characters but you can choose between 4 options: 16, 32, 64, 128. Before generating any password for any App/Website check what is the maximum length of passwords do they accept & according to their rules you can set the length of your generate password/key.\\n Remember that longer passwords with more variety of character sets are harder to crack hence more safer.")      
                color: 0,0,0,1
                font_size: '14sp'        # adjust as needed
                halign: 'center'
                valign: 'top'
                # --- Key wrapping properties ---
                text_size: self.width, None
                size_hint_y: None
                height: self.texture_size[1]
            
            RoundedButton:
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

    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'

        BoxLayout:
            orientation: 'vertical'
            padding: 20
            # Lower or remove the spacing here:
            spacing: 10

            Label:
                id: result_message
                text: 'Generating password....'
                halign: 'center'
                color: 0,0,0,1
                font_size: '20sp'
                text_size: self.width, None
                size_hint_y: None
                height: self.texture_size[1]

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

            # Horizontal box with the two buttons
            BoxLayout:
                orientation: 'horizontal'
                # Remove or reduce padding here to remove extra space
                # e.g. keep horizontal padding but remove top/bottom:
                padding: [20, 0, 20, 0]
                spacing: 100

                RoundedButton:
                    id: toggle_result_password_btn
                    text: 'Show Password'
                    size_hint_y: None
                    size_hint_x: 0.2
                    height: '40sp'
                    on_press:
                        result_input.password = not result_input.password
                        self.text = 'Show Password'

                RoundedButton:
                    text: 'Copy to Clipboard'
                    normal_color: (0.8, 0.3, 0, 1)
                    pressed_color: (0.4, 0.1, 0, 1)
                    size_hint_y: None
                    size_hint_x: 0.2
                    height: '40sp'
                    on_press: root.copy_to_clipboard()

            RoundedButton:
                text: 'Back to List'
                pos_hint: {'y': 0.1}
                size_hint_y: None
                height: '40sp'
                on_press: root.manager.current = 'list'
''')


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
    info = platform.uname()   
    if (info.system != 'ios') and (info.system != 'android'):
        Window.size = (800, 750)

    KeyForge().run()