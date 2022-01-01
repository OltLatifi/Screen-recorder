import os
import cv2
import keyboard
import threading
import pyautogui
import numpy as np
from tkinter import *

# makes a folder or notifies that the folder exists
try:
    os.mkdir('Screen Recording')
    print('Folder created')
except FileExistsError:
    print('Folder already exists')

# constants
BIGGEST_I = 0
RECORDING_LIST = os.listdir('Screen Recording')
SCREEN_SIZE = tuple(pyautogui.size())
FPS = 8

# this part generates the index of the last recording and allows the program to save the next recording with a unique name
for i in RECORDING_LIST:
    if i == 'Thumbs.db':
        pass
    else:
        # <-- this just gets the value after (#) or the index
        index = int(i.split('#')[1].split('.')[0])
        if index > BIGGEST_I:
            BIGGEST_I = index

index = BIGGEST_I + 1


# records the screen until <esc> is pressed
def start_or_stop():
    print("Recording has started")
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(
        "Screen Recording/video#{0}.avi".format(index), fourcc, FPS, (SCREEN_SIZE))

    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
        # if the user clicks esc, it exits
        if keyboard.is_pressed('esc'):
            print('Recording ended')
            cv2.destroyAllWindows()
            out.release()
            root.destroy()
            break


if __name__ == "__main__":
    t1 = threading.Thread(target=start_or_stop)

    root = Tk()
    root.geometry('200x130')
    root.title('Screen Recorder')
    root.configure(background='#b5d1ff')
    # root.iconbitmap('favicon.ico')

    start_stop_button = Button(root, text="Start", command=t1.start, bg="#b5d1ff", bd=1, padx=4)
    start_stop_button.place(x=20, y=20, width=160, height=40)

    frm = Frame(root, bg='black')
    frm.place(x=20, y=70, width=160, height=40)

    lbl = Label(frm, text="To stop, press <ESC>", anchor=CENTER, bg="#b5d1ff", padx=4)
    lbl.place(x=1, y=1, width=158, height=38)

    root.mainloop()
