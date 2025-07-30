import os
import hashlib
import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from datetime import datetime

class FileIntegrityChecker:
    def __init__(self):
        self.exclude_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.mp3', 
                                 '.wav', '.jpg', '.jpeg', '.png', '.gif', 
                                 '.iso', '.zip', '.rar', '.7z']
        self.max_file_size = 100 * 1024 * 1024  # 100MB
        self.target_folders = []

    def calculate_hash(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                file_hash = hashlib.sha256()
                while chunk := f.read(8192):
                    file_hash.update(chunk)
            return file_hash.hexdigest()
        except Exception as e:
            return f"Error calculating hash: {str(e)}"

    def should_exclude(self, filepath):
        _, ext = os.path.splitext(filepath)
        if ext.lower() in self.exclude_extensions:
            return True
        
        try:
            if os.path.getsize(filepath) > self.max_file_size:
                return True
        except:
            pass
        
        return False

    def create_snapshot(self, baseline_file):
        results = []
        file_count = 0
        baseline_data = []
        
        # Count files first
        for folder in self.target_folders:
            for root, _, files in os.walk(folder):
                for file in files:
                    filepath = os.path.join(root, file)
                    if not self.should_exclude(filepath):
                        file_count += 1
        
        if file_count == 0:
            return ["No files found to process (may be excluded by filters)"]
        
        # Process files
        processed = 0
        for folder in self.target_folders:
            folder_index = self.target_folders.index(folder)
            for root, _, files in os.walk(folder):
                for file in files:
                    filepath = os.path.join(root, file)
                    if self.should_exclude(filepath):
                        continue
                    
                    relative_path = os.path.relpath(filepath, folder)
                    file_hash = self.calculate_hash(filepath)
                    
                    if file_hash and not file_hash.startswith("Error"):
                        baseline_data.append({
                            'folder_index': folder_index,
                            'path': relative_path,
                            'hash': file_hash,
                            'size': os.path.getsize(filepath),
                            'modified': os.path.getmtime(filepath)
                        })
                    
                    processed += 1
        
        # Save baseline
        try:
            with open(baseline_file, 'w', newline='') as csvfile:
                fieldnames = ['folder_index', 'path', 'hash', 'size', 'modified']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(baseline_data)
            
            results.append(f"Snapshot created with {len(baseline_data)} files")
            results.append(f"Baseline saved to: {baseline_file}")
        except Exception as e:
            results.append(f"Error saving baseline: {str(e)}")
        
        return results

    def verify_integrity(self, baseline_file):
        results = []
        
        # Load baseline
        try:
            with open(baseline_file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                baseline = []
                for row in reader:
                    row['folder_index'] = int(row['folder_index'])
                    baseline.append(row)
        except Exception as e:
            return [f"Error loading baseline: {str(e)}"]
        
        total_files = len(baseline)
        if total_files == 0:
            return ["Baseline file is empty"]
        
        modified = 0
        missing = 0
        verified = 0
        
        # Verify files
        for baseline_data in baseline:
            folder_index = baseline_data['folder_index']
            if folder_index >= len(self.target_folders):
                results.append(f"Warning: Baseline references folder index {folder_index} but only {len(self.target_folders)} folders are selected")
                continue
            
            folder = self.target_folders[folder_index]
            relative_path = baseline_data['path']
            filepath = os.path.join(folder, relative_path)
            
            if not os.path.exists(filepath):
                results.append(f"Missing: [{folder_index}] {relative_path}")
                missing += 1
                continue
            
            if self.should_exclude(filepath):
                continue
            
            current_hash = self.calculate_hash(filepath)
            current_size = os.path.getsize(filepath)
            current_modified = os.path.getmtime(filepath)
            
            if (current_hash != baseline_data['hash'] or 
                str(current_size) != baseline_data['size'] or 
                str(current_modified) != baseline_data['modified']):
                results.append(f"Modified: [{folder_index}] {relative_path}")
                modified += 1
            else:
                verified += 1
        
        # Summary
        results.append("\nVerification complete:")
        results.append(f"Total files checked: {total_files}")
        results.append(f"Verified (unchanged): {verified}")
        results.append(f"Modified: {modified}")
        results.append(f"Missing: {missing}")
        
        return results

def load_ui(frame, back_callback):
    checker = FileIntegrityChecker()
    
    # Clear the frame and setup back button
    for widget in frame.winfo_children():
        widget.destroy()
    
    tk.Button(frame, text="← Back", command=back_callback).pack(anchor="nw", padx=10, pady=10)
    
    # Main container
    main_frame = tk.Frame(frame)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Folder Selection
    tk.Label(main_frame, text="Target Folders:").pack(anchor='w')
    
    # Listbox with scrollbar
    list_frame = tk.Frame(main_frame)
    list_frame.pack(fill='x')
    
    folder_listbox = tk.Listbox(list_frame, height=5, selectmode=tk.EXTENDED)
    folder_listbox.pack(side='left', fill='x', expand=True)
    
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side='right', fill='y')
    folder_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=folder_listbox.yview)
    
    # Folder buttons
    btn_frame = tk.Frame(main_frame)
    btn_frame.pack(fill='x')
    
    def update_listbox():
        folder_listbox.delete(0, tk.END)
        for folder in checker.target_folders:
            folder_listbox.insert(tk.END, folder)
    
    def add_folder():
        folder = filedialog.askdirectory()
        if folder and folder not in checker.target_folders:
            checker.target_folders.append(folder)
            update_listbox()
    
    def remove_folder():
        selected = folder_listbox.curselection()
        for index in selected[::-1]:
            del checker.target_folders[index]
        update_listbox()
    
    def clear_folders():
        checker.target_folders = []
        update_listbox()
    
    tk.Button(btn_frame, text="Add Folder", command=add_folder).pack(side='left', padx=2)
    tk.Button(btn_frame, text="Remove Selected", command=remove_folder).pack(side='left', padx=2)
    tk.Button(btn_frame, text="Clear All", command=clear_folders).pack(side='left', padx=2)
    
    # Baseline File
    baseline_file = tk.StringVar(value="baseline.csv")
    tk.Label(main_frame, text="Baseline File:").pack(anchor='w', pady=(10, 0))
    
    baseline_frame = tk.Frame(main_frame)
    baseline_frame.pack(fill='x')
    
    baseline_entry = tk.Entry(baseline_frame, textvariable=baseline_file, width=50)
    baseline_entry.pack(side='left', fill='x', expand=True)
    
    def browse_baseline(save=False):
        if save:
            file = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile="baseline.csv"
            )
        else:
            file = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
        if file:
            baseline_file.set(file)
    
    tk.Button(baseline_frame, text="Browse", command=lambda: browse_baseline(save=True)).pack(side='right', padx=(5, 0))
    
    # Results area
    result_text = scrolledtext.ScrolledText(main_frame, height=15, wrap='word')
    result_text.pack(fill='both', expand=True, pady=(10, 0))
    
    # Action buttons
    action_frame = tk.Frame(main_frame)
    action_frame.pack(fill='x', pady=10)
    
    def create_snapshot():
        if not checker.target_folders:
            messagebox.showerror("Error", "Please add at least one target folder")
            return
        
        file = baseline_file.get()
        if not file:
            messagebox.showerror("Error", "Please specify a baseline file")
            return
        
        results = checker.create_snapshot(file)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "\n".join(results))
    
    def verify_integrity():
        if not checker.target_folders:
            messagebox.showerror("Error", "Please add at least one target folder")
            return
        
        file = baseline_file.get()
        if not file or not os.path.isfile(file):
            messagebox.showerror("Error", "Please specify a valid baseline file")
            return
        
        results = checker.verify_integrity(file)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "\n".join(results))
    
    tk.Button(action_frame, text="Create Snapshot", command=create_snapshot).pack(side='left', padx=5)
    tk.Button(action_frame, text="Verify Integrity", command=verify_integrity).pack(side='left', padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    
    # For testing the UI standalone
    def back():
        print("Back button pressed")
    
    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)
    load_ui(frame, back)
    
    root.geometry("700x600")
    root.title("File Integrity Checker")
    root.mainloop()


    