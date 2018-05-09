from . import deprecated
if deprecated.allowed():
    from . network.udp import Sender, QueuedSender, Receiver, QueuedReceiver
