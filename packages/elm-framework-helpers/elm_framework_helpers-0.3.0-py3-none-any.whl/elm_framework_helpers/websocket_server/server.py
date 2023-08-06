import reactivex
from reactivex import Subject, operators
from reactivex.scheduler import EventLoopScheduler
from threading import Thread
from typing import Any
from elm_framework_helpers.websocket_server import models
from websocket_server import WebsocketServer


class HtmxWebsocketServer(WebsocketServer):
    _context: Any
    _parameters_context: Any
    _new_clients: Subject
    _scheduler: reactivex.abc.SchedulerBase

    def __init__(self, context, parameters_context, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._context = context
        self._parameters_context = parameters_context
        self._new_clients = Subject()
        self.set_fn_new_client(lambda *_: self._new_clients.on_next(None))
        self._scheduler = EventLoopScheduler(
            thread_factory=lambda target: Thread(
                target=target, daemon=True, name="WebsocketTriggers"
            )
        )

    def add_trigger(
        self,
        trigger: models.WebsocketTrigger,
        plain=False,
    ):
        def on_message(value):
            try:
                content = trigger.callback(
                    self._context, self._parameters_context, trigger.name, value
                )
            except Exception as e:
                content = f"Failed to render content for {trigger.name}: {e}"
            if plain:
                return content
            hx_swap_oob = f'hx-swap-oob="{trigger.oob_swap}"'
            return f'<div id="{trigger.name}" {hx_swap_oob}>{content}</div>'

        if trigger.trigger_on_new_client:
            source = trigger.source.pipe(
                operators.combine_latest(self._new_clients),
                operators.map(
                    lambda x: x[0]
                ),  # don't want value to become a tuple inclusive of the client
            )
        else:
            source = trigger.source
        source.pipe(
            operators.observe_on(self._scheduler),
        ).subscribe(lambda value: self.send_message_to_all(on_message(value)))
