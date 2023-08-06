import random
import time
import tkinter.ttk
from tkinter import *
from tkinter import ttk
import ctypes
import threading

ctypes.windll.shcore.SetProcessDpiAwareness(1)
start = -1
if start == -1:
    T_OPTIONS = ['1 minute', '2 minutes', '3 minutes', '5 minutes']
    D_OPTIONS = ['Easy', 'Moderate', 'Hard']
    time_over = False
    e = tkinter.ttk.Entry
    elbl = tkinter.ttk.Label
    entered_text = []
    word_list = []
    passage = []
    delete_press = 0
    selected = []
    answer = tkinter.ttk.Label

def gettext(difficulty='easy'):
    samples_list = []
    with open(f'{difficulty}_samples.txt', mode='r') as samples:
        text = samples.readlines()
        for t in text[::2]:
            samples_list.append(t.replace('\n', ''))
        return samples_list


def timer(length=1):
    global time_over
    time_over = False
    start_button.config(state='disabled')
    time.sleep(length * 60)
    start_button.config(state='enabled')
    time_over = True


def show_passage(text):
    global time_over, e, elbl, entered_text, passage, start, answer
    if start == 0:
        # mainframe.bind('<space>', delete)
        if not time_over:
            e = ttk.Entry(mainframe, justify='center')
            root.bind('<space>', delete)
            passage_ = random.choice(text)
            if len(passage_.split()) > 20:
                passage = passage_.split()[:20]
                passage = ' '.join(passage)
                words(passage)
            else:
                passage = passage_.split()
                passage = ' '.join(passage)
                words(passage)
            elbl = ttk.Label(mainframe, text=passage)
            elbl.pack()
            selected_passages()
            e.focus()
            e.pack()
            check()
    else:
        e.config(state='enabled')
        e.delete(0, END)
        answer.config(text='')
        root.bind('<space>', delete)
        passage_ = random.choice(text)
        if len(passage_.split()) > 20:
            passage = passage_.split()[:20]
            passage = ' '.join(passage)
            words(passage)
        else:
            passage = passage_.split()
            passage = ' '.join(passage)
            words(passage)
        elbl.config(text=passage)
        elbl.pack()
        selected_passages()
        e.focus()
        # e.pack()
        check()

def check():
    global passage, elbl, entered_text, time_over, e, delete_press
    # ent = entered_text
    act = passage.split()
    if not time_over:
        if delete_press >= len(act):
            passage_ = gettext(click.get())
            passage = random.choice(passage_)
            elbl.config(text=passage)
            delete_press = 0
            selected_passages()
        mainframe.after(300, check)
    if time_over:
        disable(e)



def disable(e):
    global entered_text, passage
    e.config(state='disabled')
    compare()


def delete(entry):
    global e, entered_text, passage, delete_press
    entered_text.append(e.get().strip(' '))
    e.delete(0, END)
    delete_press += 1


def words(text):
    global word_list
    list_ = text.split()
    for l in list_:
        word_list.append(l)


def compare():
    global entered_text, actual_text, passage, delete_press, selected, answer
    passage = passage.split()
    words_typed = len(entered_text)
    count = 0
    for i in range(len(entered_text)):
        if entered_text[i] == selected[i]:
            count += 1
    if words_typed != 0:
        accuracy = count / len(entered_text) * 100
    else:
        accuracy = 0
    speed = round(words_typed/minutes)
    output = f'Your total typing speed is {int(speed)} wpm with an accuracy of {round(accuracy, 2)}% bringing you actual typing speed to {int(round(speed/100*accuracy))}wpm'
    if start == 0:
        answer = ttk.Label(mainframe, text=output)
        answer.pack()
    else:
        answer.config(text=output)

def selected_passages():
    global passage, selected
    selected.extend(passage.split())


def count_start():
    global start, time_over, e, elbl, entered_text, word_list, passage, delete_press, selected
    time_over = False
    # e = tkinter.ttk.Entry
    # elbl = tkinter.ttk.Label
    entered_text = []
    word_list = []
    passage = []
    delete_press = 0
    selected = []
    start += 1

root = Tk()
root.title('Typing Speed Test')
root.geometry('1000x400')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky='N, W, E, S')

clicked = StringVar()
clicked.set('1 minute')
t_drop = ttk.OptionMenu(mainframe, clicked, '1 minute', *T_OPTIONS)
t_drop.pack(pady=10)

click = StringVar()
click.set('Moderate')
d_drop = ttk.OptionMenu(mainframe, click, 'Moderate', *D_OPTIONS)
d_drop.pack(pady=10)

minutes = int(list(clicked.get())[0])
start_button = ttk.Button(mainframe, text='Start',
                          command=lambda: [count_start() ,threading.Thread(target=show_passage(gettext(click.get()))).start(),
                                           threading.Thread(target=lambda: timer(minutes)).start()])
start_button.pack(pady=20)

label = ttk.Label(mainframe)

root.mainloop()
