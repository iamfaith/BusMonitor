import json

import schedule
from flask import Flask
from flask import request
from multiprocessing import Process

import util
import conf
from BusQry import BusBase
from bus_monitor import start_monitor_bus

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

def bus_12():
    start_monitor_bus('二中', '12', u'九洲港', 5)  # , receiver='u-99076430-a107-496a-937f-1d2f24d6')


def bus_11():
    start_monitor_bus('湖湾里', '11', u'夏湾', 5)  # , receiver='u-99076430-a107-496a-937f-1d2f24d6')


def start_schedule():
    schedule.every().day.at("14:37").do(bus_12)
    schedule.every().day.at("14:37").do(bus_11)
    while True:
        schedule.run_pending()

start_schedule()
# app.run(host="0.0.0.0", port=conf.port, debug=conf.debug)
