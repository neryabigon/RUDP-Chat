from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivymd.uix.list import OneLineAvatarIconListItem

Builder.load_string(
    """
<UserListItem>
    on_release: print("nerya")
    text: 'nerya'
    IconRightWidget:
        icon: "face-profile"
    Widget:
        size_hint: None, None
        size: dp(10), dp(10)
        pos_hint: {"center_x": .835, "center_y": .38}
        canvas.before:
            Color:
                rgba:
                    (0, 1, 0, .7) if root.online \
                    else (0, 0, 0, 0)
            Ellipse:
                size: self.size
                pos: self.pos
                
    """
)


class UserListItem(OneLineAvatarIconListItem):
    online = BooleanProperty()
