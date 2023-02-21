from pytube import YouTube
import sys
import tkinter as tk
from tkinter import filedialog
import os

window = tk.Tk()

#config setup
window.geometry("700x500")
window.resizable(False, False) 
window.configure(background="#1C2333")

icon = tk.PhotoImage(file='images/tkinter.png')
window.iconphoto(True, icon)  # sets the icon in the gui

window.title("GD YouTube Downloader")


#main container frame
container_frame = tk.Frame(window, bg="#0E1525", borderwidth=1, relief="sunken")
container_frame.pack(padx=30, pady=30, fill="both", expand=True)

#title label
title = tk.Label(container_frame,
                 text="GD YouTube Downloader",
                 fg="#ffffff",
                 background="#0E1525",
                 font=("monospace", 20, 'bold', 'underline'),
                 padx=10,
                 pady=30)
title.pack()

#textbox label
url_label = tk.Label(container_frame,
                     text="Enter Youtube URL: ",
                     fg="#ffffff",
                     background="#0E1525",
                     font=("monospace", 12),
                     padx=10,
                     pady=10)
url_label.pack()

#textbox url
url = tk.Entry(container_frame,
               background="#fff",
               fg="#0E1525",
               font=("monospace", 12),
               width = 30,
               justify=tk.CENTER)
url.pack()
url.focus()


#get youtube video info
def button_click():
  #check if url is a valid youtube url
  try:
    yt = YouTube(url.get())
    result.config(text="Youtube Video found: " + yt.title, 
                  padx=10, 
                  pady=10, 
                  fg="#fff")
    result.pack()
    
    #show the download button selection once the video object has been fetched
    downloadFrame.pack(padx=15, pady=15, expand=False)
    video_button.pack(fill=tk.BOTH, padx=10, pady=5)
    audio_button.pack(fill=tk.BOTH, padx=10, pady=5)

  except Exception as e:
    print(e)
    result.config(text="Please input a valid YouTube URL.", fg="red")
    result.pack()

#button frames
innerFrame = tk.Frame(container_frame, bg="#0E1525")
innerFrame.pack(padx=15, pady=15, expand=False)

#get info button
button = tk.Button(innerFrame,
                   text="Get Video info",
                   command=button_click,
                   background="#0E1525",
                   fg="#ffffff",
                   font=("monospace", 10),
                   padx=5, pady=5)
button.pack(fill=tk.BOTH, padx=10, pady=5)

#exit button
exit_button = tk.Button(innerFrame,
                        text="Close",
                        command=sys.exit,
                        fg="#ffffff",
                        background="#0E1525",
                        font=("monospace", 10),
                        padx=5)

exit_button.pack(fill=tk.BOTH, padx=10, pady=5)

#result label
result = tk.Label(container_frame, text="", bg="#0E1525", fg="#fff")
result.pack_forget()


#function for downloading as video
def video_download():
  yt = YouTube(url.get())
  download_path = filedialog.askdirectory()
  if download_path:
    stream = yt.streams.get_highest_resolution()
    stream.download(download_path)
    
    #hide buttons
    video_button.pack_forget()
    audio_button.pack_forget()
  
    result.config(text=f"{yt.title} has been downloaded!\n Please check your downloaded video file in {download_path}", fg="green")
    url.delete(0,len(url.get()))

  else:
    result.config(text="Please select a directory.", fg="red")


#function for downloading as audio/mp3
def audio_download():
  yt = YouTube(url.get())
  download_path = tk.filedialog.askdirectory()
  if download_path:
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(download_path)

    #hide buttons
    video_button.pack_forget()
    audio_button.pack_forget()
  
    result.config(text=f"{yt.title} has been downloaded!\n Please check your downloaded mp3 file in: {download_path}", fg="green")
    url.delete(0,len(url.get()))

    os.rename(f"{download_path}\\{yt.title}.mp4", f"{download_path}\\{yt.title}.mp3")
    
  else:
    result.config(text="Please select a directory.", fg="red")


#download button frame
downloadFrame = tk.Frame(container_frame, bg="#0E1525")
downloadFrame.pack_forget()

#download video button
video_button = tk.Button(downloadFrame,
                         text="Download video",
                         command=video_download)
video_button.pack_forget()

#download audio button
audio_button = tk.Button(downloadFrame,
                         text="Download as mp3",
                         command=audio_download)
audio_button.pack_forget()

#show the gui
window.mainloop()