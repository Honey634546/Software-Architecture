from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import socket
import numpy as np
import boto3


class Gui:
    def __init__(self):
        self.busToui_URL = 'https://sqs.us-east-1.amazonaws.com/604291830461/busToui'
        self.uiTobus_URL = 'https://sqs.us-east-1.amazonaws.com/604291830461/uiTobus'
        self.f = Figure(figsize=(6, 4), dpi=100)
        self.client = boto3.client('sqs')

    def ui(self):
        root = Tk()
        root.title("浦发银行数据库查询系统")
        root.maxsize(600, 500)
        root.minsize(600, 500)
        btn_1 = Button(root, text="查差价", command=self.query_1)
        btn_1.place(x=80, y=25)
        btn_2 = Button(root, text="查转手率", command=self.query_2)
        btn_2.place(x=250, y=25)
        btn_3 = Button(root, text="查涨幅", command=self.query_3)
        btn_3.place(x=420, y=25)
        self.canvas = FigureCanvasTkAgg(self.f, master=root)
        self.canvas.get_tk_widget().place(x=15, y=85)
        self.canvas.draw()

        root.mainloop()

    def query_1(self):
        self.send_message('1')
        data = None
        while True:
            data = self.recv_message()
            if data:
                break
        data = data.split(',')
        l = []
        for i in range(len(data) - 2):
            l.append(float(data[i]))
        y = np.array(l)
        a = self.f.add_subplot(111)
        x = np.arange(1999, 2016, 1)
        a.bar(x, y)
        a.set_ylim(-0.06, 0.06, 0.05)
        a.set_xlim(1999, 2016, 1)
        self.canvas.draw()
        # self.s.close()

    def query_2(self):
        self.send_message('2')
        data = None
        while True:
            data = self.recv_message()
            if data:
                break
        data = data.split(',')
        l = []
        for i in range(len(data) - 2):
            l.append(float(data[i]))
        y = np.array(l)
        a = self.f.add_subplot(111)
        x = np.arange(1999, 2016, 1)
        print(y)
        a = self.f.add_subplot(111)
        a.bar(x, y)
        a.set_ylim(-0.06, 0.06, 0.05)
        a.set_xlim(1998, 2016, 1)
        self.canvas.draw()
        # self.s.close()

    def query_3(self):
        self.send_message('3')
        data = None
        while True:
            data = self.recv_message()
            if data:
                break
        data = data.split(',')
        l = []
        for i in range(len(data) - 2):
            l.append(float(data[i]))
        y = np.array(l)
        a = self.f.add_subplot(111)
        x = np.arange(1999, 2016, 1)
        print(y)
        a = self.f.add_subplot(111)
        a.plot(x, y)
        a.set_ylim(-0.06, 0.06, 0.05)
        a.set_xlim(1998, 2016, 1)
        self.canvas.draw()
        # self.s.close()

    def send_message(self, message):
        """
        :param message:
        :return:
        """
        print('send ',message)
        self.client.send_message(
            QueueUrl=self.uiTobus_URL, MessageBody=message)

    def recv_message(self):
        """
        :return: 有消息则返回消息 无消息返回None
        """
        try:
            resp = self.client.receive_message(QueueUrl=self.busToui_URL)
            self.client.delete_message(
                QueueUrl=self.busToui_URL,
                ReceiptHandle=resp['Messages'][0]['ReceiptHandle'])
            print(resp['Messages'][0]['Body'])
            return resp['Messages'][0]['Body']
        except BaseException:
            return None


if __name__ == '__main__':
    gui = Gui()
    gui.ui()
