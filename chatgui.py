from tkinter import *


BG_GRAY = '#DC143C'
BG_COLOR = '#EEC591'
TEXT_COLOR = '#EAECEE'


FONT = 'Helvetica 14'
FONT_BOLD = 'Helvetica 13 bold'

class ChatApp:
    def __init__(self):
        self.window = Tk()
        self._setup_win()

    def run(self):
        self.window.mainloop()


    def _setup_win(self):
        self.window.title("Chatbot assistant")
        self.window.resizable(width=True, height=True)
        self.window.configure(width='470', height='550', bg = BG_COLOR)

if __name__ == '__main__':
    app = ChatApp()
    app.run()