# Importing the necessary modules
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from PIL import Image
import os

def browse_file(img_path,window):
    input = fd.askopenfilename()
    window.lift()  # To bring encode/decode window on top again
    img_path.delete(0, tk.END)
    img_path.insert(0, input)


def browse_folder(after_save_path,encode_wn):
    input = fd.askdirectory()
    encode_wn.lift()  # To bring encode window on top again
    after_save_path.delete(0, tk.END)
    after_save_path.insert(0, input)

def is_text_too_big(image,text):
    img = Image.open(image, 'r')
    width, height = img.size
    resolution = width * height
    total_bits_reqd = len(text) * 8
    total_bits_reqd += 64     #For 4 extra '$' char appended in front & at end
    if total_bits_reqd > resolution:
        # Image is too small to fit users's text
        return True
    else:
        return False

def ToBinary(num):  # Converts decimal to binary
    rem = ''
    while num > 0:
        rem = str(num%2) + rem
        num //=2
    val = rem.zfill(8)
    return val


# This function takes the bits, manipulates them according to the data and returns the modified bits in form of a list
def generate_data(pixels, data):
    data_in_binary = []
    for i in data:
        binary_data = format(ord(i), '08b')
        data_in_binary.append(binary_data)    # Storing data in binary form

    data_string=''
    for i in data_in_binary:    # Combining all bits of each char into a string
        data_string += i

    length_of_data = len(data_string)       # Finding the length of data string of binary bits

    pixels = list(pixels)  # putting all pixel values in a list, which is eventually a list of tuples
    pixel_list = [j for i in pixels for j in i]     # converting the list of tuples to a single list of rgb values

    pixel_in_binary = []
    for i in pixel_list:
        pixel_in_binary.append(ToBinary(i))

    for i in range(length_of_data):
        if data_string[i]=='0' and pixel_in_binary[i][-1]=='1':
            val = str(int(pixel_in_binary[i])-1)
            pixel_in_binary[i] = val.zfill(8)
        elif data_string[i]=='1' and pixel_in_binary[i][-1]=='0':
            val = str(int(pixel_in_binary[i])+1)
            pixel_in_binary[i] = val.zfill(8)

    pixel_in_binary = tuple(pixel_in_binary)
    pixels.clear()      # Clears the pixels list
    for i in pixel_in_binary:
        dec = int(i,2)
        pixels.append(dec)

    q=[]
    for i in range(0,length_of_data,3):
        tup = tuple(pixels[i:i+3])
        q.append(tup)

    return q    # Returns the list of tuples containing modified r,g,b values


# This function encodes the data in the image
def encryption(img, data):
    size = img.size[0]
    (x, y) = (0, 0)
    for pixel in generate_data(img.getdata(), data):
        img.putpixel((x, y), pixel)
        if size-1 == x:
            x = 0
            y += 1
        else:
            x += 1


# This function will create a copy of old image, encode the data within the copied image and save it to the provided path
def main_encryption(img, text, new_image_name, after_save_path, encode_wn):
    spcl_char=['/','\\','?','*','>','<','|']
    ls = ['P' for i in spcl_char if i in new_image_name]     # Checking if any special character is present in list

    if (len(text) == 0) or (len(img) == 0) or (len(new_image_name) == 0):
        mb.showerror("Error", 'You have not put a value! \nPlease put all values before pressing the button')
        encode_wn.lift()
    elif new_image_name.count(" ") >= 1:
        mb.showerror("Error", 'File name cannot have spaces! \nPlease put a valid name')
        encode_wn.lift()
    elif ls:
        mb.showerror("Error", 'File name cannot have special characters! \nPlease put a valid name')
        encode_wn.lift()
    elif not os.path.exists(img):
        mb.showerror("Error", 'No such File or Directory exists! \nPlease recheck and Enter full path name')
        encode_wn.lift()
    elif is_text_too_big(img, text):
        mb.showerror("Error", 'Text is too big to fit in the image! \nUse an image with higher resolution')
        encode_wn.lift()
    else:
        image = Image.open(img, 'r')
        new_image = image.copy()
        extra_text = '$$$$'     # helps in decoding the encoded text
        text = extra_text + text + extra_text
        encryption(new_image, text)
        ## Providing PATHNAME
        new_image_name = after_save_path + '/' + new_image_name + '.png'
        new_image.save(new_image_name,'png')
        if os.path.exists(new_image_name):
            tk.Label(encode_wn, text='New Image Successfully saved to the provided path!', font=("Helvetica", 16),
                  bg='#F1E4E8', fg='#214E34').place(x=190, y=434)
        else:
            tk.Label(encode_wn, text='Not saved. Refresh and try again.', font=("Helvetica", 16),
                     bg='#F1E4E8', fg='#214E34').place(x=190, y=434)


# This function will take the image, decode the data from it, and will display on the screen
def main_decryption(img, textbox, decode_wn):
    if (len(img) == 0):
        mb.showerror("Error", 'You have not put a value! \nPlease put all values before pressing the button')
        decode_wn.lift()
    elif not os.path.exists(img):
        mb.showerror("Error", 'No such File or Directory exists! \nPlease recheck and Enter full path name')
        decode_wn.lift()
    else:
        image = Image.open(img, 'r')
        image_data = list(image.getdata())
        extra_data = '00100100001001000010010000100100'
        data = ''
        pixel_list = [j for i in image_data for j in i]

        binary_string = ''
        for i in pixel_list:
            binary_string += str(i % 2)

        binary_string = binary_string[len(extra_data):]
        last_startIndex = binary_string.find(extra_data)

        for i in range(0, last_startIndex, 8):
            pixels = binary_string[i:i + 8]
            data += chr(int(pixels, 2))

        textbox.set(data)  # Puts the decoded data in an Entry box


