from typing import Any, Awaitable, Coroutine, Dict, List, Callable
from tools import Logger
from traceback import format_exc
import asyncio
import inspect

# Place custom events here (functions that subscribe must be awaitable)
class Event: ...

class TransectEvent(Event): ...
class LargeCoralColonyDetected(TransectEvent): ...
class OutplantDetected(TransectEvent): ...
class CrownOfThornsDetected(TransectEvent): ...
class SpongeDetected(TransectEvent): ...
class TransectEdgeDetected(TransectEvent): ...
class TransectStart(TransectEvent): ...
class TransectFailed(TransectEvent): ...


class SubscriptionException(Exception): ...

subscribers:Dict[Event, Any] = dict()

def SubscribeEvent(event_type:Event):
    """Decorator that subscribes async function to event event_type"""
    def subscribe(fn): # create wrapper function to manipulate wrapped fn
        if(not inspect.iscoroutinefunction(fn)): # ensure function has been defined as async def name(): ... (could add functionality for both but would add like 50 lines and its easy enough to write an asynchronous function that does not need to wait on anything :P)
            raise SubscriptionException("Cannot subscribe synchronous function to asynchronous event system")
        if not event_type in subscribers: # add subscribed event to subscription tracker
            subscribers[event_type] = []
        if fn in subscribers[event_type]: # ensure no function is subscribed twice
            try:
                raise SubscriptionException("Cannot subscribe function twice")
            except SubscriptionException:
                Logger.logError(format_exc())
                return fn
        subscribers[event_type].append(fn) # add function to subscribed event in tracker
        Logger.log(fn, "successfully subscribed to event " + event_type.__name__) # DEBUG log
        return fn
    return subscribe 

# TODO: ensure parameters match functions that have subscribed to an event before notifying them <--- expensive (calculate at subscription time??)
def post_event(event_type: Event, *args, **kwargs):
    """Post event and notify subscribers"""
    if not event_type in subscribers:
        print(f"Event '{event_type}' was posted, but either does not exist or has no subscribers")
        return
    # create list of coroutines to run
    coros:list[Coroutine] = []
    for fn in subscribers[event_type]:
        try:
            coros.append(fn(*args, **kwargs)) # create coroutines and add to list
        except TypeError: # if type error happens, attempted to create coroutine with arguments not accepted by it (not a big deal, log and move on)
            Logger.log(f"Attempted to create coroutine from function {fn} with arguments: {args} , {kwargs}")
            continue
    res = asyncio.run(__doCoros(coros)) # run all coroutines
    for i, result in enumerate(res):
        if result is not None: # if coroutine returned value, log and move on
            Logger.log(f"Function: {subscribers[event_type][i]} returned {result} when called on event bus")

async def __doCoros(coros):
    # await completion of all coroutines and return list of results
    return await asyncio.gather(*coros)