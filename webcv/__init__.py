import json
import os
from collections import OrderedDict

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension


class Dict(OrderedDict):
    def nested_update(self, dct):
        for k, v in dct.items():
            if k not in self:
                self[k] = v
            else:
                if not isinstance(v, dict):
                    self[k] = v
                else:
                    if self[k] is None:
                        self[k] = v
                    else:
                        assert isinstance(self[k], dict)
                        new = self[k]
                        if not isinstance(new, Dict):
                            new = Dict(new)
                        new.nested_update(v)
                        self[k] = new


class JsonConfig(Dict):
    def __init__(self, *args, **kwargs):
        self.file = None
        super().__init__(*args, **kwargs)

    def save(self):
        with open(self.file, 'wt', encoding='utf8') as f:
            json.dump(self, f, ensure_ascii=False, indent=4)

    def load(self, file=None):
        if file is None:
            file = self.file
        with open(file, 'rt', encoding='utf8') as f:
            d = json.load(f, object_pairs_hook=Dict)
            self.nested_update(d)

    def apply(self):
        # call me when config has been changed
        app.config.update(self.get('flask', dict()))


app = Flask(__name__)

# config for flask app
base_flask_config = {
    # do not escape non-ascii strings
    'JSON_AS_ASCII': False,
    'UPLOAD_DIR': os.path.join(app.root_path, 'uploads'),
}
app.config.update(base_flask_config)


DEFALUT_CONFIG_FILE = 'config_default.json'
CONFIG_FILE = 'config.json'
# create config file if not exists
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'wt') as f:
        json.dump(dict(), f)


# config object for whole project
config = JsonConfig()
config.load(DEFALUT_CONFIG_FILE)
config.file = CONFIG_FILE
config.load()
config.apply()

DebugToolbarExtension(app)

from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)


# load all view functions
import webcv.views
