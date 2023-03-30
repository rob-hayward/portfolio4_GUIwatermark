from tkinter import *
from tkinter import ttk, font, colorchooser
from tkinter import filedialog
from PIL import Image, ImageFont, ImageDraw, ImageTk
import sys

# creates the window.
root = Tk()
root.title("Watermark Machine")
root.geometry('1300x700')


# Functions
def position_picker(event):
    position_label['text'] = f'({event.x}, {event.y})'


def color_picker():
    color_data = colorchooser.askcolor()
    color_label['text'] = color_data
    hex_code = str(color_data[1])
    txt_box.config(foreground=hex_code)


def font_picker(event):
    font_choice.config(family=font_box.get(font_box.curselection()))


# collects the user inputs from the GUI and feeds them into the watermarker function.
def get_variables():
    text = txt_box.get()
    text_font = font_box.get(font_box.curselection())
    color_data = color_label.cget('text')
    rgb = str(color_data[0])
    opacity = opacity_slide.get()
    # converts strings into tuples with eval()
    rgba = eval(rgb.replace(')', f', {opacity})'))
    text_pos = eval(position_label.cget('text'))
    # selects file to be watermarked
    path = filedialog.askopenfilename(initialdir='Images/',
                                      title='Choose your image',
                                      filetypes=(('all files', '*.*'),
                                                 ('png files', '*.png'),
                                                 ('jpg files', '*.jpg')))

    watermarker(path, text, text_font, rgba, text_pos)


def watermarker(file, text, text_font, rgba, text_pos):
    global out
    # opens and resizes image
    img = Image.open(file)
    img = img.resize((800, 600), Image.LANCZOS)
    # make a blank image for the text, initialized to transparent text color
    with img.convert('RGBA') as base:
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        # get a font
        fnt = ImageFont.truetype(font=text_font, size=40)
        # get a drawing context
        d = ImageDraw.Draw(txt)
        d.text(text_pos, f'{text}', font=fnt, fill=rgba)
        # output image with text
        out = Image.alpha_composite(base, txt)
        out = ImageTk.PhotoImage(out)
        # place image on GUI
        canvas.create_image(0, 0, anchor=NW, image=out)


# starting variable
font_choice = font.Font(family="Arial", size=40)
# Widgets
canvas = Canvas(root, width=810, height=610)
canvas.bind('<Button-1>', position_picker)
instructions_label = Label(text='', font='"arial black" 15 bold')
txt_box = Entry(root, font=font_choice, width=18, bg='dark grey')
txt_box.insert(0, 'Write your text here!')
font_box_label = Label(anchor=W, text='Choose your font from the menu', font='"arial black" 15 bold')
font_box = Listbox(root, selectmode=SINGLE, width=47, height=5)
for f in font.families():
    font_box.insert('end', f)
font_box.bind('<ButtonRelease-1>', font_picker)
opacity_slide = Scale(root, from_=90, to=255,
                      orient=HORIZONTAL,
                      label='Slide right to increase opacity', font='"arial black" 15 bold',
                      length=420)
color_btn = Button(root, text='Click to choose your text color', font='"arial black" 15 bold', command=color_picker)
color_label = Label()
position_label_instruction = Label(anchor=W, text='Click on the image to choose position of your text', font='"arial black" 15 bold')
position_label = Label()
main_btn = Button(root, text='Watermark My Image', font='"arial black" 22 bold', command=get_variables)

# Grid positions
canvas.grid(column=1, row=1, rowspan=7)
instructions_label.grid(column=0, row=0, columnspan=2)
txt_box.grid(column=0, row=1, sticky=NW, padx=20)
font_box_label.grid(column=0, row=2, sticky=NW, padx=20)
font_box.grid(column=0, row=3, sticky=NW, padx=20)
opacity_slide.grid(column=0, row=4, sticky=NW, padx=20)
color_btn.grid(column=0, row=5, sticky=NW, padx=20)
color_label.grid(column=2, row=6, sticky=NW, padx=20)
position_label_instruction.grid(column=0, row=7, sticky=NW, padx=20)
position_label.grid(column=2, row=7, sticky=NW, padx=20)
main_btn.grid(column=1, row=8, sticky=NW)

# puts a sample image up on screen
sample_file = 'Images/sample.jpg'
sample_text = 'Sample Image / Sample Text'
sample_fnt = 'Arial Black'
sample_rgba = (255, 99, 71, 128)
sample_pos = (10, 10)
watermarker(sample_file, sample_text, sample_fnt, sample_rgba, sample_pos)

root.mainloop()
