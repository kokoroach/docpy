from datetime import datetime, date, time


def get_attribs(attribs):
    _attribs = {}
    for k in attribs.keys():
        item = attribs[k]
        if item is None:
            continue
        if not k.startswith('_'):
            _attribs[k] = item
            continue
        t = k[1:]
        if not t.startswith('_'):
            _attribs[t] = item
    return _attribs

def get_now():
    return datetime.now()

def date_from_str(date_str):
    return datetime.strptime(date_str, '%m-%d-%Y').date()

def time_from_str(time_str):
    return datetime.strptime(time_str, '%H:%M:%S').time()

def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def deserialize(dict):
    # NOTE: Only 1-level dict* (not nested)
    for k in dict:
        if 'date' in k:
            dict[k] = date_from_str(dict[k])
        elif 'time' in k:
            dict[k] = time_from_str(dict[k])
    return dict
