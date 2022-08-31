#import tkinter as tk
from tkinter import*

def image_rose():
    window=Tk()
    window.title('Image')
    window = Canvas(window,width = 450,height= 450)
    window.pack()
    my = PhotoImage(file ='C:\\Users\\Dell\\Desktop\\bot\\photos\\redrose.PNG')
    window.create_image(0,0, anchor=NW, image = my)

    window.mainloop()
    
def image_sunflower():
    window=Tk()
    window.title('Image')
    window = Canvas(window,width = 450,height= 450)
    window.pack()
    my = PhotoImage(file ='C:\\Users\\Dell\\Desktop\\bot\\photos\\sunflower.PNG')
    window.create_image(0,0, anchor=NW, image = my)

    window.mainloop()
    
def image_lily():
    window=Tk()
    window.title('Image')
    window = Canvas(window,width = 450,height= 450)
    window.pack()
    my = PhotoImage(file ='C:\\Users\\Dell\\Desktop\\bot\\photos\\lily.PNG')
    window.create_image(0,0, anchor=NW, image = my)

    window.mainloop()
    
def photo_gallery():
    inp2 = input("You: ")
    if inp2.lower() =="rose":
        print("The image of rose")
        image_rose()
    elif inp2.lower() =="sunflower":
        print("The image of sunflower")
        image_sunflower()
    elif inp2.lower() =="lily":
        print("The image of lily")
        image_lily()
    else:
        print("Moa: The image is not currently availabe, Please come back later")
