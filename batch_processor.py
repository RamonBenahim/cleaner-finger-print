#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from media_cleaner_bot import MediaCleanerBot
from advanced_cleaner import AdvancedMediaCleaner

class BatchProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Cleaner - Batch Processor")
        self.root.geometry("800x600")
        
        self.cleaner = MediaCleanerBot()
        self.advanced_cleaner = AdvancedMediaCleaner()
        self.selected_files = []
        self.processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        ttk.Label(main_frame, text="Media Cleaner - Batch Processor", 
                 font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        
        ttk.Button(file_frame, text="Add Files", 
                  command=self.add_files).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Button(file_frame, text="Add Directory", 
                  command=self.add_directory).grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        ttk.Button(file_frame, text="Clear All", 
                  command=self.clear_files).grid(row=0, column=2, sticky=tk.W)
        
        self.file_listbox = tk.Listbox(file_frame, height=8)
        self.file_listbox.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.grid(row=1, column=3, sticky=(tk.N, tk.S), pady=(10, 0))
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        options_frame = ttk.LabelFrame(main_frame, text="Processing Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.remove_exif_var = tk.BooleanVar(value=True)
        self.remove_metadata_var = tk.BooleanVar(value=True)
        self.randomize_timestamps_var = tk.BooleanVar(value=True)
        self.rename_files_var = tk.BooleanVar(value=False)
        self.advanced_cleaning_var = tk.BooleanVar(value=False)
        self.backup_originals_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(options_frame, text="Remove EXIF Data", 
                       variable=self.remove_exif_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Remove Video Metadata", 
                       variable=self.remove_metadata_var).grid(row=0, column=1, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Randomize Timestamps", 
                       variable=self.randomize_timestamps_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Rename Files", 
                       variable=self.rename_files_var).grid(row=1, column=1, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Advanced Cleaning", 
                       variable=self.advanced_cleaning_var).grid(row=2, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Backup Originals", 
                       variable=self.backup_originals_var).grid(row=2, column=1, sticky=tk.W)
        
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(0, weight=1)
        
        self.process_button = ttk.Button(control_frame, text="Start Processing", 
                                        command=self.start_processing)
        self.process_button.grid(row=0, column=0, sticky=tk.W)
        
        self.stop_button = ttk.Button(control_frame, text="Stop", 
                                     command=self.stop_processing, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(progress_frame, textvariable=self.progress_var).grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Media Files",
            filetypes=[
                ("All Supported", "*.jpg;*.jpeg;*.png;*.tiff;*.bmp;*.mp4;*.avi;*.mov;*.mkv;*.wmv"),
                ("Image Files", "*.jpg;*.jpeg;*.png;*.tiff;*.bmp"),
                ("Video Files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv"),
                ("All Files", "*.*")
            ]
        )
        
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
        
        self.log(f"Added {len(files)} files")

    def add_directory(self):
        directory = filedialog.askdirectory(title="Select Directory")
        if directory:
            supported_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', 
                                  '.mp4', '.avi', '.mov', '.mkv', '.wmv']
            
            added_count = 0
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = os.path.splitext(file)[1].lower()
                    
                    if file_ext in supported_extensions and file_path not in self.selected_files:
                        self.selected_files.append(file_path)
                        self.file_listbox.insert(tk.END, os.path.relpath(file_path, directory))
                        added_count += 1
            
            self.log(f"Added {added_count} files from directory: {directory}")

    def clear_files(self):
        self.selected_files.clear()
        self.file_listbox.delete(0, tk.END)
        self.log("File list cleared")

    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def update_progress(self, current, total, message=""):
        if total > 0:
            progress = (current / total) * 100
            self.progress_bar['value'] = progress
            self.progress_var.set(f"Processing {current}/{total} files... {message}")
        else:
            self.progress_var.set(message)
        self.root.update_idletasks()

    def start_processing(self):
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select files to process")
            return
        
        if self.processing:
            return
        
        self.processing = True
        self.process_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self.update_cleaner_config()
        
        thread = threading.Thread(target=self.process_files)
        thread.daemon = True
        thread.start()

    def stop_processing(self):
        self.processing = False
        self.process_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log("Processing stopped by user")

    def update_cleaner_config(self):
        self.cleaner.config.update({
            'remove_exif': self.remove_exif_var.get(),
            'remove_video_metadata': self.remove_metadata_var.get(),
            'randomize_timestamps': self.randomize_timestamps_var.get(),
            'rename_files': self.rename_files_var.get(),
            'backup_originals': self.backup_originals_var.get()
        })

    def process_files(self):
        total_files = len(self.selected_files)
        successful = 0
        failed = 0
        
        self.log(f"Starting batch processing of {total_files} files...")
        self.progress_bar['maximum'] = total_files
        
        for i, file_path in enumerate(self.selected_files):
            if not self.processing:
                break
            
            try:
                filename = os.path.basename(file_path)
                self.update_progress(i + 1, total_files, f"Processing {filename}")
                
                if self.advanced_cleaning_var.get():
                    result = self.advanced_cleaner.advanced_clean_single_file(
                        file_path, self.rename_files_var.get()
                    )
                else:
                    result = self.cleaner.clean_single_file(
                        file_path, self.rename_files_var.get()
                    )
                
                if result['success']:
                    successful += 1
                    operations = ', '.join(result['operations'])
                    self.log(f"SUCCESS: {filename} - {operations}")
                else:
                    failed += 1
                    errors = ', '.join(result['errors'])
                    self.log(f"FAILED: {filename} - {errors}")
                    
            except Exception as e:
                failed += 1
                self.log(f"ERROR: {filename} - {str(e)}")
        
        self.processing = False
        self.process_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        self.log(f"Batch processing complete!")
        self.log(f"Total: {total_files}, Successful: {successful}, Failed: {failed}")
        self.progress_var.set(f"Complete: {successful}/{total_files} successful")
        
        messagebox.showinfo("Processing Complete", 
                           f"Batch processing finished!\n\n"
                           f"Total files: {total_files}\n"
                           f"Successful: {successful}\n"
                           f"Failed: {failed}")

def main():
    root = tk.Tk()
    app = BatchProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()