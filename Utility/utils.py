import os

from kivy.lang import Builder

"""
Utility functions
"""

def load_kv(file_name, file_path=os.path.join("View","libs", "uix", "kv")):
    """
    `load_kv` func is used to load a .kv file.
    args that you can pass:
        * `file_name`: Name of the kv file.
        * `file_path`: Path to the kv file, it defaults
                       to `project_name/libs/kv`.

    Q: Why a custom `load_kv`?
    A: To avoid some encoding errors.
    """
    with open(os.path.join(file_path, file_name), encoding="utf-8") as kv:
        Builder.load_string(kv.read())


def deconstruct_msg(msg):
    splited_msg = msg.split("|")
    return splited_msg
