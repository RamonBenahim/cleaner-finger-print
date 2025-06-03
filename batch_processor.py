#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
from advanced_cleaner import AdvancedMediaCleaner

class BatchProcessorGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Media Fingerprint Remover")
        self.root.geometry("800x600")
        
        self.cleaner = AdvancedMediaCleaner()
        self.selected_files = []
        self.processing = False
        
        self._create_widgets()
        
    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        ttk.Label(main_frame, text="Advanced Media Fingerprint Remover", 
                 font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        
        ttk.Button(file_frame, text="Add Files", 
                  command=self._add_files).grid(row=0, column=0, padx=(0, 5), sticky=tk.W)
        ttk.Button(file_frame, text="Add Directory", 
                  command=self._add_directory).grid(row=0, column=1, padx=5, sticky=tk.W)
        ttk.Button(file_frame, text="Clear All", 
                  command=self._clear_files).grid(row=0, column=2, padx=(5, 0), sticky=tk.W)
        
        self.file_count_label = ttk.Label(file_frame, text="Files selected: 0")
        self.file_count_label.grid(row=0, column=3, sticky=tk.E)
        
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        options_frame = ttk.LabelFrame(main_frame, text="Processing Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.remove_exif_var = tk.BooleanVar(value=True)
        self.remove_metadata_var = tk.BooleanVar(value=True)
        self.randomize_timestamps_var = tk.BooleanVar(value=True)
        self.backup_files_var = tk.BooleanVar(value=True)
        self.advanced_mode_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(options_frame, text="Remove EXIF data", 
                       variable=self.remove_exif_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Remove video metadata", 
                       variable=self.remove_metadata_var).grid(row=0, column=1, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Randomize timestamps", 
                       variable=self.randomize_timestamps_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Backup original files", 
                       variable=self.backup_files_var).grid(row=1, column=1, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Advanced steganography removal", 
                       variable=self.advanced_mode_var).grid(row=2, column=0, columnspan=2, sticky=tk.W)
        
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(1, weight=1)
        
        self.process_button = ttk.Button(control_frame, text="Start Processing", 
                                        command=self._start_processing)
        self.process_button.grid(row=0, column=0, padx=(0, 10))
        
        self.progress = ttk.Progressbar(control_frame, mode='determinate')
        self.progress.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.status_label = ttk.Label(control_frame, text="Ready")
        self.status_label.grid(row=0, column=2)
        
        log_frame = ttk.LabelFrame(main_frame, text="Processing Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        main_frame.rowconfigure(5, weight=1)
    
    def _add_files(self):
        filetypes = [
            ("All supported", "*.jpg;*.jpeg;*.png;*.tiff;*.bmp;*.mp4;*.avi;*.mov;*.mkv;*.wmv"),
            ("Image files", "*.jpg;*.jpeg;*.png;*.tiff;*.bmp"),
            ("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select media files to clean",
            filetypes=filetypes
        )
        
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
        
        self._update_file_count()
    
    def _add_directory(self):
        directory = filedialog.askdirectory(title="Select directory containing media files")
        
        if directory:
            supported_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp', 
                                  '.mp4', '.avi', '.mov', '.mkv', '.wmv'}
            
            for root, _, files in os.walk(directory):
                for file in files:
                    if Path(file).suffix.lower() in supported_extensions:
                        file_path = os.path.join(root, file)
                        if file_path not in self.selected_files:
                            self.selected_files.append(file_path)
                            self.file_listbox.insert(tk.END, os.path.relpath(file_path, directory))
            
            self._update_file_count()
    
    def _clear_files(self):
        self.selected_files.clear()
        self.file_listbox.delete(0, tk.END)
        self._update_file_count()
    
    def _update_file_count(self):
        count = len(self.selected_files)
        self.file_count_label.config(text=f"Files selected: {count}")
    
    def _log_message(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def _start_processing(self):
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select files to process.")
            return
        
        if self.processing:
            return
        
        self.processing = True
        self.process_button.config(text="Processing...", state="disabled")
        self.log_text.delete(1.0, tk.END)
        
        self.cleaner.config.update({
            'remove_exif': self.remove_exif_var.get(),
            'remove_video_metadata': self.remove_metadata_var.get(),
            'randomize_timestamps': self.randomize_timestamps_var.get(),
            'backup_originals': self.backup_files_var.get()
        })
        
        thread = threading.Thread(target=self._process_files)
        thread.daemon = True
        thread.start()
    
    def _process_files(self):
        total_files = len(self.selected_files)
        processed = 0
        failed = 0
        
        self.progress.config(maximum=total_files, value=0)
        
        for i, file_path in enumerate(self.selected_files):
            try:
                self._log_message(f"Processing: {os.path.basename(file_path)}")
                
                if self.advanced_mode_var.get():
                    result = self.cleaner.advanced_clean_single_file(file_path)
                else:
                    result = self.cleaner.clean_single_file(file_path)
                
                if result['success']:
                    processed += 1
                    operations = ', '.join(result['operations'])
                    self._log_message(f"✅ Success: {operations}")
                    
                    if 'entropy' in result:
                        self._log_message(f"   Entropy: {result['entropy']:.2f}, Risk: {result['steganography_risk']}")
                else:
                    failed += 1
                    errors = ', '.join(result['errors'])
                    self._log_message(f"❌ Failed: {errors}")
                
            except Exception as e:
                failed += 1
                self._log_message(f"❌ Error processing {os.path.basename(file_path)}: {str(e)}")
            
            self.progress.config(value=i + 1)
            self.status_label.config(text=f"Processing {i + 1}/{total_files}")
            self.root.update_idletasks()
        
        self._log_message(f"\n📊 Processing complete!")
        self._log_message(f"Total files: {total_files}")
        self._log_message(f"Processed successfully: {processed}")
        self._log_message(f"Failed: {failed}")
        
        self.processing = False
        self.process_button.config(text="Start Processing", state="normal")
        self.status_label.config(text="Complete")
        
        messagebox.showinfo("Processing Complete", 
                           f"Processed {processed}/{total_files} files successfully.")

def main():
    root = tk.Tk()
    app = BatchProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()