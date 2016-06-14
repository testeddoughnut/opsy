import asyncio
from flask import json
from hourglass.utils import get_filters_list
from . import db, ExtraOut, CacheBase


class Zone(CacheBase, db.Model):

    __bind_key__ = 'cache'
    __tablename__ = 'zones'

    name = db.Column(db.String(64), primary_key=True)
    backend_type = db.Column(db.String(64))
    host = db.Column(db.String(64))
    port = db.Column(db.Integer())
    timeout = db.Column(db.Integer())

    meta_data = db.relationship('ZoneMetadata', backref='zone', lazy='dynamic',
                                query_class=ExtraOut)
    clients = db.relationship('Client', backref='zone', lazy='dynamic',
                              query_class=ExtraOut)
    checks = db.relationship('Check', backref='zone', lazy='dynamic',
                             query_class=ExtraOut)
    events = db.relationship('Event', backref='zone', lazy='dynamic',
                             query_class=ExtraOut)
    results = db.relationship('Result', backref='zone', lazy='dynamic',
                              query_class=ExtraOut)
    stashes = db.relationship('Stash', backref='zone', lazy='dynamic',
                              query_class=ExtraOut)

    def __init__(self, name, host, port, timeout):
        self.models = [Check, Client, Event, Stash, Result]
        self.backend_type = None
        self.name = name
        self.host = host
        self.port = port
        self.timeout = timeout

    def query_api(self, uri):
        raise NotImplementedError

    @asyncio.coroutine
    def update_objects(self, model):
        raise NotImplementedError

    def get_update_tasks(self, app, loop):
        tasks = []
        for model in self.models:
            tasks.append(asyncio.async(self.update_objects(app, loop, model)))
        return tasks

    @classmethod
    def get_dashboard_filters_list(cls, config, dashboard):
        if config['dashboards'].get(dashboard) is None:
            return ()
        zones = config['dashboards'][dashboard].get('zone')
        filters = ((zones, cls.name),)
        return get_filters_list(filters)

    def __repr__(self):
        return '<Zone %s>' % self.name


class ZoneMetadata(CacheBase, db.Model):

    __bind_key__ = 'cache'
    __tablename__ = 'zone_metadata'

    zone_name = db.Column(db.String(64), primary_key=True)
    key = db.Column(db.String(64))
    value = db.Column(db.String(64))

    __table_args__ = (
        db.ForeignKeyConstraint(['zone_name'], ['zones.name']),
    )

    def __init__(self, zone_name, key, value):
        self.zone_name = zone_name
        self.key = key
        self.value = value

    def __repr__(self):
        return '<ZoneMetadata %s: %s - %s>' % (self.zone_name, self.key,
                                               self.value)


class Client(CacheBase, db.Model):

    __bind_key__ = 'cache'
    __tablename__ = 'clients'

    zone_name = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(256), primary_key=True)

    events = db.relationship('Event', backref='client', lazy='dynamic',
                             query_class=ExtraOut,
                             primaryjoin="and_(Client.zone_name==foreign(Event.zone_name), "
                             "Client.name==foreign(Event.client_name))")
    results = db.relationship('Result', backref='client', lazy='dynamic',
                              query_class=ExtraOut,
                              primaryjoin="and_(Client.zone_name==foreign(Result.zone_name), "
                              "Client.name==foreign(Result.client_name))")
    stash = db.relationship('Stash', backref='clients', lazy='dynamic',
                            query_class=ExtraOut,
                            primaryjoin="and_(Client.zone_name==foreign(Stash.zone_name), "
                            "Client.name==foreign(Stash.client_name))")

    __table_args__ = (
        db.ForeignKeyConstraint(['zone_name'], ['zones.name']),
    )

    def __init__(self, zone_name, extra):
        self.zone_name = zone_name
        self.name = extra['name']
        extra['zone_name'] = zone_name
        self.extra = json.dumps(extra)

    @classmethod
    def get_dashboard_filters_list(cls, config, dashboard):
        if config['dashboards'].get(dashboard) is None:
            return ()
        zones = config['dashboards'][dashboard].get('zone')
        clients = config['dashboards'][dashboard].get('client')
        filters = ((zones, cls.zone_name),
                   (clients, cls.name))
        return get_filters_list(filters)

    def __repr__(self):
        return '<Client %s/%s>' % (self.zone_name, self.name)


class Check(CacheBase, db.Model):

    __bind_key__ = 'cache'
    __tablename__ = 'checks'

    zone_name = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(256), primary_key=True)

    results = db.relationship('Result', backref='check', lazy='dynamic',
                              query_class=ExtraOut,
                              primaryjoin="and_(Check.zone_name==foreign(Result.zone_name), "
                              "Check.name==foreign(Result.check_name))")
    events = db.relationship('Event', backref='check', lazy='dynamic',
                             query_class=ExtraOut,
                             primaryjoin="and_(Check.zone_name==foreign(Event.zone_name), "
                             "Check.name==foreign(Event.check_name))")

    __table_args__ = (
        db.ForeignKeyConstraint(['zone_name'], ['zones.name']),
    )

    def __init__(self, zone_name, extra):
        self.zone_name = zone_name
        self.name = extra['name']
        extra['zone_name'] = zone_name
        self.extra = json.dumps(extra)

    @classmethod
    def get_dashboard_filters_list(cls, config, dashboard):
        if config['dashboards'].get(dashboard) is None:
            return ()
        zones = config['dashboards'][dashboard].get('zone')
        checks = config['dashboards'][dashboard].get('check')
        filters = ((zones, cls.zone_name),
                   (checks, cls.name))
        return get_filters_list(filters)

    def __repr__(self):
        return '<Check %s/%s>' % (self.zone_name, self.name)


