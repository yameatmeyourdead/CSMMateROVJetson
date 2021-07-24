from typing import Dict, List, Callable
# from tools import Logger
from traceback import format_exc

# event dict
subscribers:Dict[str, List[Callable]] = dict()

def SubscribeEvent(event_type:str):
    """Decorator that subscribes function to event event_type"""
    def subscribe(fn:Callable):
        if not event_type in subscribers:
            subscribers[event_type] = []
        subscribers[event_type].append(fn)
        print(fn, "successfully subscribed to event " + event_type)
        return fn
    return subscribe

# TODO: ensure parameters match functions that have subscribed to an event before notifying them
def post_event(event_type: str, *args, **kwargs):
    """Post event and notify subscribers"""
    if not event_type in subscribers:
        return
    for fn in subscribers[event_type]:
        try:
            fn(*args, **kwargs)
        except TypeError:
            # Logger.logError(format_exc())
            print(format_exc())

# test events
# @SubscribeEvent(event_type="Yeet")
# def thisBitchEmpty(*args, **kwargs):
#     print("YEET!")

# @SubscribeEvent(event_type="Yeet")
# def howEmptyThisBitch(emptiness="", *args, **kwargs):
#     print("how", emptiness)

# post_event("Yeet")
# post_event("Yeet", 1)