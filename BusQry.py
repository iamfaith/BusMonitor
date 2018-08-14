# -*- coding: UTF-8 -*-
import json
import re
import time

import requests


class BusBase:
    __UA = ('mozilla/5.0 (linux; u; android 4.1.2; zh-cn; mi-one plus build/jzo54k)'
            ' applewebkit/534.30 (khtml, like gecko) version/4.0 mobile safari/534.'
            '30 micromessenger/5.0.1.352')
    __BusQuery = 'http://www.zhbuswx.com/Handlers/BusQuery.ashx'
    __header = {
        'user-agent': __UA,
        "Cookie": "openid3=oiFDwsnIOua4D0p6nN1ab1J1FOoU"
    }

    __Route = 'http://restapi.amap.com/v3/direction/transit/integrated?origin={}&destination={}' \
              '&city=珠海&strategy=0&nightflag=0&extensions&s=rsv3&cityd=珠海&key' \
              '=ceb54024fae4694f734b1006e8dc8324&callback=jsonp_486288_&platform=JS&logversion=2.0&sdkversion=1.3' \
              '&appname=http%3A%2F%2Fwww.zhbuswx.com%2Fbusline%2FBusQuery.html%3Fv%3D2.01%23%2F&csid=53640C7D-3FEB' \
              '-41BA-8E73-D225FCD5E92F'

    __SearchStation = 'http://restapi.amap.com/v3/place/text?s=rsv3&key=ceb54024fae4694f734b1006e8dc8324&extensions' \
                      '=all&page=1&offset=10&city=%E7%8F%A0%E6%B5%B7&language=zh_cn&callback=jsonp_622988_&platform' \
                      '=JS&logversion=2.0&sdkversion=1.3&appname=http%3A%2F%2Fwww.zhbuswx.com%2Fbusline%2FBusQuery' \
                      '.html%3Fv%3D2.01%23%2F&csid=FAB7C96B-8BCB-4AF0-BC0A-0B02766E455F&keywords={}'

    __ListBusStation = 'http://www.zhbuswx.com/Handlers/BusQuery.ashx?handlerName=GetStationList&lineId={}' \
                       '&_=1534145964159 '
    __BusDirection = 'http://www.zhbuswx.com/Handlers/BusQuery.ashx?handlerName=GetLineListByLineName&key={}&_' \
                     '=1534146141487 '

    @staticmethod
    def handle_jsonp(jsonp):
        m = re.search('\((.*)\)', jsonp)
        if m:
            found = m.group(1)
            found = json.loads(found)
            return found

    @staticmethod
    def search_station(text):
        if text is None:
            return
        c = requests.get(BusBase.__SearchStation.format(text), headers=BusBase.__header).content.decode('utf-8')
        pos = BusBase.handle_jsonp(c)
        if pos:
            pos = pos['pois']
            # for p in pos:
            #     print("{} -- {}".format(p["name"], p["location"]))
            return pos

    @staticmethod
    def get_route(origin, destination):
        url = BusBase.__Route.format(origin, destination)
        # print(url)
        c = requests.get(url, headers=BusBase.__header).content.decode('utf-8')
        r = BusBase.handle_jsonp(c)
        if r:
            r = r['route']
            transits = r['transits']
            bus_route = []
            for t in transits:
                seg = []
                for s in t["segments"]:
                    buslines = s["bus"]["buslines"]
                    if 0 < len(buslines) <= 10:
                        for bus_line in buslines:
                            bus_info = {'arrival_stop': bus_line['arrival_stop'],
                                        'departure_stop': bus_line['departure_stop'], 'name': bus_line['name']}
                            seg.append(bus_info)
                if len(seg) > 0:
                    bus_route.append({"seg": seg})
            return bus_route

    @staticmethod
    def get_bus(line_name, from_station):
        params = {
            'lineName': line_name,
            'fromStation': from_station,
            'handlerName': 'GetBusListOnRoad',
            '_': int(time.time() * 1000)
        }
        c = requests.get(BusBase.__BusQuery, params=params, headers=BusBase.__header).content.decode('utf-8')
        print(c)
        return json.loads(c)['data']

    @staticmethod
    def get_station(line_name, from_station):
        c = requests.get(BusBase.__BusDirection.format(line_name), headers=BusBase.__header).content.decode('utf-8')
        directions = json.loads(c)['data']
        bus_info = {}
        for d in directions:
            if d['FromStation'] == from_station:
                bus_info = d
                break
        # print(bus_info)
        c = requests.get(BusBase.__ListBusStation.format(bus_info['Id']), headers=BusBase.__header).content.decode(
            'utf-8')
        stations = json.loads(c)['data']
        # print(stations)
        return stations

    @staticmethod
    def pre_station(stations, cur, pre=2):
        index = -1
        for i, item in enumerate(stations):
            if cur in item['Name']:
                index = i
                break
        if index is not -1:
            stations = stations[index - pre: index]
        else:
            stations = []
        return stations


if __name__ == '__main__':
    msg = set()
    msg.add('asdzxc')
    msg.add('asdzxc')
    msg.add('123')
    print(msg)
    print(msg.__contains__('123'))
    # s = BusBase.get_station('20', '上冲总站')
    # s = BusBase.pre_station(s, "柠溪")
    # print(s)
    # s = BusBase.get_station('11', '夏湾')
    # s = BusBase.pre_station(s, "柠溪", 4)
    # print(s)


# origin = BusBase.search_station('柠溪(公交')[0]["location"]
# print("---")
# dest = BusBase.search_station('二中1111111')[0]["location"]
# route = BusBase.get_route(origin, dest)
# print(route)
