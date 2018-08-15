# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import yaml
from openpyxl.compat.singleton import Singleton
from threading import Lock
import alert_over as conf

lock = Lock()


class MessageSender(metaclass=Singleton):
    __login_url = 'https://www.alertover.com/auth/login'
    __send_url = "https://www.alertover.com/console/send"

    def __init__(self):
        # with open("conf.yaml", "r") as f:
        #     conf = yaml.load(f)

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/67.0.3396.99 Safari/537.36 ",
            "Referer": "https://www.alertover.com/auth/login",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.session = requests.Session()
        self.msg_queue = set()
        response = self.session.post(MessageSender.__login_url, data=conf.data, headers=headers, verify=False)

    def send_message(self, msg, title, url=None, receiver="u-27130018-e12c-480c-8f10-6671f591"):
        with lock:
            if self.msg_queue.__contains__(msg):
                return
            data = {
                "content": msg,
                "priority": 0,
                "receiver": receiver,
                "sound": "default",
                "source": "Alertover",
                "title": title,
                "url": url
            }
            response = self.session.post(MessageSender.__send_url, data=data)
            self.msg_queue.add(msg)
            content = response.content
            parsed_html = BeautifulSoup(content.decode('utf-8'), "lxml")
            print(parsed_html)

    @staticmethod
    def dump_config():
        with open("conf.yaml", "w") as f:
            yaml.dump(MessageSender.__data, f)


def test_class():
    sender = MessageSender()
    content = "abc1111"
    title = "conf"
    send_url = "www.baidu.com"
    sender.send_message(content, title, send_url)


if __name__ == '__main__':
    # MessageSender.dump_config()
    test_class()

# def login():
#     url = 'https://www.alertover.com/auth/login'
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
#                       "Chrome/67.0.3396.99 Safari/537.36 ",
#         "Referer": "https://www.alertover.com/auth/login",
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     data = {
#     }
#     session = requests.Session()
#     response = session.post(url, data=data, headers=headers)
#
#     print("response headers:", response.headers)
#
#     content = "abc"
#     title = "test"
#     send_url = "www.baidu.com"
#
#     url = "https://www.alertover.com/console/send"
#     data = {
#         "content": content,
#         "priority": 0,
#         "receiver": "u-27130018-e12c-480c-8f10-6671f591",
#         "sound": "default",
#         "source": "Alertover",
#         "title": title,
#         "url": send_url
#     }
#
#     response = session.post(url, data=data)
#     content = response.content
#     parsed_html = BeautifulSoup(content.decode('utf-8'), "lxml")
#     print(parsed_html)
