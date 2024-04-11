"""This module runs a tkinter GUI for downloading YouTube Videos and Playlists"""

import threading
from tkinter import messagebox as mb
import customtkinter as ctk
import pytube as pt
from pytube.exceptions import RegexMatchError, VideoUnavailable

# Window Specifications
root = ctk.CTk()
root.title('YouTube Videos and Playlists Downloader')
root.geometry('600x600')
root.resizable(False, False)

def download_it():
    """Checking the downloading type"""

    if downloadable_type.get():
        try:
            yt = pt.Playlist(link.get())
            temp = yt.videos[0]
            del temp
        except KeyError:
            mb.showerror('ERROR', "The Link pasted doesn't consist any YouTube Playlist!")
        else:
            thread = threading.Thread(target=download_playlist, args=(yt,))
            thread.start()

    else:
        try:
            yt = pt.YouTube(link.get())
            yt.bypass_age_gate()
            temp = yt.streams[0]
            del temp
        except RegexMatchError:
            mb.showerror('ERROR', "The Link pasted doesn't consist any YouTube Video!")
        else:
            thread = threading.Thread(target=download_video, args=(yt,))
            thread.start()

def download_video(yt):
    """Downloading Video"""

    path = ctk.filedialog.askdirectory()
    yt.streams.order_by('resolution').last().download(path)
    mb.showinfo('SUCCESS', f'Downloaded "{yt.title}"!')

def download_playlist(yt):
    """Downloading Playlist"""

    path = ctk.filedialog.askdirectory()
    for vid in yt.videos:
        vid.streams.order_by('resolution').last().download(path)
    mb.showinfo('SUCCESS', f'Downloaded "{yt.title}"!')

# Variables
downloadable_type = ctk.IntVar()
link = ctk.StringVar()
percent = 0
progress_bar = 0

# Window Elements
rb1 = ctk.CTkRadioButton(root, text='Video', value=0, variable=downloadable_type)
rb1.place(relx=0.25, rely=0.2)
rb2 = ctk.CTkRadioButton(root, text='Playlist', value=1, variable=downloadable_type)
rb2.place(relx=0.62, rely=0.2)
ctk.CTkLabel(root, text='Paste the Link below').place(relx=0.5, rely=0.4, anchor='center')
textbox = ctk.CTkEntry(root, width=360, height=40, textvariable=link)
textbox.place(relx=0.2, rely=0.5)
button = ctk.CTkButton(root, height=30, text='Download', command=download_it)
button.place(relx=0.5, rely=0.7, anchor='center')

# For Fast Pasting
root.update()
textbox.focus()

# Repeat the Cycle
root.mainloop()
