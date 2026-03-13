from typing import Any

from typing_extensions import Self

from ...element import Element
from ...event import Event
from ...events import GenericEventArguments, Handler, JoystickEventArguments


class Joystick(Element, component='joystick.js', esm={'nicegui-joystick': 'dist'}, default_classes='nicegui-joystick'):

    def __init__(self, *,
                 on_start: Handler[JoystickEventArguments] | None = None,
                 on_move: Handler[JoystickEventArguments] | None = None,
                 on_end: Handler[JoystickEventArguments] | None = None,
                 throttle: float = 0.05,
                 **options: Any) -> None:
        """Joystick

        Create a joystick based on `nipple.js <https://yoannmoi.net/nipplejs/>`_.

        :param on_start: callback for when the user touches the joystick
        :param on_move: callback for when the user moves the joystick
        :param on_end: callback for when the user releases the joystick
        :param throttle: throttle interval in seconds for the move event (default: 0.05)
        :param options: arguments like `color` which should be passed to the `underlying nipple.js library <https://github.com/yoannmoinet/nipplejs#options>`_
        """
        super().__init__()
        self._props['options'] = options
        self.active = False

        self._start_event: Event = Event()
        self._move_event: Event = Event()
        self._end_event: Event = Event()
        if on_start:
            self._start_event.subscribe(on_start)
        if on_move:
            self._move_event.subscribe(on_move)
        if on_end:
            self._end_event.subscribe(on_end)

        def handle_start() -> None:
            self.active = True
            args = JoystickEventArguments(sender=self, client=self.client, action='start')
            self._start_event.emit(args)

        def handle_move(e: GenericEventArguments) -> None:
            if self.active:
                args = JoystickEventArguments(sender=self,
                                              client=self.client,
                                              action='move',
                                              x=float(e.args['data']['vector']['x']),
                                              y=float(e.args['data']['vector']['y']))
                self._move_event.emit(args)

        def handle_end() -> None:
            self.active = False
            args = JoystickEventArguments(sender=self,
                                          client=self.client,
                                          action='end')
            self._end_event.emit(args)

        self.on('start', handle_start, [])
        self.on('move', handle_move, ['data'], throttle=throttle)
        self.on('end', handle_end, [])

    def on_start(self, callback: Handler[JoystickEventArguments]) -> Self:
        """Add a callback to be invoked when the user touches the joystick."""
        self._start_event.subscribe(callback)
        return self

    def on_move(self, callback: Handler[JoystickEventArguments]) -> Self:
        """Add a callback to be invoked when the user moves the joystick."""
        self._move_event.subscribe(callback)
        return self

    def on_end(self, callback: Handler[JoystickEventArguments]) -> Self:
        """Add a callback to be invoked when the user releases the joystick."""
        self._end_event.subscribe(callback)
        return self
