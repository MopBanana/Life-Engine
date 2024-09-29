from PIL import Image, ImageTk
import tkinter as tk
import math

root = tk.Tk()

root.geometry("500x600")
root.config(bg="lightgrey")

canvas = tk.Canvas(root, width="500", height="500")

img = Image.new("1", (20,20))

data = [0]*400
img.putdata(data, 1, 0)

def render(image):
    global tkimg

    tkimg = image.resize((500,500))
    tkimg = ImageTk.BitmapImage(tkimg)
    canvas.itemconfigure(grid,image=tkimg)

def click(event):
    
    temp = 0
    print(click, math.floor(event.x/25), math.floor(event.y/25))
    
    if img.getpixel((math.floor(event.x/25), math.floor(event.y/25))) == 0:
        temp = 1
    else:
        temp = 0

    print(temp)
    
    img.putpixel((math.floor(event.x/25), math.floor(event.y/25)), temp)

    render(img)
    
tkimg = img.resize((500,500))
tkimg = ImageTk.BitmapImage(tkimg)

grid = canvas.create_image(250, 250, image=tkimg, anchor="center")
canvas.pack()

canvas.bind("<Button>", click)

stayLabel = tk.Label(root, text="Stay:", bg="lightgrey", anchor="w")
stayLabel.place(x=0, y=505)
stayEntry = tk.Entry(root)
stayEntry.place(x=50, y=505)

liveLabel = tk.Label(root, text="Live:", bg="lightgrey", anchor="w")
liveLabel.place(x=0, y=525)
liveEntry = tk.Entry(root)
liveEntry.place(x=50, y=525)

def step():
    swap = []

    stay = stayEntry.get().split(",")
    for n in range(len(stay)):
        if stay[n] != "":
            stay[n] = int(stay[n])

    live = liveEntry.get().split(",")
    for n in range(len(live)):
        if live[n] != "":
            live[n] = int(live[n])
    
    for y in range(0,20):
        swap.append([])
        for x in range(0,20):
            state = img.getpixel((x, y))
            ngb = 0
            swap[y].append([0])

            try: ngb += img.getpixel((x-1, y)) # L
            except: pass
            try: ngb += img.getpixel((x-1, y-1)) # UL
            except: pass
            try: ngb += img.getpixel((x, y-1)) # U
            except: pass
            try: ngb += img.getpixel((x+1, y-1)) # UR
            except: pass
            try: ngb += img.getpixel((x+1, y)) # R
            except: pass
            try: ngb += img.getpixel((x+1, y+1)) # DR
            except: pass
            try: ngb += img.getpixel((x, y+1)) # D
            except: pass
            try: ngb += img.getpixel((x-1, y+1)) # DL
            except: pass

            if state == 0 and ngb in live:
                swap[y][x] = 1
            elif state == 1 and not(ngb in stay):
                swap[y][x] = 1

    for i in range(len(swap)):
        for j in range(len(swap[0])):
            state = img.getpixel((j, i))
            if swap[i][j] == 1 and state == 0:
                img.putpixel((j,i), 1)
            elif swap[i][j] == 1 and state == 1:
                img.putpixel((j,i), 0)

    render(img)
    root.after(1000, step)

root.after(2000, step)

root.mainloop()
