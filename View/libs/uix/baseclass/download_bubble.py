from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivymd.uix.label import MDLabel

Builder.load_string(
    """
<DownloadBubble>
    adaptive_height: True
    padding: [dp(8), dp(8)]
    text_color: 1, 1, 1, 1
    text_size: self.width, None

    canvas.before:
        Color:
            rgba: self.theme_cls.primary_dark
        RoundedRectangle:
            id: rect
            size: self.size
            pos: self.pos
            radius:
                [(dp(-5), dp(5)), dp(8), dp(8), dp(8)]
        
        MDIconButton:
        icon: "download"
        ripple_scale: .5
        pos_hint: {"center_y": .5}
        pos: rect.width - self.width + dp(20), 0
        on_release: app.root.download("hey")
"""
)


class DownloadBubble(MDLabel):
    # send_by_user = BooleanProperty()
    pass
