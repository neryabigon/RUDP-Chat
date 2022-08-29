from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivymd.uix.label import MDLabel

Builder.load_string(
    """
<ChatBubble>
    adaptive_height: True
    padding: [dp(8), dp(8)]
    text_color: 1, 1, 1, 1
    text_size: self.width, None

    canvas.before:
        Color:
            rgba:
                self.theme_cls.primary_dark if self.send_by_user \
                else self.theme_cls.primary_color
        RoundedRectangle:
            id: rect
            size: self.size
            pos: self.pos
            radius:
                [dp(8), dp(8), (dp(-5), dp(5)), dp(8)] if self.send_by_user \
                else [(dp(-5), dp(5)), dp(8), dp(8), dp(8)]
                
    MDIconButton:
        id: downloadButton
        icon: "download"
        pos_hint: {"center_y": .5}
        pos: root.width - self.width + dp(10), 0
        on_release: app.root.download("hey")
        # disabled: app.root.get_screen('chat').chat_logs[2]["REGULAR"]
        # opacity: 0 if app.root.get_screen('chat').chat_logs[2]["REGULAR"] else 1
        
"""
)


class ChatBubble(MDLabel):
    send_by_user = BooleanProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        REGULAR = BooleanProperty()