# Creating the 'Encode' window
def encode_image():
    encode_wn = tk.Toplevel(root)
    encode_wn.title("Encode an Image")
    encode_wn.geometry('850x500+365+132')
    encode_wn.resizable(0, 0)

    # background colour of decode window
    background_color = '#F1E4E8'
    button_color = '#138A36'
    encode_wn.config(bg='#F1E4E8')

    tk.Label(encode_wn, text='Encode Image', font=("Helvetica", 20), bg=background_color, bd=2, relief="solid", padx=10, pady=10).place(x=320, y=50, rely=0)

    # Asking for the pathname of original image
    tk.Label(encode_wn, text='Enter the path to the image (with extension)', font=("Helvetica", 14), bg=background_color).place(x=20, y=150)
    img_path = tk.Entry(encode_wn, font=("Helvetica", 11), width=42)
    img_path.place(x=400, y=152, height=25)
    tk.Button(encode_wn, text="Browse", command=lambda: browse_file(img_path, encode_wn)).place(x=760, y=151)

    # Asking for the encoded data
    tk.Label(encode_wn, text='Enter the data to be encoded', font=("Helvetica", 14), bg=background_color).place(x=20, y=200)
    text_to_be_encoded = tk.Entry(encode_wn, font=("Helvetica", 11), width=54)
    text_to_be_encoded.place(x=400, y=200, height=30)

    # Asking for the output image name
    tk.Label(encode_wn, text='Enter the output image name (without extension)', font=("Helvetica", 14), bg=background_color).place(x=20, y=250)
    output_image_name = tk.Entry(encode_wn, font=("Helvetica", 11), width=35)
    output_image_name.place(x=455, y=250, height=25)

    # Asking pathname of 'output image'
    tk.Label(encode_wn, text='Enter the path to save output image', font=("Helvetica", 14), bg=background_color).place(x=20, y=300)
    after_save_path = tk.Entry(encode_wn, font=("Helvetica", 11), width=42)
    after_save_path.place(x=400, y=300, height=25)
    tk.Button(encode_wn, text="Browse", command=lambda: browse_folder(after_save_path, encode_wn)).place(x=760, y=301)

    # Final Encode button which starts the actual execution of steganography
    btn = tk.Button(encode_wn, text='Encode Image', font=('Helvetica', 15), bg=button_color, fg='white', relief='raised', command=lambda:main_encryption(img_path.get(), text_to_be_encoded.get(), output_image_name.get(), after_save_path.get(), encode_wn))
    btn.place(x=350, y=380)


# Creating the 'Decode' window
def decode_image():
    decode_wn = tk.Toplevel(root)
    decode_wn.title("Decode an Image")
    decode_wn.geometry('850x510+365+132')
    decode_wn.resizable(0, 0)

    #background colour of decode window
    background_color = '#F1E4E8'
    button_color = '#138A36'
    decode_wn.config(bg=background_color)

    tk.Label(decode_wn, text='Decode Image', font=("Helvetica", 20), bg=background_color, bd=2, relief="solid", padx=10, pady=10).place(x=320, y=60, rely=0)  #x=320, y=20, rely=0

    # Asking for the pathname of image which needs to be decoded
    tk.Label(decode_wn, text='Enter the path to the image (with extension)', font=("Helvetica", 14), bg=background_color).place(x=20, y=160)
    img_entry = tk.Entry(decode_wn, font=("Helvetica",11), width=42)
    img_entry.place(x=400, y=161, height=25)
    tk.Button(decode_wn, text="Browse", command=lambda: browse_file(img_entry, decode_wn)).place(x=760, y=160)


    text_strvar = tk.StringVar()

    encrypted_textbox = tk.Entry(decode_wn, font=('Times New Roman', 14), width=65, justify='center', text=text_strvar, state='disabled')
    encrypted_textbox.place(x=127, y=295, height=120)

    # For horizontal Scrollbar
    xscroll = tk.Scrollbar(decode_wn, orient='horizontal')
    xscroll.config(command=encrypted_textbox.xview)
    xscroll.place(x=129, y=398, width=585)
    encrypted_textbox.configure(xscrollcommand=xscroll.set)

    # Final Decode button which starts the actual execution of decrypting the data
    b1 = tk.Button(decode_wn, text='Decode Image', font=('Helvetica', 15), bg=button_color, fg='white',
                relief="raised", command=lambda:main_decryption(img_entry.get(), text_strvar, decode_wn))
    b1.place(x=345, y=220)


# Initializing the main window
root = tk.Tk()
blank_space =" "    # One empty space
root.title(100*blank_space+'Steganography Software')    # To bring the text in the center
root.geometry('800x420+390+182')  # root.geometry('800x420+width+height')

root.resizable(0, 0)    # User would not be able to maximize or minimize
root.config(bg='NavajoWhite')
tk.Label(root, text='Steganographic Operations', font=('Helvetica', 30), bg='NavajoWhite',
      wraplength=300).place(x=260, y=50)

tk.Button(root, text='Encode', width=20, font=('Times New Roman', 18), bg='LightBlue', command=encode_image).place(
    x=262, y=200)
tk.Button(root, text='Decode', width=20, font=('Times New Roman', 18), bg='LightBlue', command=decode_image).place(
    x=262, y=280)

# Finalizing the window
root.update()
root.mainloop()
