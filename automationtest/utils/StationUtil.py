import requests
import os
import json


class Station:

    def __init__(self):
        self.dirPath = "/Users/xinjianhou/PycharmProjects/automationtest/data/"

    def send_request(self):
        try:
            response = requests.get(
                url="https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9053",
            )
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))

            strr = str(response.content, encoding="utf8")
            f = open(self.dirPath + "ceshi.txt", 'w+')
            f.truncate()
            f.write(strr)

            for line2 in open(self.dirPath + "ceshi.txt"):
                clean_data = line2.split('|')  # 先根据'|'分隔数据
            dictx = {}
            resultx = clean_data[1:len(clean_data):5]  # 观察数据后,切片,从i=1开始,每次间隔5个,做字典key
            resulty = clean_data[2:len(clean_data):5]  # 观察数据后,切片,从i=2开始,每次间隔5个,做字典value
            for i in range(len(resultx)):
                dictx[resultx[i]] = resulty[i]
            f = open(self.dirPath + "result.txt", 'w+')  # 最终数据写入文件
            f.truncate()
            f.write(str(json.dumps(dictx)))

        except requests.exceptions.RequestException:
            print('HTTP Request failed')

    def get_station(self, name):

        file = open(self.dirPath + "result.txt", 'r')
        dict = json.loads(file.read())
        file.close()

        print('移除前test目录下有文件：%s' % os.listdir(self.dirPath))
        # 判断文件是否存在
        if (os.path.exists(self.dirPath + "ceshi.txt")):
            os.remove(self.dirPath + "ceshi.txt")
            print('移除后test 目录下有文件：%s' % os.listdir(self.dirPath))
        else:
            print("要删除的文件不存在！")
        return dict.get(name)
