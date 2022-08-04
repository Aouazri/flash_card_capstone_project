from tkinter import *
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
LANG_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")

# ---------------------------- Create Flash Cards ------------------------------- #
try:
    df = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    df = pd.read_csv("data/french_words.csv")
    word_dict = df.to_dict(orient="records")
else:
    word_dict = df.to_dict(orient="records")


def next_card():
    global eng_translation, flip_timer, random_word
    random_word = choice(word_dict)
    fr_word = random_word['French']
    window.after_cancel(flip_timer)
    eng_translation = random_word['English']
    # French
    canvas.itemconfig(card_title, text="French", fill="Black")
    canvas.itemconfig(card_word, text=fr_word, fill="Black")
    canvas.itemconfig(canvas_image, image=bg_image)
    flip_timer = window.after(3000, func=flip_card)


def is_known():
    # Removing words that the user knows
    word_dict.remove(random_word)
    data = pd.DataFrame(word_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def flip_card():
    # To change The image
    canvas.itemconfig(canvas_image, image=flip_image)
    canvas.itemconfig(card_title, text="English", fill="White")
    canvas.itemconfig(card_word, text=eng_translation, fill="White")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526)
bg_image = PhotoImage(file="images/card_front.png")
# flip image for english translation
flip_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=bg_image)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="Title", font=LANG_FONT)
card_word = canvas.create_text(400, 263, text="Word", font=WORD_FONT)

# Buttons
correct_image = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_image, highlightthickness=0, command=is_known)
correct_button.config(padx=50, pady=50)
correct_button.grid(row=1, column=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.config(padx=50, pady=50)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()
