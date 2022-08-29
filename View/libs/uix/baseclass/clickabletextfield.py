from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout

Builder.load_string('''
<ClickableTextFieldRound>:
    size_hint_y: None
    height: field.height

    MDTextFieldRound:
        id: field
        hint_text: "Write your message"
        on_text_validate: app.root.send(field.text)
        color_active: app.theme_cls.primary_light
        padding:
            self._lbl_icon_left.texture_size[1] + dp(10) if self.icon_left else dp(15), (self.height / 2) - (self.line_height / 2), self._lbl_icon_right.texture_size[1] + dp(20), 0

    MDIconButton:
        icon: "send"
        ripple_scale: .5
        pos_hint: {"center_y": .5}
        pos: field.width - self.width + dp(20), 0
        on_release: app.root.send(field.text)
        
    
    MDIconButton:
        id: fileButton
        icon: "file-download-outline"
        ripple_scale: .5
        pos_hint: {"center_y": .5}
        pos: field.width - self.width + dp(60), 0
        disabled: self.parent.disabled
        opacity: self.parent.opacity
        on_release: app.root.choose()
''')


class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    # Here specify the required parameters for MDTextFieldRound:
    # [...]
