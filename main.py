from tkinter import *
from tkinter import ttk
import googletrans
import threading

text_to_translate = None
def new_combo(event):
    global text_to_translate
    text_to_translate = f'{text_to_translate}.'

def thredingg():
    threading.Thread(target=translate).start()
    window.after(1000, thredingg)


def translate(event=None):
    global text_to_translate
    if not text1.get('1.0', 'end-1c').strip():
        text2.delete('1.0', 'end')
        text1.delete('1.0', 'end')

    try:
        if text1.get('1.0', 'end-1c').strip() and text1.get('1.0', 'end-1c') != text_to_translate:
            lang_from = combo1.get().lower()
            lang_to = combo2.get().lower()
            text_to_translate = text1.get('1.0',
                                          'end-1c')  # Pobranie tekstu z widgetu Text, pomijając ostatni znak nowej linii
            translator = googletrans.Translator()
            translated_text = translator.translate(text_to_translate, src=lang_from, dest=lang_to)
            text2.delete('1.0', 'end')  # Usunięcie tekstu z widgetu Text2
            text2.insert('end', translated_text.text)  # Wstawienie przetłumaczonego tekstu do widgetu Text2

    except Exception as e:
        print(e)


def rotate():
    old_text = text1.get('1.0', 'end')
    new_text = text2.get('1.0', 'end')
    old_combo = combo1.get().lower()
    new_combo = combo2.get().lower()
    combo1.set(new_combo)
    combo2.set(old_combo)
    text1.delete('1.0', 'end')
    text2.delete('1.0', 'end')
    text1.insert('end', new_text)
    text2.insert('end', old_text)


window = Tk()
window.resizable(False, False)
window.geometry('900x530')
window.config(bg='#dddddd')
Label(window, text="Translator", font=('Arial', 30, 'bold')).pack()

language = googletrans.LANGUAGES
languageV = list(language.values())
lang1 = language.keys()
combo1 = ttk.Combobox(window, width=30, font=('Roboto', 14), values=languageV)
combo1.set('English')
combo1.place(x=50, y=100)

combo2 = ttk.Combobox(window, width=30, font=('Roboto', 14), values=languageV)
combo2.place(x=460, y=100)
combo2.set('polish')
combo2.bind('<<ComboboxSelected>>', new_combo)


frame1 = Frame(window, bd='5', relief=RIDGE)
frame1.place(x=40, y=150, width=400, height=300)

text1 = Text(frame1, font=('Roboto', 15))
text1.place(x=0, y=0, width=370, height=290)
text1.bind('<<Modified>>', translate)

scrollbar1 = Scrollbar(frame1)
scrollbar1.pack(side=RIGHT, fill=Y)
scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

frame2 = Frame(window, bd='5', relief=RIDGE)
frame2.place(x=450, y=150, width=400, height=300)

scrollbar2 = Scrollbar(frame2)
scrollbar2.pack(side=LEFT, fill=Y)

text2 = Text(frame2, font=('Roboto', 15))
text2.place(x=0, y=0, width=370, height=290)


scrollbar2 = Scrollbar(frame2)
scrollbar2.pack(side=RIGHT, fill=Y)
scrollbar2.configure(command=text2.yview)
text2.configure(yscrollcommand=scrollbar2.set)

swapimg = PhotoImage(file='swap.png')

swap_btn = Button(window, image=swapimg, bg='#dddddd', relief='raised', bd=0,
                  padx=20, pady=10, cursor='hand2', command=rotate)
swap_btn.place(x=410, y=460)

thredingg()

window.mainloop()
