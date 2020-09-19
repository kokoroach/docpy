from datetime import datetime


def get_attribs(attribs):
    _attribs = {}
    for k in attribs.keys():
        if attribs[k] is None:
            continue
        t = k[1:]
        if not t.startswith('_'):
            _attribs[t] = attribs[k]
    return _attribs

def get_now():
    return datetime.now()
