from datetime import datetime
import json
from poc import process_zip_file
import tkinter as tk
from tkinter import filedialog
import os 

start_time = datetime.now()
current_dir = os.getcwd()

root = tk.Tk()
root.withdraw()
# open file dialog in the current directory
file_path = filedialog.askopenfilename(initialdir=current_dir)
print("Reading JSON file...")

with open(file_path) as f:
    data = json.load(f)
    done = 0
    total = len(data)
    print(f"Processing {total} items...")

    for key, value in data.items():
        I_data = value["I"]
        J_data = value["J"]
        K_data = value["K"]

        FILENAME = key
        DATA = {"SKU": FILENAME, "i": I_data, "j": J_data, "k": K_data}

        # Uncomment and define your process_zip_file function to use it
        process_zip_file(FILENAME, DATA)

        # Update on completion for each item
        done += 1
        print(f"Completed {done}/{total}: {key}{' ' * 50}", end="\r")

# Ensure clear separation before final time output
print("\n" + "=" * 50)  # This creates a separation line for readability
end_time = datetime.now()
time_diff = end_time - start_time
seconds = time_diff.total_seconds()
print(f"Time taken: {seconds:.2f} seconds")
