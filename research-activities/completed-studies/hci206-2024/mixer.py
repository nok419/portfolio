import pygame as p
from tkinter import *
import tkinter.font as font
from tkinter import filedialog
def addsongs(): 
    temp_song=filedialog.askopenfilenames(initialdir="Music/",title="Choose a song", filetypes=(("mp3 Files","*.mp3"),("wav Files","*.wav"),))
    
def deletesong():
    curr_song=songs_list.curselection()
    songs_list.delete(curr_song[0])  
def Play():
    song=songs_list.get(ACTIVE)
    song=f'D:/zemi/mix/sounds/{song}'
    p.mixer.music.load(song)
    p.mixer.music.play()
def Effect():
    set=songs_list.get(ACTIVE)
    set=f'D:/zemi/mix/sounds/{set}'
    se=p.mixer.Sound(set)
    se.play()
def Pause():
    p.mixer.music.pause()
def Stop():
    p.mixer.music.stop()
    songs_list.selection_clear(ACTIVE)
def Resume():
    p.mixer.music.unpause()
def Previous():
    previous_one=songs_list.curselection()
    previous_one=previous_one[0]-1
    temp2=songs_list.get(previous_one)
    temp2=f'C:/Users/DataFlair/python-mp3-music-player/{temp2}'
    p.mixer.music.load(temp2)
    p.mixer.music.play()
    songs_list.selection_clear(0,END)
    songs_list.activate(previous_one)
    songs_list.selection_set(previous_one)
def Next():
    next_one=songs_list.curselection()
    next_one=next_one[0]+1
    temp=songs_list.get(next_one)
    temp=f'C:/Users/DataFlair/python-mp3-music-player/{temp}'
    p.mixer.music.load(temp)
    p.mixer.music.play()
    songs_list.selection_clear(0,END)
    songs_list.activate(next_one)
    songs_list.selection_set(next_one)

root=Tk()
root.title('音楽再生ツール ')
p.mixer.init()
songs_list=Listbox(root,selectmode=SINGLE,bg="black",fg="white",font=('arial',15),height=12,width=52,selectbackground="gray",selectforeground="black")
songs_list.grid(columnspan=9) 
defined_font = font.Font(family='Helvetica')
play_button=Button(root,text="Play",width =7,command=Play)
play_button['font']=defined_font
play_button.grid(row=1,column=0)
play2_button=Button(root,text="Effect",width =7,command=Effect)
play2_button['font']=defined_font
play2_button.grid(row=1,column=1)
pause_button=Button(root,text="Pause",width =7,command=Pause)
pause_button['font']=defined_font
pause_button.grid(row=1,column=2)
stop_button=Button(root,text="Stop",width =7,command=Stop)
stop_button['font']=defined_font
stop_button.grid(row=1,column=3)
Resume_button=Button(root,text="Resume",width =7,command=Resume)
Resume_button['font']=defined_font
Resume_button.grid(row=1,column=4)
previous_button=Button(root,text="Prev",width =7,command=Previous)
previous_button['font']=defined_font
previous_button.grid(row=1,column=5)
next_button=Button(root,text="Next",width =7,command=Next)
next_button['font']=defined_font
next_button.grid(row=1,column=6)
my_menu=Menu(root)
root.config(menu=my_menu)
add_song_menu=Menu(my_menu)
my_menu.add_cascade(label="Menu",menu=add_song_menu)
add_song_menu.add_command(label="Add songs",command=addsongs)
add_song_menu.add_command(label="Delete song",command=deletesong)
mainloop()

