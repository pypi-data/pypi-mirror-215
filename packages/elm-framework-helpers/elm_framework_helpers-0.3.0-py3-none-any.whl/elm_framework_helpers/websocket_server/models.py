
from typing import Callable, Any
from reactivex import Observable
from dataclasses import dataclass


WebsocketTriggerCallback = Callable[
    [Any, Any, str, Any], str
]


@dataclass
class WebsocketTrigger:
    name: str
    source: Observable
    callback: WebsocketTriggerCallback
    trigger_on_new_client: bool = True
    oob_swap: str = "outerHTML"

