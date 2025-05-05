import cv2
import numpy as np
from tkinter import filedialog, Tk, Label, Frame
from tkinter import ttk
from PIL import Image, ImageTk

img = None
panel_original = None
panel_result = None
result_image = None

# حجم الصور
width = 470
height = 420

def load_image():
    global img, panel_original

    file_path = filedialog.askopenfilename()
    if file_path:
        img_original = cv2.imread(file_path)
        img = cv2.resize(img_original, (width, height))

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

def update_result_image(image):
    global panel_result, result_image

    image_resized = cv2.resize(image, (width, height))
    result_image = image_resized.copy()

    if len(image_resized.shape) == 2:
        img_rgb = cv2.cvtColor(image_resized, cv2.COLOR_GRAY2RGB)
    else:
        img_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)

    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    for widget in frame_center_result.winfo_children():
        widget.destroy()

    panel_result = Label(frame_center_result, image=img_tk)
    panel_result.image = img_tk
    panel_result.pack(padx=10, pady=10)

# ------------------- الفلاتر ---------------------

def apply_negative():
    if img is None:
        return
    negative = 255 - img
    update_result_image(negative)

def apply_log():
    if img is None:
        return
    c = 255 / np.log(1 + np.max(img))
    log_img = c * np.log(1 + img.astype(np.float32))
    log_img = cv2.normalize(log_img, None, 0, 255, cv2.NORM_MINMAX)
    log_img = np.array(log_img, dtype=np.uint8)
    update_result_image(log_img)

def apply_gamma():
    if img is None:
        return
    gamma = 1.5
    gamma_corrected = np.power(img / 255.0, gamma)
    gamma_img = np.uint8(gamma_corrected * 255)
    update_result_image(gamma_img)

def apply_hist_eq():
    if img is None:
        return
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist_eq = cv2.equalizeHist(img_gray)
    hist_eq_bgr = cv2.cvtColor(hist_eq, cv2.COLOR_GRAY2BGR)
    update_result_image(hist_eq_bgr)

def apply_contrast_stretch():
    if img is None:
        return
    min_val = np.min(img, axis=(0, 1))
    max_val = np.max(img, axis=(0, 1))
    contrast_stretch = (img - min_val) * 255 / (max_val - min_val)
    contrast_stretch = np.clip(contrast_stretch, 0, 255)
    contrast_stretch = np.array(contrast_stretch, dtype=np.uint8)
    update_result_image(contrast_stretch)

def apply_blur():
    if img is None:
        return
    blurred = cv2.GaussianBlur(img, (9, 9), 0)
    update_result_image(blurred)

def apply_edge_detection():
    if img is None:
        return
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img_gray, 100, 200)
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    update_result_image(edges_bgr)

def add_noise():
    if img is None:
        return
    noisy = img.copy()
    row, col, ch = noisy.shape
    mean = 0
    var = 20
    sigma = var ** 0.5
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(row, col, ch)
    noisy = noisy + gauss
    noisy = np.clip(noisy, 0, 255)
    noisy = noisy.astype(np.uint8)
    update_result_image(noisy)

def apply_sharpen():
    if img is None:
        return
    kernel = np.array([[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]])
    sharpened = cv2.filter2D(img, -1, kernel)
    update_result_image(sharpened)

# --------- فلاتر جديدة -----------

def apply_smoothing():
    if img is None:
        return
    smoothed = cv2.blur(img, (5,5))  # average filter
    update_result_image(smoothed)

def apply_spatial_filter():
    if img is None:
        return
    kernel = np.array([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]], np.float32) / 9
    filtered = cv2.filter2D(img, -1, kernel)
    update_result_image(filtered)

def apply_gaussian_blur():
    if img is None:
        return
    gaussian = cv2.GaussianBlur(img, (7,7), 1.5)
    update_result_image(gaussian)

def apply_thresholding():
    if img is None:
        return
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    thresh_bgr = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    update_result_image(thresh_bgr)

def save_result():
    global result_image
    if result_image is None:
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files", "*.png"),
                                                        ("JPEG files", "*.jpg"),
                                                        ("All files", ".")])
    if file_path:
        cv2.imwrite(file_path, result_image)

# ------------------- إعداد الواجهة ---------------------

root = Tk()
root.title("Image Processing Project - Full Filters")
root.geometry("1500x800")

style = ttk.Style()
style.configure("TButton",
                font=("Arial", 11),
                padding=5,
                relief="solid",
                borderwidth=2,
                width=25)

frame_left = Frame(root)
frame_left.pack(side="left", padx=10, pady=10, fill="y")

frame_center = Frame(root)
frame_center.pack(side="left", padx=10, pady=10)

frame_center_result = Frame(root)
frame_center_result.pack(side="left", padx=10, pady=10)

# ------------------- الأزرار ---------------------

# فريم الفلاتر
frame_filters = Frame(frame_left)
frame_filters.pack(pady=20)

# فريم التحميل والحفظ
frame_load_save = Frame(frame_left)
frame_load_save.pack(side="bottom", pady=20)

# أزرار الفلاتر الأساسية
filters = [
    ("Negative Image", apply_negative),
    ("Logarithmic Transform", apply_log),
    ("Gamma Correction", apply_gamma),
    ("Histogram Equalization", apply_hist_eq),
    ("Contrast Stretching", apply_contrast_stretch),
    ("Gaussian Blur", apply_blur),
    ("Edge Detection (Canny)", apply_edge_detection),
    ("Add Gaussian Noise", add_noise),
    ("Sharpen Image", apply_sharpen),
    ("Smoothing", apply_smoothing),
    ("Spatial Filter", apply_spatial_filter),
    ("Gaussian Blur (7x7)", apply_gaussian_blur),
    ("Thresholding", apply_thresholding)
]

for text, command in filters:
    btn = ttk.Button(frame_filters, text=text, command=command)
    btn.pack(pady=3)

# أزرار التحميل والحفظ
btn_load = ttk.Button(frame_load_save, text="Upload Image", command=load_image)
btn_load.pack(pady=10)

btn_save = ttk.Button(frame_load_save, text="Save Result", command=save_result)
btn_save.pack(pady=10)

root.mainloop()
