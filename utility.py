import json

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("static"))
base_key = "bEHMmq5X4aXo6GUhl8OnOpqHKePfkn4qo0M_AuVikoc"


def render(template, **kwargs):
    kwargs["key"] = base_key
    return env.get_template(template).render(kwargs)


def build_object_json(data, resulting_json):
    hide_private_attributes = True
    for key in dir(data):
        if key.startswith("__") and hide_private_attributes:
            continue
        value = getattr(data, key)
        if isinstance(value, dict):
            next_level = {}
            resulting_json[key] = next_level
            build_object_json(value, next_level)
        else:
            resulting_json[key] = str(value)


def get_object_json(data):
    resulting_json = {}
    build_object_json(data, resulting_json)
    return json.dumps(resulting_json, sort_keys=True, indent=4)
