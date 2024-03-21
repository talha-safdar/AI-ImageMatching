import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
from scipy.spatial.distance import cosine
from pathlib import Path

# Initialize ResNet50 model for feature extraction
model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

images_path = Path('images/') # local directory with images
image_paths = [str(image) for image in images_path.glob('*.jpg')]

def extract_features(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = model.predict(img_array)
    return features.flatten()

def match_image(image_path, image_paths, model, threshold=0.01):
    uploaded_features = extract_features(image_path, model)
    
    for img_path in image_paths:
        current_features = extract_features(img_path, model)
        dist = cosine(uploaded_features, current_features)
        
        if dist < threshold:
            return img_path
    
    return None

root = tk.Tk()
root.title("VisualMatch AI")

def upload_image():
    file_path = filedialog.askopenfilename()
    if not file_path:  # Check if a file was actually selected
        return

    matched_image_path = match_image(file_path, image_paths, model)
    
    if matched_image_path:
        matched_img = Image.open(matched_image_path)
        matched_img = matched_img.resize((250, 250), Image.LANCZOS)
        matched_img_tk = ImageTk.PhotoImage(matched_img)
        matched_label.configure(image=matched_img_tk)
        matched_label.image = matched_img_tk
        status_label.config(text="Exact match found!")
    else:
        status_label.config(text="No exact match found.")
        matched_label.configure(image='')
        matched_label.image = None

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

status_label = tk.Label(root, text="Upload an image to start matching", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()