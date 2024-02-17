from PyQt5.QtWidgets import QVBoxLayout
from .message_dialog import MessageDialog

class Dialog(MessageDialog):
    def __init__(self, title: str, content: str, parent):
        super().__init__(title, content, parent)
        