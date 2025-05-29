import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import os

class CurrencyDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💵 Fake Currency Detection")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f2f5")

        self.templates = {}  # dictionary {denomination: image}
        self.input_img = None

        # Load all templates
        template_folder = "templates"
        if not os.path.exists(template_folder):
            messagebox.showerror("Error", f'Please create a "{template_folder}" folder with template images.')
            root.destroy()
            return

        # Supported denominations expected as filenames like 10.jpg, 20.jpg, ...
        for file in os.listdir(template_folder):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                denom = os.path.splitext(file)[0]  # filename without extension
                img_path = os.path.join(template_folder, file)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    self.templates[denom] = img

        if not self.templates:
            messagebox.showerror("Error", f'No template images found in "{template_folder}" folder.')
            root.destroy()
            return

        # Title
        tk.Label(root, text="Fake Currency Detection System", font=("Helvetica", 20, "bold"), bg="#f0f2f5", fg="#333").pack(pady=10)

        # Frame only for input currency image (no template frame at start)
        self.frame_input = tk.LabelFrame(root, text="Input Currency Image", font=("Arial", 12), bg="white", bd=2)
        self.frame_input.place(x=250, y=70, width=300, height=230)

        # Canvas for input image
        self.canvas_input = tk.Label(self.frame_input, bg="white")
        self.canvas_input.pack(expand=True)

        # Canvas for matched template image (shown only after detection)
        self.frame_template = tk.LabelFrame(root, text="Matched Template Note", font=("Arial", 12), bg="white", bd=2)
        self.frame_template.place(x=50, y=70, width=180, height=140)
        self.canvas_template = tk.Label(self.frame_template, bg="white")
        self.canvas_template.pack(expand=True)

        # Result Label
        self.result_label = tk.Label(root, text="Upload an image and click Detect", font=("Arial", 14), bg="#f0f2f5", fg="#444")
        self.result_label.place(x=220, y=320)

        # Buttons
        self.upload_btn = tk.Button(root, text="📁 Upload Image", command=self.upload_image, font=("Arial", 11), bg="#4CAF50", fg="white", width=15)
        self.upload_btn.place(x=200, y=370)

        self.detect_btn = tk.Button(root, text="🔍 Detect Fake", command=self.detect_fake, font=("Arial", 11), bg="#2196F3", fg="white", width=15)
        self.detect_btn.place(x=420, y=370)

    def show_image(self, img_cv, canvas, size=(280, 180)):
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_GRAY2RGB)
        img_pil = Image.fromarray(img_rgb).resize(size)
        img_tk = ImageTk.PhotoImage(img_pil)
        canvas.img = img_tk
        canvas.config(image=img_tk)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not file_path:
            return
        self.input_img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if self.input_img is None:
            messagebox.showerror("Error", "Failed to load image. Please select a valid image file.")
            return
        self.show_image(self.input_img, self.canvas_input)
        self.result_label.config(text="Image uploaded. Click Detect.", fg="#444")

        # Clear previous template match image and result
        self.canvas_template.config(image='')
        self.result_label.config(text="Image uploaded. Click Detect.", fg="#444")

    def detect_fake(self):
        if self.input_img is None:
            messagebox.showerror("Error", "Please upload an input image first.")
            return

        best_score = -1
        best_denom = None

        for denom, tmpl_img in self.templates.items():
            try:
                resized_input = cv2.resize(self.input_img, (tmpl_img.shape[1], tmpl_img.shape[0]))
            except Exception as e:
                messagebox.showerror("Error", f"Error resizing images: {e}")
                return

            corr_val = np.corrcoef(tmpl_img.flatten(), resized_input.flatten())[0, 1]

            if corr_val > best_score:
                best_score = corr_val
                best_denom = denom

        # Show matched template image
        self.show_image(self.templates[best_denom], self.canvas_template, size=(160, 100))

        threshold = 0.9
        if best_score > threshold:
            self.result_label.config(text=f"✅ Detected PKR {best_denom} - Likely Real (Score: {best_score:.2f})", fg="green")
        else:
            self.result_label.config(text=f"❌ Detected PKR {best_denom} - Likely Fake (Score: {best_score:.2f})", fg="red")

# Launch app
root = tk.Tk()
app = CurrencyDetectorApp(root)
root.mainloop()
