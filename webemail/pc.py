from tkinter.ttk import Combobox

import requests
import tkinter
from tkinter import *
import tkinter.messagebox


class app(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title = 'email'

        self.lable1 = Label(self.master, text='url')
        self.lable1.pack()
        self.entry1 = Entry(self.master)
        self.entry1.pack()

        self.lable2 = Label(self.master, text='title')
        self.lable2.pack()
        self.entry2 = Entry(self.master)
        self.entry2.pack()

        self.lable3 = Label(self.master, text='body')
        self.lable3.pack()
        self.text1 = Entry(self.master)
        self.text1.pack()

        self.lable4 = Label(self.master, text='method')
        self.lable4.pack()
        self.comvalue = tkinter.StringVar()
        self.box = Combobox(self.master, textvariable=self.comvalue)
        self.box["values"] = ("restful", "soap")
        self.box.pack()
        self.box.current(0)

        self.button1 = Button(
            self.master,
            text='send',
            command=lambda: self.send_email(
                self.entry1.get(),
                self.entry2.get(),
                self.text1.get(),
                self.comvalue.get()))
        self.button1.pack()

    def send_email(self, url, title, body, method):
        if method == 'restful':
            data = {
                'url': url,
                'title': title,
                'body': body,
            }
            res = requests.post('http://127.0.0.1:5000/email', data=data)
            tkinter.messagebox.showinfo('发送状态', '成功')
            # print(res)
        elif method == 'soap':
            res = requests.get(
                'http://localhost:5000/soap/sendemail?url=462194914@qq.com&title=title&body=123')
            print(res)
            tkinter.messagebox.showinfo('发送状态', '成功')


if __name__ == '__main__':
    root = tkinter.Tk()
    test = app(root)
    test.mainloop()
