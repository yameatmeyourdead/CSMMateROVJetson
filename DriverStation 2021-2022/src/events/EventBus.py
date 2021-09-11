import inspect

subscribers = {}
event_metadata = {}

class SubscriptionException(Exception):...

def SubscribeEvent():
    """Subscribes wrapped function to event given by the function name"""
    def subscribe(fn):
        if(fn.__name__ not in subscribers):
            subscribers[fn.__name__] = []
            event_metadata[fn.__name__] = [(), (), {}]
        elif(fn in subscribers[fn.__name__]):
            raise SubscriptionException("Cannot subscribe function twice")
        meta = inspect.getfullargspec
        event_metadata[fn.__name__]
        subscribers[fn.__name__].append(fn)
        return fn
    return subscribe


def postEvent(event):
    for subscriber in subscribers[event]:
        subscriber()