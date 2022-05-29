import tkinter as tk
from tkinter import ttk
from ip_Handle import ip_handle


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
    root.tk.call("source", "sun-valley.tcl")
    root.tk.call("set_theme", "light")

    # 设置窗体
    root.geometry('285x75+{}+{}'.format(
        (root.winfo_screenwidth() - 285) // 2,
        (root.winfo_screenheight() - 75) // 2)
    )
    root.resizable(False, False)

    app = App(root, ip_module)

    root.update()
    root.mainloop()
