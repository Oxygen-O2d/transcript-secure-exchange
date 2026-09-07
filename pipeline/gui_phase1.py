import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase1_symmetric.encryption import encrypt_aes_cbc, encrypt_3des_cbc
from phase1_symmetric.ecb_vs_cbc import encrypt_image_ecb, encrypt_image_cbc

class CryptoDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Phase 1: Cryptography Tools")
        self.geometry("1000x700")
        
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.tab_file = self.tabview.add("File Encryption")
        self.tab_img = self.tabview.add("ECB vs CBC Leakage")
        
        self.setup_file_tab()
        self.setup_img_tab()
        
    def setup_file_tab(self):
        self.file_path_var = ctk.StringVar(value="No file selected")
        
        ctk.CTkLabel(self.tab_file, text="Select any text or binary file to encrypt:", font=("Arial", 16)).pack(pady=10)
        
        row_frame = ctk.CTkFrame(self.tab_file, fg_color="transparent")
        row_frame.pack(pady=10)
        
        ctk.CTkButton(row_frame, text="Browse File", command=self.browse_file).pack(side="left", padx=10)
        ctk.CTkLabel(row_frame, textvariable=self.file_path_var).pack(side="left", padx=10)
        
        self.enc_btn = ctk.CTkButton(self.tab_file, text="Encrypt File (AES & 3-DES)", command=self.encrypt_file, state="disabled")
        self.enc_btn.pack(pady=20)
        
        self.file_log = ctk.CTkTextbox(self.tab_file, width=600, height=300, state="disabled")
        self.file_log.pack(pady=10)
        
    def browse_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.file_path_var.set(filepath)
            self.enc_btn.configure(state="normal")
            
    def encrypt_file(self):
        filepath = self.file_path_var.get()
        if not os.path.exists(filepath):
            return
            
        with open(filepath, 'rb') as f:
            data = f.read()
            
        self.file_log.configure(state="normal")
        self.file_log.delete("1.0", "end")
        self.file_log.insert("end", f"File: {os.path.basename(filepath)}\nSize: {len(data)} bytes\n\n")
        
        key_16 = os.urandom(16)
        key_24 = os.urandom(24)
        
        # AES
        start = time.perf_counter()
        aes_iv, aes_ct = encrypt_aes_cbc(key_16, data)
        aes_time = time.perf_counter() - start
        self.file_log.insert("end", f"[AES-128 CBC]\nTime taken: {aes_time:.6f} seconds\n")
        
        # 3DES
        start = time.perf_counter()
        des_iv, des_ct = encrypt_3des_cbc(key_24, data)
        des_time = time.perf_counter() - start
        self.file_log.insert("end", f"\n[3-DES CBC]\nTime taken: {des_time:.6f} seconds\n")
        
        # Save them
        out_aes = filepath + ".aes.enc"
        out_des = filepath + ".3des.enc"
        with open(out_aes, 'wb') as f: f.write(aes_iv + aes_ct)
        with open(out_des, 'wb') as f: f.write(des_iv + des_ct)
        
        self.file_log.insert("end", f"\nSuccess! Encrypted files saved securely next to the original file:\n- {os.path.basename(out_aes)}\n- {os.path.basename(out_des)}")
        self.file_log.configure(state="disabled")

    def setup_img_tab(self):
        ctk.CTkLabel(self.tab_img, text="Select an Image to demonstrate ECB Pattern Leakage", font=("Arial", 16)).pack(pady=10)
        
        self.img_btn = ctk.CTkButton(self.tab_img, text="Browse Image", command=self.browse_image)
        self.img_btn.pack(pady=10)
        
        # Image Display Frame
        self.img_frame = ctk.CTkFrame(self.tab_img, fg_color="transparent")
        self.img_frame.pack(fill="both", expand=True, pady=10)
        
        self.lbl_orig = ctk.CTkLabel(self.img_frame, text="Original Image")
        self.lbl_ecb = ctk.CTkLabel(self.img_frame, text="ECB Mode (Vulnerable!)")
        self.lbl_cbc = ctk.CTkLabel(self.img_frame, text="CBC Mode (Secure)")
        
        self.lbl_orig.grid(row=0, column=0, padx=10, pady=5)
        self.lbl_ecb.grid(row=0, column=1, padx=10, pady=5)
        self.lbl_cbc.grid(row=0, column=2, padx=10, pady=5)
        
        self.img_orig_disp = ctk.CTkLabel(self.img_frame, text="")
        self.img_ecb_disp = ctk.CTkLabel(self.img_frame, text="")
        self.img_cbc_disp = ctk.CTkLabel(self.img_frame, text="")
        
        self.img_orig_disp.grid(row=1, column=0, padx=10)
        self.img_ecb_disp.grid(row=1, column=1, padx=10)
        self.img_cbc_disp.grid(row=1, column=2, padx=10)
        
        self.img_frame.grid_columnconfigure((0,1,2), weight=1)

    def browse_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if not filepath:
            return
            
        base_dir = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        
        # Convert to 24-bit BMP under the hood for clean encryption 
        # (Compressed formats like PNG break if you scramble their raw bytes)
        bmp_path = os.path.join(base_dir, "temp_target.bmp")
        try:
            with Image.open(filepath) as img:
                img = img.convert("RGB")
                img.save(bmp_path, format="BMP")
        except Exception as e:
            print(f"Error converting image: {e}")
            return
            
        ecb_path = os.path.join(base_dir, f"ECB_LEAKAGE_{filename}.bmp")
        cbc_path = os.path.join(base_dir, f"CBC_SECURE_{filename}.bmp")
        
        key = os.urandom(16)
        iv = os.urandom(16)
        
        # Encrypt
        encrypt_image_ecb(bmp_path, ecb_path, key)
        encrypt_image_cbc(bmp_path, cbc_path, key, iv)
        
        # Display on GUI
        self.load_and_display(bmp_path, self.img_orig_disp)
        self.load_and_display(ecb_path, self.img_ecb_disp)
        self.load_and_display(cbc_path, self.img_cbc_disp)
        
        # Cleanup temp
        if os.path.exists(bmp_path):
            os.remove(bmp_path)
            
    def load_and_display(self, path, label_widget):
        try:
            # We open with PIL, load into CTkImage
            img = Image.open(path)
            # Resize for display nicely
            img.thumbnail((300, 300))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            label_widget.configure(image=ctk_img, text="")
        except Exception as e:
            label_widget.configure(text="Error loading image")

if __name__ == "__main__":
    app = CryptoDashboard()
    app.mainloop()
