import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("no-NN Style Transfer")
        
        self.root.geometry("650x800")
        self.root.resizable(False, False)

        self.image1_path = None
        self.image2_path = None

        self.image1_display = self.create_upload_field("Style", 0, self.upload_image1)
        self.image2_display = self.create_upload_field("Content", 0, self.upload_image2)

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

    def upload_image1(self):
        self.image1_path = filedialog.askopenfilename()
        self.display_image(self.image1_path, self.image1_display)

    def upload_image2(self):
        self.image2_path = filedialog.askopenfilename()
        self.display_image(self.image2_path, self.image2_display)

    def display_image(self, image_path, display_label):
        if image_path:
            img = Image.open(image_path)
            img.thumbnail((200, 200))
            img = ImageTk.PhotoImage(img)
            display_label.config(image=img)
            display_label.image = img

    def process_images(self):
        # This is where you would process the images.
        # For simplicity, let's just show the first image as the result.
        if self.image1_path:
            self.display_image(self.image1_path, self.result_image_label)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageUploaderApp(root)
    root.mainloop()
