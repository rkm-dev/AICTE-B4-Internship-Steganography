import customtkinter as ctk
from PIL import Image
import threading
import time
import cv2
import os
import tkinter as tk

# import custom encryption logic
import encryption

# import custom decryption logic
import decryption

# Global variable for passcode
pass_code = ""
msg_len = 0


class Window1(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x400")
        self.title("Encryption Program")
        self.configure(fg_color="black")

        # Back button in top-left corner
        back_button = ctk.CTkButton(self, text="<", width=40, height=40, 
                                  command=self.destroy, corner_radius=10)
        back_button.place(x=10, y=10)

        # Add submit image button
        submit_button = ctk.CTkButton(self, text="Select Image", 
                                    command=self.select_image,
                                    width=180, height=40)
        submit_button.place(relx=0.5, rely=0.4, anchor="center")

        # Add secret message input box
        self.secret_message = ctk.CTkEntry(self, width=180, height=40, 
                                         placeholder_text="Enter secret message")
        self.secret_message.place(relx=0.5, rely=0.55, anchor="center")

        # Add passcode input box
        self.passcode = ctk.CTkEntry(self, width=180, height=40,
                                   placeholder_text="Enter passcode",
                                   show="*")  # This masks the input with *
        self.passcode.place(relx=0.5, rely=0.7, anchor="center")

        # Add encrypt button
        encrypt_button = ctk.CTkButton(self, text="Encrypt", 
                                        command=self.encrypt_message,
                                        width=180, height=40)
        encrypt_button.place(relx=0.5, rely=0.85, anchor="center")  # Placed below passcode

    def select_image(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.selected_image_path = file_path
            print(f"Selected image path: {self.selected_image_path}")

    def encrypt_message(self):
        global pass_code  # Access the global variable
        global msg_len
        secret = self.secret_message.get()
        msg_len = len(secret)
        pass_code = self.passcode.get()  # Store the passcode in global variable
        print(f"Encrypting message: {secret} with passcode: {pass_code}")

        # Check if all fields are filled
        if hasattr(self, 'selected_image_path') and secret and pass_code:
            # Show progress bar
            self.progress_bar = ctk.CTkProgressBar(self, width=180, height=20)
            self.progress_bar.place(relx=0.5, rely=0.95, anchor="center")

            # Start encryption in a separate thread
            self.encrypt_thread = threading.Thread(target=self.perform_encryption, args=(self.selected_image_path, secret, pass_code))
            self.encrypt_thread.start()
        else:
            # Show error message
            self.error_window = tk.Toplevel(self)
            self.error_window.title("Error")
            tk.Label(self.error_window, text="Please select an image and enter a message and passcode.").pack(pady=10)
            tk.Button(self.error_window, text="OK", command=self.error_window.destroy).pack()
            self.error_window.update_idletasks()  # Update the window to calculate its size
            screen_width = self.error_window.winfo_screenwidth()
            screen_height = self.error_window.winfo_screenheight()
            window_width = self.error_window.winfo_width()
            window_height = self.error_window.winfo_height()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            self.error_window.geometry(f"+{x}+{y}")
            
    def perform_encryption(self, selected_image_path, secret, pass_code):
        global msg_len
        # Update progress bar (example)
        for i in range(100):
            self.progress_bar.set(i)
            time.sleep(0.01)
        
        # Run encryption logic here
        img = cv2.imread(selected_image_path)
        extension = os.path.splitext(selected_image_path)[1]
        path = os.path.dirname(selected_image_path)
        
        encrypted_image = os.path.join(path , f"encryptedImage{extension}")
        print(encrypted_image)
        cv2.imwrite(encrypted_image, encryption.encypt(img, secret))
        
        # After encryption is done
        self.progress_bar.destroy()
        self.success_window = tk.Toplevel(self)
        self.success_window.title("Encryption Successful")
        tk.Label(self.success_window, text="Encryption Successful!").pack(pady=10)
        tk.Button(self.success_window, text="OK", command=self.success_window.destroy).pack()
        self.success_window.update_idletasks()  # Update the window to calculate its size
        screen_width = self.success_window.winfo_screenwidth()
        screen_height = self.success_window.winfo_screenheight()
        window_width = self.success_window.winfo_width()
        window_height = self.success_window.winfo_height()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.success_window.geometry(f"+{x}+{y}")


class Window2(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x400")
        self.title("Decryption Program")
        self.configure(fg_color="black")

        # Back button in top-left corner
        back_button = ctk.CTkButton(self, text="<", width=40, height=40,
                                  command=self.destroy, corner_radius=10)
        back_button.place(x=10, y=10)

        # Add "Open Encrypted Image" button
        open_image_button = ctk.CTkButton(self, text="Select Encrypted Image",
                                            command=self.open_encrypted_image,
                                            width=180, height=40)
        open_image_button.place(relx=0.5, rely=0.4, anchor="center")

        # Add passcode input box
        self.passcode_entry = ctk.CTkEntry(self, width=180, height=40,
                                   placeholder_text="Enter passcode",
                                   show="*")  # This masks the input with *
        self.passcode_entry.place(relx=0.5, rely=0.55, anchor="center")
        
        # Add Decrypt Button
        self.decrypt_button = ctk.CTkButton(self, text="Decrypt",
            command=self.decrypt_message,
            width=180, height=40)
        self.decrypt_button.place(relx=0.5, rely=0.7, anchor="center")

        # Add Message Title
        self.message_title = ctk.CTkLabel(self, text="",
        width=180, height=40,
        font=("Arial", 12))
        self.message_title.place(relx=0.5, rely=0.80, anchor="center")
        
        # Add Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, width=180, height=20)
        self.progress_bar.place(relx=0.5, rely=0.80, anchor="center")
        
        # Add Message Display Box
        self.message_label = ctk.CTkLabel(self, text="",
        width=180, height=40,
        font=("Arial", 16))
        self.message_label.place(relx=0.5, rely=0.90, anchor="center")

    def open_encrypted_image(self):
        from tkinter import filedialog
        self.encrypted_image_path = filedialog.askopenfilename(
            title="Select Encrypted Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        if self.encrypted_image_path:
            print(f"Selected encrypted image path: {self.encrypted_image_path}")
            # Implement decryption logic here using self.encrypted_image_path and pass_code

    def decrypt_message(self):
        global pass_code
        entered_passcode = self.passcode_entry.get()

        if not hasattr(self, 'encrypted_image_path'):
            self.show_error("Please select an encrypted image.")
            return
        if not entered_passcode:
            self.show_error("Please enter the passcode.")
            return
        if entered_passcode != pass_code:
            self.show_error("Not Authorized")
            return
        
        # Start decryption in a separate thread
        self.decrypt_thread = threading.Thread(target=self.perform_decryption)
        self.decrypt_thread.start()
        
    def perform_decryption(self):
        global msg_len
        # Update progress bar (example)
        for i in range(100):
            self.progress_bar.set(i)
            time.sleep(0.01)

        # Run decryption logic here
        img = cv2.imread(self.encrypted_image_path)
        
        decrypted_message = decryption.decrypt(img, msg_len)
        print("Decrypted message :", decrypted_message)
        
        # After decryption is done
        self.progress_bar.destroy()  # Reset progress bar
        self.message_title.configure(text="Decrypted Message")
        self.message_label.configure(text=decrypted_message)  # Display decrypted message
        
    def show_error(self, message):
        self.error_window = tk.Toplevel(self)
        self.error_window.title("Error")
        tk.Label(self.error_window, text=message).pack(pady=10)
        tk.Button(self.error_window, text="OK", command=self.error_window.destroy).pack()
        self.error_window.update_idletasks()  # Update the window to calculate its size
        screen_width = self.error_window.winfo_screenwidth()
        screen_height = self.error_window.winfo_screenheight()
        window_width = self.error_window.winfo_width()
        window_height = self.error_window.winfo_height()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.error_window.geometry(f"+{x}+{y}")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("300x400")
        self.title("DataSec")
        self.configure(fg_color="black")

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create frame for buttons and image
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=0, column=0, padx=20, pady=20)

        # Add image
        image = ctk.CTkImage(light_image=Image.open("attached_assets/crypto-gif.gif"),
                            dark_image=Image.open("attached_assets/crypto-gif.gif"),
                            size=(200, 200))
        image_label = ctk.CTkLabel(button_frame, image=image, text="")
        image_label.pack(pady=(0, 20))

        # Add buttons
        button1 = ctk.CTkButton(button_frame, text="Encryption", command=self.open_window1,
                               width=180, height=40)
        button1.pack(pady=10)

        button2 = ctk.CTkButton(button_frame, text="Decryption", command=self.open_window2,
                               width=180, height=40)
        button2.pack(pady=10)

        self.window1 = None
        self.window2 = None

    def open_window1(self):
        if self.window1 is None or not self.window1.winfo_exists():
            self.window1 = Window1(self)

    def open_window2(self):
        if self.window2 is None or not self.window2.winfo_exists():
            self.window2 = Window2(self)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = App()
    app.mainloop()