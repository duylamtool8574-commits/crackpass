import tkinter as tk
from tkinter import ttk, messagebox
import threading
import itertools
import string
import time

# Charset mặc định
charset = string.digits + string.ascii_letters

class CrackPassApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CrackPass Complete Tool")
        self.running = False

        tk.Label(root, text="Target Password:").pack(pady=5)
        self.target_entry = tk.Entry(root, show="*")
        self.target_entry.pack(pady=5)

        self.start_btn = tk.Button(root, text="Start Attack", command=self.start_attack)
        self.start_btn.pack(pady=5)

        self.stop_btn = tk.Button(root, text="Stop", command=self.stop_attack, state=tk.DISABLED)
        self.stop_btn.pack(pady=5)

        self.progress = ttk.Progressbar(root, length=300)
        self.progress.pack(pady=10)

        self.log = tk.Text(root, height=10, width=40)
        self.log.pack(pady=5)

    def start_attack(self):
        self.target_password = self.target_entry.get()
        if not self.target_password:
            messagebox.showerror("Error", "Please enter a target password.")
            return
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.log.delete("1.0", tk.END)
        self.thread = threading.Thread(target=self.brute_force)
        self.thread.start()

    def stop_attack(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log.insert(tk.END, "Attack stopped by user.\n")

    def brute_force(self):
        found = False
        length = len(self.target_password)
        total_combinations = len(charset) ** length
        count = 0

        for attempt in itertools.product(charset, repeat=length):
            if not self.running:
                break
            guess = ''.join(attempt)
            count += 1
            self.progress['value'] = (count / total_combinations) * 100
            self.log.delete("1.0", tk.END)
            self.log.insert(tk.END, f"Trying: {guess}\n")
            self.root.update()
            time.sleep(0.01)  # Thêm delay để GUI cập nhật

            if guess == self.target_password:
                found = True
                break

        if found:
            messagebox.showinfo("Success", f"Password found: {self.target_password}")
        else:
            if self.running:
                messagebox.showinfo("Finished", "Password not found.")
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CrackPassApp(root)
    root.mainloop()
