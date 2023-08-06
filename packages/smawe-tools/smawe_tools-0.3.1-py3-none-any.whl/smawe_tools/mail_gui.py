"""
PyInstaller简单打包
    url: https://zhuanlan.zhihu.com/p/367063488

说什么？看起来我们没有对这些小部件做任何事情！这是我们在创建小部件时指定的神奇 textvariable 选项发挥作用的地方。
我们将全局变量 feet 指定为条目的文本变量。每当条目发生变化时，Tk 会自动更新全局变量 feet 。类似地，
如果我们显式更改与小部件关联的文本变量的值（就像我们对附加到标签的 meters 所做的那样），小部件将自动更新为变量的当前内容。
对于 Python，唯一需要注意的是这些变量必须是 StringVar 类的实例。
"""

import os
import re
import smtplib
import socket
from email.message import EmailMessage
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, showwarning
import environs


class EmailGUI:
    def __init__(self, title="邮件发送软件(作者QQ:1281722462).exe"):
        self._tk = Tk()
        self._tk.title(title)
        ttk.Style().configure('custom.TFrame', background='white', borderwidth=10, relief='solid')
        self._mainframe = ttk.Frame(self._tk, padding="10 10 20 20", style="custom.TFrame")
        self._mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self._tk.columnconfigure(0, weight=1, minsize=50)
        self._tk.rowconfigure(0, weight=1, minsize=50)
        self._mainframe.columnconfigure(0, weight=1)
        self._mainframe.columnconfigure(1, weight=3)
        self._mainframe.rowconfigure(0, weight=1)
        self._mainframe.rowconfigure(1, weight=1)
        self._mainframe.rowconfigure(2, weight=1)
        self._mainframe.rowconfigure(3, weight=1)
        self._mainframe.rowconfigure(4, weight=1)
        self._mainframe.rowconfigure(5, weight=1)
        self._mainframe.rowconfigure(6, weight=1)

        # error tip message
        self._errmsg = StringVar()
        self._format_msg = "user should be #########@qq.com"
        ttk.Label(self._mainframe, font='TkSmallCaptionFont', foreground='red', textvariable=self._errmsg).grid(
            column=1, row=8, sticky="we")
        self._validate_wrapper = (self._tk.register(self._validate), "%P")

        self._user = StringVar()
        self._user_entry = ttk.Entry(self._mainframe, width=20, textvariable=self._user, validate="key",
                                     validatecommand=self._validate_wrapper)
        self._user_entry.grid(column=1, row=1, sticky=W)
        self._password = StringVar()
        self._password_entry = ttk.Entry(self._mainframe, width=20, textvariable=self._password, show="*")
        self._password_entry.grid(column=1, row=2, sticky=W)
        self._content_text = Text(self._mainframe, width=40, height=10, wrap="char")
        self._content_text.grid(column=1, row=4, sticky=(N, W, S, E))
        self._to_addrs = StringVar()
        self._to_addrs_entry = ttk.Entry(self._mainframe, width=50, textvariable=self._to_addrs)
        self._to_addrs_entry.grid(column=1, row=5, sticky=W)
        self._mail_subject = StringVar()
        self._mail_subject_entry = ttk.Entry(self._mainframe, width=20, textvariable=self._mail_subject)
        self._mail_subject_entry.grid(column=1, row=3, sticky=W)

        ttk.Label(self._mainframe, text="账号: ").grid(column=0, row=1, sticky=E)
        ttk.Label(self._mainframe, text="密码: ").grid(column=0, row=2, sticky=E)
        ttk.Label(self._mainframe, text="邮件内容: ").grid(column=0, row=4, sticky=E)
        ttk.Label(self._mainframe, text="收件人列表: ").grid(column=0, row=5, sticky=E)
        self._send_button = ttk.Button(self._mainframe, text="发送", command=self._send)
        self._send_button.grid(column=2, row=4, sticky=E)
        ttk.Label(self._mainframe, text="邮件主题: ").grid(column=0, row=3, sticky=E)

        for child in self._mainframe.winfo_children():
            child.grid_configure(padx=3, pady=5)

        self._content_text.focus()

        # do some private handle
        try:
            _env = environs.Env()
            _env.read_env(path=os.getcwd() + os.sep + ".env")
            _mode = _env.str("MODE", "PROD")
            if _mode == "DEV":
                self._user.set(_env.str("USER", ""))
                self._password.set(_env.str("PASSWORD", ""))
        except AttributeError:
            pass

    def _send(self, *args, **kwargs):
        self._flags = False
        user = self._user_entry.get().strip()
        password = self._password_entry.get().strip()
        to_addrs = self._to_addrs.get().strip().split(",")
        if len(to_addrs) != 1:
            to_addrs = [v.strip() for v in to_addrs]
        else:
            to_addrs = [to_addrs[0].strip()] if to_addrs[0].strip() else []
        content = self._content_text.get("1.0", "end").strip()
        subject = self._mail_subject_entry.get().strip()
        if not (user and password and to_addrs and content and subject):
            showwarning(title="warning", message="账号或密码或主题或邮件内容或收件人列表不能为空!")
            return
        try:
            smtp = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=120)
        except socket.timeout:
            showerror(title="error", message="连接超时, 请重试...")
            raise
        except socket.gaierror:
            showerror(title="error", message="请检查网络是否已连接...")
            raise
        try:
            smtp.login(user, password)
        except smtplib.SMTPAuthenticationError:
            print("账号或密码错误...")
            showerror(title="error", message="账号或密码错误...")
            raise
        except smtplib.SMTPServerDisconnected:
            print("未能连接上QQ邮箱服务器, 请检查账号或QQ邮箱授权码是否正确!")
            showerror(title="error", message="未能连接上QQ邮箱服务器, 请检查账号或密码是否正确!")
            raise
        else:
            print("已成功连接上QQ邮箱服务器...")
        mail = EmailMessage()
        mail["From"] = user
        mail["To"] = to_addrs
        mail["subject"] = subject
        mail.set_content(content)
        try:
            smtp.send_message(mail)
            showinfo(title="states", message="发送成功")
        except (smtplib.SMTPRecipientsRefused, smtplib.SMTPNotSupportedError):
            showerror(title="error", message="请检查收件人列表是否正确填写!")
            raise
        finally:
            smtp.quit()

    def _validate(self, val):
        """refuse change if return is False,else allow change"""
        self._errmsg.set("")
        valid = re.match("^[0-9a-z@\\.]*$", val) is not None
        if not valid:
            self._errmsg.set(self._format_msg)
        return valid

    def start(self):
        self._tk.mainloop()


if __name__ == '__main__':
    # 后续考虑添加附件发送功能(待完善)...
    EmailGUI().start()
