import tkinter as tk
import tkinter.scrolledtext as st
from tkinter.simpledialog import askstring
from tkinter import messagebox
import socket
from time import sleep
import threading
from cryptography.fernet import Fernet
import random

# main window
window = tk.Tk()
window.title("Pychat")
window.geometry("500x355")

HOST = askstring("Logon", "Enter IP adress of server")

PORT = 12160 #3000

BUFFER_SIZE = 1024

USERNAME = askstring("Logon", "Select a username")

keys = []
keyfile = open("keys.txt","r")
keyfile.readline()
for key in keyfile.readlines():
    keys.append(key)
keyfile.close()

message = ""
receivemsg = ""

def connection_error():
    messagebox.showerror(title="Connection error!", message=f"Unable to establish connection to server at {HOST} : {PORT}")

def decode(text):
    for key in keys:
        f = Fernet(key)
        try:
            return (f.decrypt(text))
        except:
            pass

def enterpressed(placeholder_dont_remove):
    message = textwin.get()
    textwin.delete(0,"end")
    Send_message(message)

def receive():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 3001))
    s.listen(5)
    while True:
        global receivemsg
        #accept the connection
        client_connection, client_address = s.accept()
        #receive the data
        request_data = client_connection.recv(BUFFER_SIZE)
        #decode data from binary to uft-8
        try:
            receivemsg = decode(request_data).decode("utf-8") + "\n"
        except:
            pass
        

def update():
    global receivemsg
    if receivemsg != "":
        txt.config(state="normal")
        txt.insert("insert",receivemsg)
    receivemsg = ""
    txt.see("end")
    txt.config(state="disabled")
    window.after(1,update)

def Send_message(MESSAGE):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    MESSAGE = USERNAME + ": " + MESSAGE
    rkey = random.choice(keys)
    coder = Fernet(rkey.encode())
    s.send(coder.encrypt(MESSAGE.encode()))
    s.close()

#check if server is online
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    s.connect((HOST, PORT))
    s.close()
except:
    connection_error()
    exit()
    
textwin = tk.Entry(window, width = 500, font=("arial", 20))


textwin.bind("<Return>", enterpressed)
txt = st.ScrolledText(window, undo=True)
txt.insert(tk.INSERT, message)

txt.pack()
txt.config(state="disabled")
textwin.pack()
x = threading.Thread(target=receive)
x.start()
Send_message("has entered the realm!")
update()
window.mainloop()
