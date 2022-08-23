import tkinter as tk
from tkinter import ttk
import sv_ttk
import re
import ipaddress
import json


class ip_handle:
    def __init__(self, json_file, result_IP_Data=None):
        # 这里可以放在json_Load_IP方法中定义
        if result_IP_Data is None:
            result_IP_Data = {}
        self.result_IP_Data = result_IP_Data
        # 实例化时需要传入json文件名，实际上也可以放在json_Load_IP方法中去定义
        self.json_file = json_file
        # 强制调用json_Load_IP方法，将json文件中的数据处理为ipaddress.ip_network对象
        self.json_Load_IP()

    def json_Load_IP(self):
        # 读文件
        with open("./database.json", encoding='utf-8') as f:
            ip_data = json.loads(f.read())['children']
        # 将ip段转化为ipaddress.ip_network对象
        for item in ip_data:
            temp_data = []
            try:
                for ips in item["networks"]:
                    temp_data.append(ipaddress.ip_network(ips, False))
                self.result_IP_Data.update({item["name"]: temp_data})
            except ValueError:
                pass
        return self.result_IP_Data

    # 输入IP合法性校验
    def check_ip(self, ipAddr):
        compile_ip = re.compile(
            '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$'
        )
        if compile_ip.match(ipAddr):
            return True
        else:
            return False

    # 查找IP，不要问为啥不用二分法、问就是不会
    def search_ip(self, ipaddr):
        if self.check_ip(ipaddr):
            try:
                for key, value in self.result_IP_Data.items():
                    for item in value:
                        if ipaddress.ip_address(ipaddr) in item:
                            return True, key
                return False, None
            except BaseException:
                return False, None
        else:
            return False, None


class App(ttk.Frame):

    def __init__(self, tk_module, ip_module):
        ttk.Frame.__init__(self)
        self.tk_module = tk_module
        self.ip_module = ip_module
        self.setup_widgets()
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

    def setup_widgets(self):
        self.result = tk.StringVar()
        self.tip_label = ttk.Label(
            self.tk_module,
            text="IP:",
            font=("-size", 15),
        )
        self.tip_label.grid(row=0, column=0, padx=5)

        self.ip_input_entry = ttk.Entry(
            self.tk_module,
            font=("-size", 15),
            width=18,
        )
        self.ip_input_entry.grid(row=0, column=1, padx=5)

        self.search_button = ttk.Button(
            self.tk_module,
            text="查询",
            style="Accent.TButton",
            command=self.search_ip_func,
        )
        self.search_button.grid(row=0, column=2)

        self.result_label = ttk.Label(
            self.tk_module,
            textvariable=self.result,
            font=("-size", 15),
        )
        self.result_label.grid(row=1, column=0, columnspan=3, pady=5)

        self.copyright_label = ttk.Label(
            self.tk_module,
            text="Powered by BigBigBan v1.0",
        )
        self.copyright_label.grid(row=2, column=0, columnspan=3, sticky="SE")

    def search_ip_func(self):
        ipaddr = self.ip_input_entry.get()
        if self.ip_module.check_ip(ipaddr):
            flag, result = self.ip_module.search_ip(ipaddr)
            if flag:
                self.result.set(result)
            else:
                self.result.set("没有找到")
        else:
            self.result.set("请检查IP格式")


if __name__ == '__main__':
    root = tk.Tk()
    root.title("IP归属查询工具_v1.0")
    # 处理IP数据
    ip_module = ip_handle("./database.json")

    # 设置主题
    sv_ttk.set_theme("light")

    # 设置窗体
    root.geometry('285x75+{}+{}'.format(
        (root.winfo_screenwidth() - 285) // 2,
        (root.winfo_screenheight() - 75) // 2)
    )
    root.resizable(False, False)

    app = App(root, ip_module)

    root.update()
    root.mainloop()
