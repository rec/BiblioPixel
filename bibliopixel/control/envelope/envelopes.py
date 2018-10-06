from .. import control
from . import envelope


class Envelopes(control.Control):
    def __init__(self, envelopes=None, **kwds):
        """
        """
        super().__init__(self, **kwds)

        envelopes = envelopes or {}
        unknown = set(self.routing) - set(envelopes)
        if unknown:
            plural = '' if len(unknown) == 1 else 's'
            unk = ', '.join(str(i) for i in unknown)
            raise ValueError('Unknown envelope%s: %s' % (plural, unk))

        self.envelopes = {k: envelope.Envelope(v) for k, v in envelopes.items()}
        self.start_time = 0

    def set_root(self, root):
        super().set_root(root)
        root.animation.add_preframe_callback(self.preframe_callback)

        for action_list in self.routing.routing.values():
            if isinstance(action_list, dict):
                raise ValueError('Nested routing is not allowed in Envelopes')
            for action in action_list.actions:
                action.address.edit_queue = None

    def preframe_callback(self):
        time = self.root.clock.time()
        self.start_time = self.start_time or time
        delta_time = time - self.start_time

        for name, action_list in self.routing.routing.items():
            envelope = self.envelopes[name]
            value = envelope(delta_time)
            action_list.receive((value,))
