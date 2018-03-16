from enum import IntEnum
from .. util import log


class RETURN_CODES(IntEnum):
    SUCCESS = 255  # All is well
    REBOOT = 42  # Device reboot needed after configuration
    ERROR = 0  # Generic error
    ERROR_SIZE = 1  # Data received does not match given command length
    ERROR_UNSUPPORTED = 2  # Unsupported command
    ERROR_PIXEL_COUNT = 3  # Too many pixels for device
    ERROR_BAD_CMD = 4  # Unknown Command
    NONE = 512  # The device did not respond
    EMPTY = 1024  # The device responded with an empty packet


RETURN_CODE_ERRORS = {
    RETURN_CODES.SUCCESS: 'Success!',
    RETURN_CODES.REBOOT: 'Device reboot needed after configuration.',
    RETURN_CODES.ERROR: 'Generic error',
    RETURN_CODES.ERROR_SIZE: 'Data packet size incorrect.',
    RETURN_CODES.ERROR_UNSUPPORTED: 'Unsupported configuration attempted.',
    RETURN_CODES.ERROR_PIXEL_COUNT: 'Wrong number of pixels for device.',
    RETURN_CODES.ERROR_BAD_CMD:
        'Unsupported protocol command. Check your device version.',
    RETURN_CODES.NONE:
        'The device did not respond.  Check your connections and cables',
    RETURN_CODES.EMPTY:
        'The device responded with an empty packet',
}

UNKNOWN_ERROR = 'Unknown error occured.'


class SerialError(RuntimeError):
    pass


class ReturnCode:
    def __init__(self, com):
        resp = com.read(1)
        if resp is None:
            self.code = RETURN_CODES.NO_RESPONSE
        elif not resp:
            self.code = RETURN_CODES.EMPTY_RESPONSE
        else:
            self.code = ord(resp)

    def __str__(self):
        msg = RETURN_CODE_ERRORS.get(self.code, UNKNOWN_ERROR)
        return '%s: %s' % (self.code, msg)

    def check(self, *codes, fail=True):
        codes = RETURN_CODE.SUCCESS, *codes
        if self.code == RETURN_CODE.SUCCESS:
            return
        if not needs_success and self.code == RETURN_CODE.NO_RESPONSE:
            return
        log.error(self)
        if fail:
            raise SerialError(self)


from .. util import deprecated
if deprecated.allowed():
    BiblioSerialError = SerialError

    def print_error(error):
        msg = RETURN_CODE_ERRORS.get(error, )
        log.error('%s: %s', error, msg)
        return msg


    def raise_error(error):
        raise SerialError(print_error(error))
