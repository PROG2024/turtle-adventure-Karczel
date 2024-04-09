from PIL import Image, ImageTk
import tkinter as tk

root = tk.Tk()
root.title("Canvas Item Example")
frame = tk.Frame()
frame.pack()
canvas = tk.Canvas(frame, width=500, height=400, background="gray75")
canvas.pack()

img = Image.open("PowerTwo.png")
imgtk = ImageTk.PhotoImage(img)
canvas.create_image(0, 0, image=imgtk)

root.mainloop()