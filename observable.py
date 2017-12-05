from collections import defaultdict


class Observable():
    """
    A very simple observable class which allows observers to register
    callbacks for arbitrary events.
    """
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.events = defaultdict(set)

    def register(self, event, callback):
        """
        Register a callback for a particular event.

        Let an observer register a callback to be fired when the given event
        is dispatched.

        Args:
            event (str): The name of the event.
            callback (function): A function to be called when the event fires.
        """
        self.events[event].add(callback)

    def unregister(self, event, callback):
        """
        Unregister a callback for a particular event.

        Stop the Observable from calling a previously registered callback when
        the given event is dispatched.

        Args:
            event (str): The name of the event.
            callback (function): The previously registered callback function.
        """
        self.events[event].remove(callback)

    def dispatch(self, event, values):
        """
        Dispatch an event, calling any registered callbacks.

        Args:
            event (str): The name of the event.
            values (list): Arguments to be passed to the callbacks.
        """
        for callback in self.events[event]:
            callback(*values)
