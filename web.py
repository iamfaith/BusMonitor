# -*- coding: UTF-8 -*-
import json
from multiprocessing import Process

import schedule
from flask import Flask
from flask import request

import conf
from BusQry import BusBase
from bus_monitor import start_monitor_bus
from common import util
from redis_config import RedisConf

app = Flask(__name__)
logger = util.setup_logger()


# curl 127.0.0.1:8080/stations --data-urlencode "text=柠溪" -X GET -G
@app.route("/stations", methods=['GET'])
def get_stations():
    # logger.debug('123')
    text = request.args.get('text')
    pos = BusBase.search_station(text)
    if pos is not None:
        return json.dumps(pos)
    return ""


# curl 127.0.0.1:8080/routes --data-urlencode "from=柠溪(公交" --data-urlencode "to=二中" -X GET -G
@app.route("/routes", methods=['GET'])
def get_routes():
    try:

        origin = request.args.get('from')
        dest = request.args.get('to')
        if origin is not None and dest is not None:
            origin = BusBase.search_station(origin)[0]["location"]
            dest = BusBase.search_station(dest)[0]["location"]
            route = BusBase.get_route(origin, dest)
            return json.dumps(route)
    except:
        return ""


@app.route("/task/<receiver>", methods=['POST'])
def tasks(receiver):
    print(receiver)
    data = request.json
    r = RedisConf()
    if data.get('isOn') == 0:
        r.hash_set(receiver, 'isOn', 0)
    else:
        r.hash_set(receiver, 'isOn', 1)
    return "ok"


# @app.route("/bus_watcher", methods=['POST'])
# def bus_watcher():
#     data = request.json
#     route = data['route']
#     dep_station = data['dep_station']
#     at = data['at']
#
#     t = Process(target=notify_rt_oneshot, args=(route, dep_station, at))
#     t.deamon = True
#     t.start()
#
#     return "Enabled notify for bus %s from %s when it's at %s" % (route,
#                                                                   dep_station,
#                                                                   at)

def bus():
    # start_monitor_bus('柠溪', '12', u'九洲港')  # , receiver='u-99076430-a107-496a-937f-1d2f24d6')
    # start_monitor_bus('柠溪', '56', u'夏湾')  # , receiver='u-99076430-a107-496a-937f-1d2f24d6')
    # start_monitor_bus('柠溪', '14', u'长隆')  # , receiver='u-99076430-a107-496a-937f-1d2f24d6')
    # start_monitor_bus('柠溪', '20', u'上冲总站')  # , receiver='u-99076430-a107-496a-937f-1d2f24d6')

    start_monitor_bus('柠溪', '12', u'九洲港', receiver='u-99076430-a107-496a-937f-1d2f24d6')
    start_monitor_bus('柠溪', '56', u'夏湾', receiver='u-99076430-a107-496a-937f-1d2f24d6')
    start_monitor_bus('柠溪', '14', u'长隆', receiver='u-99076430-a107-496a-937f-1d2f24d6')
    start_monitor_bus('柠溪', '20', u'上冲总站', receiver='u-99076430-a107-496a-937f-1d2f24d6')


def start_schedule():
    schedule.every().day.at("07:40").do(bus)
    while True:
        schedule.run_pending()


# t = Process(target=start_schedule)
# t.deamon = True
# t.start()
start_schedule()
# bus()
# app.run(host="0.0.0.0", port=conf.port, debug=conf.debug)
