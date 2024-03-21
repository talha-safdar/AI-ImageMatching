# working code

import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

image_paths = [r'C:\LHU\AI\images\cat\cat_0000.jpg', r'C:\LHU\AI\images\cat\cat_0001.jpg']
threshold = 500

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def match_image(image_path, image_paths, threshold):
    uploaded_image = Image.open(image_path).convert('L')
    uploaded_image = uploaded_image.resize((250, 250))
    uploaded_array = np.array(uploaded_image)

    min_mse = None
    matched_image_path = None

    for img_path in image_paths:
        dataset_image = Image.open(img_path).convert('L')
        dataset_image = dataset_image.resize((250, 250))
        dataset_array = np.array(dataset_image)

        current_mse = mse(uploaded_array, dataset_array)

        if min_mse is None or current_mse < min_mse:
            min_mse = current_mse
            matched_image_path = img_path

    if min_mse is not None and min_mse < threshold:
        return matched_image_path
    return None 

root = tk.Tk()
root.title("Image Matching System")

def upload_image():
    file_path = filedialog.askopenfilename()
    matched_image_path = match_image(file_path, image_paths, threshold)
    
    if matched_image_path:
        matched_img = Image.open(matched_image_path)
        matched_img = matched_img.resize((250, 250), Image.LANCZOS)
        matched_img_tk = ImageTk.PhotoImage(matched_img)
        matched_label.configure(image=matched_img_tk)
        matched_label.image = matched_img_tk
    else:
        print("No match found")

    uploaded_img = Image.open(file_path)
    uploaded_img = uploaded_img.resize((250, 250), Image.LANCZOS)
    uploaded_img_tk = ImageTk.PhotoImage(uploaded_img)
    uploaded_label.configure(image=uploaded_img_tk)
    uploaded_label.image = uploaded_img_tk

upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack()

uploaded_label = tk.Label(root)
uploaded_label.pack(side="left", padx=20)

matched_label = tk.Label(root)
matched_label.pack(side="right", padx=20)

root.mainloop()
