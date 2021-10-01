from datetime import datetime
from tkinter import *
import textwrap
from PIL import ImageTk, Image
from bot import Bot

# Pour les couleurs de polices, background, etc..
BG_GRAY = '#ABB2B9'
BG_COLOR = '#CDCCCC'
TEXT_COLOR = '#000000'
# FONT = 'Helvetica 14'
FONT_BOLD = 'Helvetica 10 bold'

fenetre_chat = Tk()
fenetre_chat.title("Chatbot")
fenetre_chat.geometry("400x500")
fenetre_chat.configure(bg=BG_COLOR)
fenetre_chat.resizable(width=FALSE, height=FALSE)

# Boutons pour quitter la fenêtre (quit)
# About us on pourra rajouter une création de fenêtre avec écris développé par ... 
main_menu = Menu(fenetre_chat)
main_menu.add_command(label="About us")
main_menu.add_command(label="Quit", command=fenetre_chat.destroy)
fenetre_chat.config(menu=main_menu)

now = datetime.now()
current_time = now.strftime("%D - %H:%M \n")



def send(event): # Ce qui se passe quand on appuie sur entrée pour envoyer le msg
    getmsg = EntryBox.get("1.0", 'end-1c').strip()
    msg = textwrap.fill(getmsg,30)
    EntryBox.delete("0.0", END)

    if msg != '':
        Dialog.config(state=NORMAL)
        Dialog.insert(END, current_time, ("small","right","colour"))
        Dialog.insert(END,msg + '\n\n',("right"))

        Dialog.config(foreground=TEXT_COLOR, font=FONT_BOLD)

        res = bob.treat_message(msg)
        Dialog.insert(END, current_time, ("small", "colour"))
        Dialog.insert(END,textwrap.fill(res,30)+'\n\n')

        Dialog.config(state=DISABLED)
        Dialog.yview(END)


def bouton_envoi(): # Si on envoie le message en cliquant sur le bouton d'envoi au lieu d'appuie sur entrer
    getmsg = EntryBox.get("1.0", 'end-1c').strip()
    msg = textwrap.fill(getmsg,30)
    EntryBox.delete("0.0", END)

    if msg != '':
        Dialog.config(state=NORMAL)
        Dialog.insert(END, current_time, ("small","right","colour"))
        Dialog.insert(END,msg + '\n\n',("right"))

        Dialog.config(foreground="white", font=FONT_BOLD)

        res = bob.treat_message(msg)
        Dialog.insert(END, current_time, ("small", "colour"))
        Dialog.insert(END,textwrap.fill(res,30)+'\n\n')

        Dialog.config(state=DISABLED)
        Dialog.yview(END)


# Fenêtre de dialogue avec le bot
Dialog = Text(fenetre_chat, bd=0, height="8", width="50", font=FONT_BOLD, wrap="word", bg=BG_COLOR)
Dialog.config(state=NORMAL)
Dialog.tag_config("right", justify="right")
Dialog.tag_config("small", font=FONT_BOLD)
Dialog.tag_config("colour", foreground="#333333")
Dialog.insert(END, current_time, ("small","colour"))
Dialog.insert(END,textwrap.fill("Le bot commence par \"Hello what can I do for you\" ?",30))
Dialog.insert(END,'\n')
Dialog.config(foreground=TEXT_COLOR, font=FONT_BOLD)
Dialog.config(state=DISABLED)

# Barre sur le côté pour défiler la conversation
scrollbar = Scrollbar(fenetre_chat, command=Dialog.yview, cursor="double_arrow")
Dialog['yscrollcommand'] = scrollbar.set

# Bouton pour envoyer un message au bot
img = Image.open("send.png")  # On resize l'image avant de l'intégrer au bouton
img = img.resize((50, 48), Image.ANTIALIAS)
loadimage = ImageTk.PhotoImage(img)
SendButton = Button(fenetre_chat, image=loadimage, command=bouton_envoi)
SendButton["bg"] = "white"
SendButton["border"] = "0"
SendButton.pack()

# SendButton = Button(fenetre_chat, font=("Arial", 12, 'bold'), text="Send", width="8", height=5,
#                     bd=0, fg="#750216", activebackground="#AAAAAA", bg="#999999", command=bouton_envoi)

# Pour l'envoi d'un message
EntryBox = Text(fenetre_chat, bd=0, fg="#000000", bg="#fff5f5", highlightcolor="#750216",
                width="18", height="5", font=("Arial",10), wrap="word")

# Placement des composantes (entrée de texte, bouton envoyer, boite de dialogue)
scrollbar.place(x=376, y=6, height=406)
Dialog.place(x=6, y=6, height=430, width=370)
EntryBox.place(x=6, y=441, height=50, width=316)
SendButton.place(x=322, y=441, height=50)



def update():
    global placeholderFlag
    if (EntryBox.get("1.0", 'end-1c').strip() == ''):
        SendButton['state'] = DISABLED # Si pas de texte à envoyer le bouton d'envoie est désactivé
        placeholderFlag = 1
    elif EntryBox.get("1.0", 'end-1c').strip() != '':
        SendButton['state'] = ACTIVE
        placeholderFlag = 0
    fenetre_chat.after(100, update)


fenetre_chat.bind('<Return>', send)
update()

bob = Bot()

fenetre_chat.mainloop()
