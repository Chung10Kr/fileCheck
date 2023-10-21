import tkinter as tk
from tkinter import filedialog,messagebox
import hashlib
import os

files_in_path1={};
files_in_path2={};

#md5 hash값 구하기
def generate_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f: # 바이너리 모드(rb)로 open
        for chunk in iter(lambda: f.read(4096), b""): # 4096씩 읽어옴
            hash_md5.update(chunk) 
    return hash_md5.hexdigest()

def browse_local():
    local_dir = filedialog.askdirectory()
    local_path_label.config(text=local_dir)

def browse_server():
    server_dir = filedialog.askdirectory()
    server_path_label.config(text=server_dir)


def get_files_in_path(path):
    files_in_path = {}
    for dirpath, dirnames, filenames in os.walk(path): # os.walk는 주어진 디렉토리와 그 하위 디렉토리를 탐색, 각 디렉토리에 대해 반환
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            files_in_path[f] = {
                 'fullPath' : full_path,
                 'md5' : generate_md5(full_path)
            }
    return files_in_path

def browse_and_compare():
    path1 = local_path_label.cget("text")
    path2 = server_path_label.cget("text")
    
    if not path1 or not path2:
        messagebox.showwarning("비교 대상 누략", "비교 대상을 선택해주세요")
        return
    
    files_in_path1 = get_files_in_path(path1)
    files_in_path2 = get_files_in_path(path2)
    
    only_in_path1 = {f:data for f, data in files_in_path1.items() if f not in files_in_path2}
    different_files = {f:data for f, data in files_in_path1.items() if (f in files_in_path2 and files_in_path2[f]['md5'] != data['md5'])}
    only_in_path2 = {f:data for f, data in files_in_path2.items() if (f not in files_in_path1)}

    for textarea in [textarea_only_in_1, textarea_diff, textarea_only_in_2]:
            textarea.configure(state='normal')
            textarea.delete(1.0, tk.END)

    textarea_only_in_1.insert(tk.END, "\n".join([data['fullPath'] for data in only_in_path1.values()]))
    textarea_diff.insert(tk.END, "\n".join([data['fullPath'] for data in different_files.values()]))
    textarea_only_in_2.insert(tk.END, "\n".join([data['fullPath'] for data in only_in_path2.values()]))

    for textarea in [textarea_only_in_1, textarea_diff, textarea_only_in_2]:
            textarea.configure(state='disabled')




root = tk.Tk() 

compare_button = tk.Button(root, text="compare", command=browse_and_compare)
compare_button.grid(row=0, column=0, rowspan=2, sticky='nsew')

local_button = tk.Button(root, text="Path 1", command=browse_local)
local_button.grid(row=0, column=1, sticky='nsew')

server_button = tk.Button(root, text="Path 2", command=browse_server)
server_button.grid(row=1, column=1, sticky='nsew')

local_path_label = tk.Label(root, text="")
local_path_label.grid(row=0, column=2)

server_path_label = tk.Label(root, text="")
server_path_label.grid(row=1, column=2)

path1_only_label=tk.Label(root,text="Path 1만 존재하는 파일")
path1_only_label.grid(row=2,column=0)
diff_only_label=tk.Label(root,text="서로 다른 파일")
diff_only_label.grid(row=2,column=1)
path2_only_label=tk.Label(root,text="Path 2만 존재하는 파일")
path2_only_label.grid(row=2,column=2)

textarea_only_in_1 = tk.Text(root, width=40,height=50)
textarea_only_in_1.insert(tk.END,"")
textarea_only_in_1.configure(state='disabled')
textarea_only_in_1.grid(row=3,column=0) 

textarea_diff = tk.Text(root,width=40,height=50)
textarea_diff.insert(tk.END,"")
textarea_diff.configure(state='disabled')
textarea_diff.grid(row=3,column=1) 

textarea_only_in_2=tk.Text(root,width=40,height=50)
textarea_only_in_2.insert(tk.END,"")
textarea_only_in_2.configure(state='disabled')
textarea_only_in_2.grid(row=3,column=2) 

root.mainloop()
