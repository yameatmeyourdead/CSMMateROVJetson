from EventBase import Event
import inspect
subscribers = {}

class SubscriptionException(Exception): ...
class EventPostingException(Exception): ...

def SubscribeEvent(event:Event):
    """Subscribes wrapped function to event given by the function name"""
    def subscribe(fn):
        if(not inspect.isclass(event)):
            raise SubscriptionException("Function must subscribe to a subclass of Event")
        if(event not in subscribers):
            subscribers[event] = []
        elif(fn in subscribers[event]):
            raise SubscriptionException("Cannot subscribe function to event twice")
        subscribers[event].append(fn)
        return fn
    return subscribe

def postEvent(event:Event):
    if(event.__class__ not in subscribers):
        raise EventPostingException("Event you posted has no subscribers or does not exist!")
    
    for subscriber in subscribers[event.__class__]:
        args = event.getData()
        if args is None:
            subscriber()
        else:
            subscriber(args)