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
            hint_text: 'Name (required)'
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
                hint_text: 'Email (optional)'
                multiline: False
                size_hint_x: 0.8
                
            RoundedButton:
                text: 'Know More'
                size_hint_x: 0.2
                on_press: root.manager.current = 'additional_info'
        
        Label:
            text: 'Choose customization'
            size_hint_y: None
            height: dp(30)
        
        GridLayout:
            cols: 2
            rows: 4
            size_hint_y: None
            height: dp(80)
            
            CheckBox:
                id: check1
                active: True
            Label:
                text: 'Option 1'
            
            CheckBox:
                id: check2
                active: True
            Label:
                text: 'Option 2'
            
            CheckBox:
                id: check3
                active: True
            Label:
                text: 'Option 3'
            
            CheckBox:
                id: check4
                active: True
            Label:
                text: 'Option 4'
        
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
                min: 1
                max: 4
                step: 1
                value: 2
                value_normalized: (self.value - self.min) / (self.max - self.min)
                on_value: root.slider_value = int(self.value)
        
        RoundedButton:
            text: 'Add Item'
            on_press: root.add_item()

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
            hint_text: 'Name (required)'
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
                hint_text: 'Email (optional)'
                multiline: False
                size_hint_x: 0.8
                
            RoundedButton:
                text: 'Know More'
                size_hint_x: 0.2
                on_press: root.manager.current = 'additional_info'
        
        Label:
            text: 'Choose customization'
            size_hint_y: None
            height: dp(30)
        
        GridLayout:
            cols: 2
            rows: 4
            size_hint_y: None
            height: dp(80)
            
            CheckBox:
                id: check1
            Label:
                text: 'Option 1'
            
            CheckBox:
                id: check2
            Label:
                text: 'Option 2'
            
            CheckBox:
                id: check3
            Label:
                text: 'Option 3'
            
            CheckBox:
                id: check4
            Label:
                text: 'Option 4'
        
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(60)
            spacing: 5
            
            Label:
                text: f'Priority Level: {root.slider_value}'
                size_hint_y: None
                height: dp(20)
                
            Slider:
                min: 1
                max: 4
                step: 1
                value: root.slider_value
                value_normalized: (self.value - self.min) / (self.max - self.min)
                on_value: root.slider_value = int(self.value)
        
        RoundedButton:
            text: 'Save Changes'
            on_press: root.save_item()

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
            # Handle regular keys
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

class LoginInfoScreen(Screen):
    pass

class ListScreen(Screen):
    def on_enter(self):
        self.ids.rv.data = [
            {'name': item['name'], 'email': item.get('email', ''), 'index': i}
            for i, item in enumerate(App.get_running_app().items)
        ]

class AddItemScreen(Screen):
    def on_enter(self):
        # Reset checkboxes to True when the screen is opened
        self.ids.check1.active = True
        self.ids.check2.active = True
        self.ids.check3.active = True
        self.ids.check4.active = True

    def add_item(self):
        name = self.ids.name_input.text.strip()
        if not name:
            return
        
        email = self.ids.email_input.text.strip()
        checks = [
            self.ids.check1.active,
            self.ids.check2.active,
            self.ids.check3.active,
            self.ids.check4.active
        ]
        
        # Add new item with checks
        App.get_running_app().items.append({
            'name': name,
            'email': email,
            'checks': checks
        })
        
        # Clear input fields
        self.ids.name_input.text = ''
        self.ids.email_input.text = ''
        self.manager.current = 'list'

class EditItemScreen(Screen):
    edit_index = NumericProperty(-1)
    
    def on_enter(self):
        app = App.get_running_app()
        if 0 <= self.edit_index < len(app.items):
            item = app.items[self.edit_index]
            self.ids.name_input.text = item['name']
            self.ids.email_input.text = item.get('email', '')
            
            # Set checkbox states
            for i in range(4):
                self.ids[f'check{i+1}'].active = item.get('checks', [True, True, True, True])[i]
    
    def save_item(self):
        name = self.ids.name_input.text.strip()
        if not name:
            return
        
        email = self.ids.email_input.text.strip()
        checks = [
            self.ids.check1.active,
            self.ids.check2.active,
            self.ids.check3.active,
            self.ids.check4.active
        ]
        
        app = App.get_running_app()
        if 0 <= self.edit_index < len(app.items):
            app.items[self.edit_index] = {
                'name': name,
                'email': email,
                'checks': checks
            }
            self.manager.current = 'list'

class AdditionalInfoScreen(Screen):
    pass

class ResultScreen(Screen):
    def copy_to_clipboard(self):
        text = self.ids.result_input.text
        Clipboard.put(text)
        Clock.schedule_once(lambda dt: self.clear_clipboard(), 5)

    def clear_clipboard(self):
        Clipboard.put('')
        print("Clipboard content erased after 5 seconds")

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
        sm.add_widget(UsernameExplanationScreen(name='username_explanation'))
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
        if 0 <= index < len(self.items):
            item = self.items[index]
            result = f"{item['name']}{item.get('email', '')}"
            result_screen = self.root.get_screen('result')
            result_screen.ids.result_input.text = result
            self.root.current = 'result'

    def edit_item(self, index):
        if 0 <= index < len(self.items):
            edit_screen = self.root.get_screen('edit_item')
            edit_screen.edit_index = index
            edit_screen.on_enter()
            self.root.current = 'edit_item'

if __name__ == '__main__':
    InventoryApp().run()