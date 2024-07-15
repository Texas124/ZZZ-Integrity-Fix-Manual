import tkinter as tk
from tkinter import messagebox
import os

class ZZZIntegrityPatcher:
    def __init__(self, root):
        self.root = root
        self.root.title("ZZZ Integrity Patcher")
        
        self.remote_files = {
            "audio": "audio_version_remote",
            "data": "data_version_remote",
            "res": "res_version_remote",
            "silence": "silence_version_remote"
        }
        
        self.persist_files = {
            "audio": "audio_version_persist",
            "data": "data_version_persist",
            "res": "res_version_persist",
            "silence": "silence_version_persist"
        }
        
        self.revision_fields = {}
        
        self.create_widgets()
        
    def create_widgets(self):
        # Locate remote file button
        self.locate_btn = tk.Button(self.root, text="Locate remote file", command=self.locate_remote_file)
        self.locate_btn.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Remote file count label
        self.remote_file_label = tk.Label(self.root, text="Remote file count")
        self.remote_file_label.grid(row=1, column=0)
        self.remote_file_count = tk.Label(self.root, text="0")
        self.remote_file_count.grid(row=1, column=1)
        
        # Revision fields
        tk.Label(self.root, text="Enter revision number").grid(row=2, column=0, columnspan=2)
        
        for idx, key in enumerate(self.remote_files.keys(), start=3):
            tk.Label(self.root, text=key).grid(row=idx, column=0)
            self.revision_fields[key] = tk.Entry(self.root, state='disabled')
            self.revision_fields[key].grid(row=idx, column=1)
        
        # Patch button
        self.patch_btn = tk.Button(self.root, text="Patch!", command=self.patch, state='disabled')
        self.patch_btn.grid(row=len(self.remote_files) + 3, column=0, columnspan=2, pady=10)
    
    def locate_remote_file(self):
        base_path = os.path.join(os.getcwd(), "ZenlessZoneZero Game", "ZenlessZoneZero_Data", "Persistent")
        remote_files_count = 0
        
        for key, filename in self.remote_files.items():
            if os.path.exists(os.path.join(base_path, filename)):
                self.revision_fields[key].config(state='normal')
                remote_files_count += 1
            else:
                self.revision_fields[key].config(state='disabled')
        
        self.remote_file_count.config(text=str(remote_files_count))
        
        if remote_files_count == 0:
            messagebox.showwarning("Warning", "Remote file not found!")
        else:
            self.patch_btn.config(state='normal')
    
    def patch(self):
        base_path = os.path.join(os.getcwd(), "ZenlessZoneZero Game", "ZenlessZoneZero_Data", "Persistent")
        
        for key, remote_filename in self.remote_files.items():
            persist_filename = self.persist_files[key]
            remote_path = os.path.join(base_path, remote_filename)
            persist_path = os.path.join(base_path, persist_filename)
            
            if os.path.exists(remote_path):
                if os.path.exists(persist_path):
                    os.remove(persist_path)
                os.rename(remote_path, persist_path)
        
        for key, entry in self.revision_fields.items():
            revision_filename = f"{key}_revision"
            revision_txt_filename = f"{revision_filename}.txt"
            revision_path = os.path.join(base_path, revision_filename)
            revision_txt_path = os.path.join(base_path, revision_txt_filename)
            
            if entry.get():
                if os.path.exists(revision_path):
                    os.remove(revision_path)
                with open(revision_txt_path, 'w') as file:
                    file.write(entry.get())
                os.rename(revision_txt_path, revision_path)
        
        patch_log_path = os.path.join(os.getcwd(), "patch_log.txt")
        with open(patch_log_path, 'a') as log_file:
            log_file.write("Patch applied successfully.\n")
        
        for entry in self.revision_fields.values():
            entry.config(state='disabled')
        
        self.patch_btn.config(state='disabled')
        messagebox.showinfo("Success", "Patch applied successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZZZIntegrityPatcher(root)
    root.mainloop()
