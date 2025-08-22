import tkinter as tk
import random
import time
import threading

# Random password 6 số (000000 - 999999)
password = str(random.randint(0, 9999999)).zfill(6)

# Hàm brute-force
def brute_force(label, result_label, button):
    button.config(state="disabled")  # vô hiệu hóa nút khi đang brute-force
    for guess in range(100000):  # từ 000000 -> 999999
        guess_str = str(guess).zfill(6)
        label.config(text=f"🔐 Trying: {guess_str}")
        label.update()

        time.sleep(0.0005)  # delay một chút để thấy nó chạy

        if guess_str == password:
            result_label.config(text=f"✅ Password cracked: {guess_str}")
            break
    button.config(state="normal")  # bật lại nút

# Hàm chạy thread để không bị treo GUI
def start_attack(label, result_label, button):
    t = threading.Thread(target=brute_force, args=(label, result_label, button))
    t.start()

# GUI
root = tk.Tk()
root.title("crack pass")
root.geometry("400x200")

label = tk.Label(root, text="Click 'Start Attack' to begin...", font=("Arial", 12))
label.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14), fg="green")
result_label.pack(pady=10)

start_button = tk.Button(root, text="🚀 Start Attack", font=("Arial", 12),
                         command=lambda: start_attack(label, result_label, start_button))
start_button.pack(pady=20)

root.mainloop()

