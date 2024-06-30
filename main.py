import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from style_transfer import style_transfer
from utils import load_images, get_stylized_rgb
import matplotlib.pyplot as plt

class ImageUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("no-NN Style Transfer")
        
        self.root.geometry("500x800")
        self.root.resizable(True, True)

        self.IMG_WDTH = int(50 * 3)
        self.IMG_HGH = int(37 * 3)

        self.content_image_path = None
        self.style_image_path = None

        self.content_image_display = self.create_upload_field("Style", 0, self.upload_content_image)
        self.style_image_display = self.create_upload_field("Content", 0, self.upload_style_image)

        self.process_button = tk.Button(root, text="Perform Style Transfer", command=self.process_images)
        self.process_button.grid(row=2, column=0, columnspan=2, pady=(250, 10), sticky="s")

        self.result_label = tk.Label(root, text="Result Image")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=20)
        self.result_image_label = tk.Label(root)
        self.result_image_label.grid(row=4, column=0, columnspan=2, pady=10)

    def create_upload_field(self, text, row, command):
        label = tk.Label(self.root, text=text)
        label.grid(row=row, column=0 if text == "Style" else 1, padx=20, pady=10)

        upload_button = tk.Button(self.root, text="Upload", command=command)
        upload_button.grid(row=row+1, column=0 if text == "Style" else 1, padx=20, pady=10)

        display_label = tk.Label(self.root)
        display_label.grid(row=row+2, column=0 if text == "Style" else 1, padx=20, pady=10)

        return display_label

    def upload_content_image(self):
        self.content_image_path = filedialog.askopenfilename()
        self.display_image(self.content_image_path, self.content_image_display)

    def upload_style_image(self):
        self.style_image_path = filedialog.askopenfilename()
        self.display_image(self.style_image_path, self.style_image_display)

    def display_image(self, image_path, display_label, from_array=False, image_content=None):
        if image_path and not from_array:
            img = Image.open(image_path)
            img.thumbnail((200, 200))
            img = ImageTk.PhotoImage(img)
            display_label.config(image=img)
            display_label.image = img
        
        elif from_array:
            img = Image.fromarray(image_content)
            Iwidth, Iheight = img.size
            new_width = Iwidth * 4
            new_height = Iheight * 4
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            resized_img = ImageTk.PhotoImage(resized_img)
            display_label.config(image=resized_img)
            display_label.image = resized_img


    def process_images(self):
        content_image, style_image = load_images(self.content_image_path, self.style_image_path, self.IMG_WDTH, self.IMG_HGH)

        generated_stylized_image = style_transfer(content_image, style_image, patch_size=2, stride=2)
        generated_stylized_image = get_stylized_rgb(generated_stylized_image)

        self.display_image(image_path=None, display_label=self.result_image_label, from_array=True, image_content=generated_stylized_image)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageUploaderApp(root)
    root.mainloop()
