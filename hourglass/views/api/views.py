from time import time
from . import api
from hourglass.models.api import Event, Check
from flask import jsonify


@api.route('/ping')
def ping():
    return jsonify({'pong': time()})


@api.route('/events')
@api.route('/events/<datacenter>')
def events(datacenter=None):
    filter_list = []
    if datacenter:
        filter_list.append(Event.datacenter.in_([datacenter]))
    sensuevents = Event.query.filter(*filter_list).all_extra_as_dict()
    return jsonify({'events': sensuevents, 'timestamp': time()})


@api.route('/checks')
@api.route('/checks/<datacenter>')
def checks(datacenter=None):
    filter_list = []
    if datacenter:
        filter_list.append(Check.datacenter.in_([datacenter]))
    sensuchecks = Check.query.filter(*filter_list).all_extra_as_dict()
    return jsonify({'checks': sensuchecks, 'timestamp': time()})
