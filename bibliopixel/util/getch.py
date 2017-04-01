from ..threads.threads import Loop

# http://stackoverflow.com/a/32671356/43839

try:
    from msvcrt import getch  # try to import Windows version

except ImportError:
    def getch():   # define non-Windows version
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def keyboard_loop(callback, **kwds):
    return Loop(lambda: callback(getch()), **kwds)


def print_keycodes():
    while True:
        ch = getch()
        if ch == 'q':
            return
        print(ch)
        print(*(ord(c) for c in ch))
