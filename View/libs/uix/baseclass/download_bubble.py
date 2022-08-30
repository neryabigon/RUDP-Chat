from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineAvatarIconListItem

Builder.load_string(
    """
<DownloadBubble>
    text: "file name"
    IconRightWidget:
        icon: "download"
        on_release: app.root.download("hey")
    Widget:
        size_hint: None, None
        size: dp(10), dp(10)
        pos_hint: {"center_x": .835, "center_y": .38}
"""
)


class DownloadBubble(OneLineAvatarIconListItem):
    downloading = BooleanProperty()
    pass
