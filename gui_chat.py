from tkinterdnd2 import TkinterDnD
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import shutil
import os

def upload_files(filepaths):
    if not os.path.exists("docs"):
        os.mkdir("docs")
    for path in filepaths:
        filename = os.path.basename(path)
        shutil.copy(path, os.path.join("docs", filename))
    try:
        res = requests.post("http://127.0.0.1:5000/build")
        messagebox.showinfo("建庫完成", res.json()["message"])
    except Exception as e:
        messagebox.showerror("建庫失敗", str(e))

def on_drop(event):
    filepaths = root.tk.splitlist(event.data)
    upload_files(filepaths)

def send_query():
    query = entry.get()
    try:
        res = requests.post("http://127.0.0.1:5000/query", json={"query": query})
        response = res.json().get("answer", "")
    except Exception as e:
        response = f"❌ 發送失敗：{e}"
    chat.insert(tk.END, f"🧑‍💻 你：{query}\n🤖 AI：{response}\n\n")
    chat.see(tk.END)

# ✅ 使用 TkinterDnD.Tk() 而不是 tk.Tk()
root = TkinterDnD.Tk()
root.title("RAG 對話系統")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

chat = tk.Text(frame, width=80, height=20)
chat.pack()

entry = tk.Entry(frame, width=80)
entry.pack()
entry.bind("<Return>", lambda e: send_query())

root.drop_target_register('DND_Files')
root.dnd_bind('<<Drop>>', on_drop)

tk.Label(root, text="請將文件拖進此視窗上傳並建立索引\n支援 .txt, .md, .pdf").pack()
root.mainloop()
