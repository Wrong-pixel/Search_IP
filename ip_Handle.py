import re
import ipaddress
import json


class ip_handle:
    def __init__(self, json_file, result_IP_Data={}):
        # 这里可以放在json_Load_IP方法中定义
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

    # 输入IP合法性娇艳
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
                for key in self.result_IP_Data:
                    for item in self.result_IP_Data[key]:
                        if ipaddress.ip_address(ipaddr) in item:
                            return True, key
                return False, None
            except BaseException:
                return False, None
        else:
            return False, None