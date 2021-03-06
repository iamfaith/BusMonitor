# -*- coding: UTF-8 -*-
import threading
import time

from BusQry import BusBase
from auto_login import MessageSender


class BusMonitor(BusBase):
    def __init__(self, station, line_name, from_station, before_num=2):
        self.station = station
        self.content = ""
        self.line_name = '{}路'.format(line_name)
        self.from_station = from_station
        self.title = "Dear:{}-{}来了".format(self.from_station, self.line_name)
        self.before_num = before_num
        stations = self.get_station(self.line_name, self.from_station)
        self.pre = self.pre_station(stations, self.station, self.before_num)

    def monitor_bus(self):
        bus = self.get_bus(self.line_name, self.from_station)
        for b in bus:
            for i, p in enumerate(self.pre):
                if b['CurrentStation'] in p['Name']:
                    left = len(self.pre) - i
                    self.content = "{}到了{}，还有{}站到达{}[{}]".format(b['BusNumber'], b['CurrentStation'], left,
                                                                 self.station, self.line_name)
                    return True

        print(bus)
        gen = (b for b in bus if self.station in b['CurrentStation'])
        for b in gen:
            self.content = "{}到达{}[{}]".format(b['BusNumber'], b['CurrentStation'], self.line_name)
            return True
        return False


def monitor_bus(station, line_name, from_station, interval=1200, receiver="u-27130018-e12c-480c-8f10-6671f591"):
    monitor = BusMonitor(station, line_name, from_station)
    start = time.time()
    msg = set()
    while True:
        try:
            done = time.time()
            elapsed = done - start
            if elapsed > interval:
                break
            if monitor.monitor_bus():
                sender = MessageSender()
                content = monitor.content
                if msg.__contains__(content):
                    time.sleep(3)
                    continue
                title = monitor.title
                sender.send_message(content, title, receiver=receiver)
                msg.add(content)
            time.sleep(4)
        except:
            time.sleep(3)


def start_monitor_bus(*args, **kwargs):
    t = threading.Thread(target=monitor_bus, args=args, kwargs=kwargs)
    t.start()


if __name__ == '__main__':
    start_monitor_bus('湖湾里', '11', u'夏湾', 5, receiver='u-99076430-a107-496a-937f-1d2f24d6')
    # start_monitor_bus('二中', '12', u'九洲港', 5, receiver='u-99076430-a107-496a-937f-1d2f24d6')

# resp = requests.get(
#     "https://apis.map.qq.com/tools/geolocation?key=OB4BZ-D4W3U-B7VVO-4PJWW-6TKDJ-WPB77&referer=myapp")
# content = resp.content
# parsed_html = content.decode('utf-8')
#
# m = re.search('window._DEFAULT_CITY = (.*)[;]', parsed_html)
# print(m)
# if m:
#     found = m.group(1)
#     data = json.loads(found)
#     url = "http://apis.map.qq.com/ws/geocoder/v1"
#     params = {"location": "{},{}".format(data["lat"], data["lng"]),
#               "coord_type": 5,
#               "key": "TKUBZ-D24AF-GJ4JY-JDVM2-IBYKK-KEBCU"}
#     content = requests.get(url, params=params).content
#     bus_station = json.loads(content.decode('utf-8'))
#     print(bus_station)
