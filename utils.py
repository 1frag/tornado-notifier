import os
import json
import attr


class Collector:
    storage = dict()

    def __init__(self, callback, *include, **kwargs):
        self.__call__(*include, **kwargs)
        for key, value in self.storage.items():
            if callback:
                callback(key, value)

    @classmethod
    def _define(cls, key, value):
        cls.storage[key] = value

    def __call__(self, *include, **kwargs):
        check = lambda name: name in include

        check('def_base') and self.def_base()
        check('def_secrets') and self.def_secrets()
        check('def_kwargs') and self.def_kwargs(**kwargs)

    def def_base(self):
        self.storage['environment'] = os.getenv('environment', 'development')
        self.storage['site_title'] = 'Simple Notifier'
        self.storage['port'] = '8000'

    def def_secrets(self):
        if self.storage['environment'] == 'development':
            getter = json.load(open('secrets.json')).get
        else:
            getter = os.getenv
        definer = lambda key: self._define(key, getter(key))

        definer('tg_token')
        definer('cookie_secret')
        definer('dburl')
        definer('EMAIL')
        definer('PASSWORD')

    def def_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            self._define(key, value)


@attr.s
class Item:
    collector = attr.ib(type=Collector)
    field_name = attr.ib(type=str)

    def get(self):
        return self.collector.storage[self.field_name]

    def set(self, value):
        self.collector.storage[self.field_name] = value