class Result(CacheBase, db.Model):

    __bind_key__ = 'cache'
    __tablename__ = 'results'

    zone_name = db.Column(db.String(64), primary_key=True)
    client_name = db.Column(db.String(256), primary_key=True)
    check_name = db.Column(db.String(256), primary_key=True)
    status = db.Column(db.Integer)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['zone_name'], ['zones.name']
        ),
    )

    def __init__(self, zone_name, extra):
        self.zone_name = zone_name
        self.extra = extra
        self.client_name = extra['client']
        self.check_name = extra['check']['name']
        self.status = extra['check']['status']
        extra['zone_name'] = zone_name
        self.extra = json.dumps(extra)

    @classmethod
    def get_dashboard_filters_list(cls, config, dashboard):
        if config['dashboards'].get(dashboard) is None:
            return ()
        zones = config['dashboards'][dashboard].get('zone')
        checks = config['dashboards'][dashboard].get('check')
        clients = config['dashboards'][dashboard].get('client')
        statuses = config['dashboards'][dashboard].get('status')
        filters = ((zones, cls.zone_name),
                   (checks, cls.check_name),
                   (clients, cls.client_name),
                   (statuses, cls.status))
        return get_filters_list(filters)

    def __repr__(self):
        return '<Result %s/%s/%s>' % (self.zone_name, self.client_name,
                                      self.check_name)


class Event(CacheBase, db.Model):

    __bind_key__ = 'cache'
    __tablename__ = 'events'

    zone_name = db.Column(db.String(64), primary_key=True)
    client_name = db.Column(db.String(256), primary_key=True)
    check_name = db.Column(db.String(256), primary_key=True)
    check_occurrences = db.Column(db.BigInteger)
    event_occurrences = db.Column(db.BigInteger)
    status = db.Column(db.Integer)

    stash = db.relationship('Stash', backref='events', lazy='dynamic',
                            query_class=ExtraOut,
                            primaryjoin="and_(Event.zone_name==foreign(Stash.zone_name),"
                            "Event.client_name==foreign(Stash.client_name), "
                            "Event.check_name==foreign(Stash.check_name))")

    __table_args__ = (
        db.ForeignKeyConstraint(['zone_name'], ['zones.name']),
    )

    def __init__(self, zone_name, extra):
        self.zone_name = zone_name
        self.client_name = extra['client']['name']
        self.check_name = extra['check']['name']
        self.check_occurrences = extra['check'].get('occurrences')
        self.event_occurrences = extra['occurrences']
        self.status = extra['check']['status']
        extra['zone_name'] = zone_name
        self.extra = json.dumps(extra)

    @classmethod
    def get_dashboard_filters_list(cls, config, dashboard):
        if config['dashboards'].get(dashboard) is None:
            return ()
        zones = config['dashboards'][dashboard].get('zone')
        checks = config['dashboards'][dashboard].get('check')
        clients = config['dashboards'][dashboard].get('client')
        statuses = config['dashboards'][dashboard].get('status')
        filters = ((zones, cls.zone_name),
                   (checks, cls.check_name),
                   (clients, cls.client_name),
                   (statuses, cls.status))
        return get_filters_list(filters)

    def __repr__(self):
        return '<Event %s/%s/%s>' % (self.zone_name, self.client_name,
                                     self.check_name)


class Stash(CacheBase, db.Model):

    __bind_key__ = 'cache'
    __tablename__ = 'stashes'

    zone_name = db.Column(db.String(64), primary_key=True)
    client_name = db.Column(db.String(256), primary_key=True)
    check_name = db.Column(db.String(256), nullable=True, primary_key=True, default="")
    #path = db.Column(db.String(256), primary_key=True)
    flavor = db.Column(db.String(64))

    __table_args__ = (
        db.ForeignKeyConstraint(['zone_name'], ['zones.name']),
    )

    def __init__(self, zone_name, extra):
        self.zone_name = zone_name
        self.path = extra['path']
        try:
            path_list = self.path.split('/')
            self.flavor = path_list[0]
            self.client_name = path_list[1]
            try:
                self.check_name = path_list[2]
            except IndexError:
                self.check_name = None
            self.source = extra['content']['source']
        except:
            self.flavor = None
            self.client_name = None
            self.check_name = None
            self.source = None
            self.created_at = None
            self.expire_at = None
        extra['zone_name'] = self.zone_name
        extra['check_name'] = self.check_name
        extra['client_name'] = self.client_name
        extra['flavor'] = self.flavor
        self.extra = json.dumps(extra)

    def __repr__(self):
        return '<Stash %s/%s>' % (self.zone_name, self.path)
