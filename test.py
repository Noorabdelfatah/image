import cv2
import numpy as np
from tkinter import filedialog, Tk, Label, Frame
from tkinter import ttk
from PIL import Image, ImageTk


img = None  
panel_original = None
panel_result = None

def load_image():
    global img, panel_original

    file_path = filedialog.askopenfilename()
    if len(file_path) > 0:
        img = cv2.imread(file_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)

        if panel_original is None:
            panel_original = Label(frame_center, image=img_tk)
            panel_original.image = img_tk
            panel_original.pack(padx=10, pady=10)
        else:
            panel_original.configure(image=img_tk)
            panel_original.image = img_tk

def apply_negative():
    global img, panel_result
    if img is None:
        return

    negative = 255 - img
    neg_rgb = cv2.cvtColor(negative, cv2.COLOR_BGR2RGB)
    neg_pil = Image.fromarray(neg_rgb)
    neg_tk = ImageTk.PhotoImage(neg_pil)

    if panel_result is None:
        panel_result = Label(frame_right, image=neg_tk)
        panel_result.image = neg_tk
        panel_result.pack(padx=10, pady=10)
    else:
        panel_result.configure(image=neg_tk)
        panel_result.image = neg_tk

def apply_log():
    global img, panel_result
    if img is None:
        return
    
    c = 255 / np.log(1 + np.max(img))
    log_img = c * np.log(1 + img.astype(np.float32))
    log_img = np.array(log_img, dtype=np.uint8)
    log_rgb = cv2.cvtColor(log_img, cv2.COLOR_BGR2RGB)
    log_pil = Image.fromarray(log_rgb)
    log_tk = ImageTk.PhotoImage(log_pil)

    if panel_result is None:
        panel_result = Label(frame_right, image=log_tk)
        panel_result.image = log_tk
        panel_result.pack(padx=10, pady=10)
    else:
        panel_result.configure(image=log_tk)
        panel_result.image = log_tk

def apply_gamma():
    global img, panel_result
    if img is None:
        return
    
    gamma = 1.5
    gamma_img = np.array(255 * (img / 255) ** gamma, dtype=np.uint8)
    gamma_rgb = cv2.cvtColor(gamma_img, cv2.COLOR_BGR2RGB)
    gamma_pil = Image.fromarray(gamma_rgb)
    gamma_tk = ImageTk.PhotoImage(gamma_pil)

    if panel_result is None:
        panel_result = Label(frame_right, image=gamma_tk)
        panel_result.image = gamma_tk
        panel_result.pack(padx=10, pady=10)
    else:
        panel_result.configure(image=gamma_tk)
        panel_result.image = gamma_tk

def apply_hist_eq():
    global img, panel_result
    if img is None:
        return
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist_eq = cv2.equalizeHist(img_gray)
    hist_eq_rgb = cv2.cvtColor(hist_eq, cv2.COLOR_GRAY2RGB)
    hist_eq_pil = Image.fromarray(hist_eq_rgb)
    hist_eq_tk = ImageTk.PhotoImage(hist_eq_pil)

    if panel_result is None:
        panel_result = Label(frame_right, image=hist_eq_tk)
        panel_result.image = hist_eq_tk
        panel_result.pack(padx=10, pady=10)
    else:
        panel_result.configure(image=hist_eq_tk)
        panel_result.image = hist_eq_tk

def apply_contrast_stretch():
    global img, panel_result
    if img is None:
        return
    
    min_val = np.min(img)
    max_val = np.max(img)
    contrast_stretch = (img - min_val) * 255 / (max_val - min_val)
    contrast_stretch = np.array(contrast_stretch, dtype=np.uint8)
    contrast_rgb = cv2.cvtColor(contrast_stretch, cv2.COLOR_BGR2RGB)
    contrast_pil = Image.fromarray(contrast_rgb)
    contrast_tk = ImageTk.PhotoImage(contrast_pil)

    if panel_result is None:
        panel_result = Label(frame_right, image=contrast_tk)
        panel_result.image = contrast_tk
        panel_result.pack(padx=10, pady=10)
    else:
        panel_result.configure(image=contrast_tk)
        panel_result.image = contrast_tk

root = Tk()
root.title("Image Processing Project")
root.geometry("1200x600")

style = ttk.Style()
style.configure("TButton",
                font=("Arial", 14, "bold"),
                padding=10,
                relief="solid",
                borderwidth=3,
                width=20)

frame_left = Frame(root)
frame_left.pack(side="left", padx=10, pady=10)

frame_center = Frame(root)
frame_center.pack(side="left", padx=10, pady=10)

frame_right = Frame(root)
frame_right.pack(side="right", padx=10, pady=10)

btn_load = ttk.Button(frame_left, text="Upload Image", command=load_image, style="TButton")
btn_load.pack(pady=10)

btn_negative = ttk.Button(frame_left, text="Negative Image", command=apply_negative, style="TButton")
btn_negative.pack(pady=10)

btn_log = ttk.Button(frame_left, text="Logarithmic Transform", command=apply_log, style="TButton")
btn_log.pack(pady=10)

btn_gamma = ttk.Button(frame_left, text="Gamma Transformation", command=apply_gamma, style="TButton")
btn_gamma.pack(pady=10)

btn_hist_eq = ttk.Button(frame_left, text="Histogram Equalization", command=apply_hist_eq, style="TButton")
btn_hist_eq.pack(pady=10)

btn_contrast = ttk.Button(frame_left, text="Contrast Stretching", command=apply_contrast_stretch, style="TButton")
btn_contrast.pack(pady=10)

root.mainloop()
