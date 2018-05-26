import serial, serial.tools.list_ports
from distutils.version import LooseVersion
from . codes import CMDTYPE, LEDTYPE, SPIChipsets, BufferChipsets
from ... drivers.return_codes import RETURN_CODES, raise_error
from ... util import log, util
from ... project.importer import import_module


class Devices(object):
    """Manage a list of serial devices.

    :param str hardware_id: A valid USB VID:PID pair such as "1D50:60AB"
    :param int baudrate: Baud rate to connect to serial device
    """

    def __init__(self, hardware_id, baudrate):
        self.hardware_id = hardware_id
        self.baudrate = baudrate

    def find_serial_devices(self):
        """Scan and report all compatible serial devices on system.

        :returns: List of discovered devices
        """
        self.devices = {}
        hardware_id = "(?i)" + self.hardware_id  # forces case insensitive

        for ports in serial.tools.list_ports.grep(hardware_id):
            port = ports[0]
            try:
                id = self.get_device_id(port, self.baudrate)
                ver = self._get_device_version(port, self.baudrate)
            except:
                log.debug('Error getting device_id for %s, %s',
                          port, self.baudrate)
                if True:
                    raise
                continue

            if getattr(ports, '__len__', lambda: 0)():
                log.debug('Multi-port device %s:%s:%s with %s ports found',
                          self.hardware_id, id, ver, len(ports))
            if id < 0:
                log.debug('Serial device %s:%s:%s with id %s < 0',
                          self.hardware_id, id, ver)
            else:
                self.devices[id] = port, ver

        return self.devices

    def get_device(self, id=None):
        """Returns details of either the first or specified device

        :param int id: Identifier of desired device. If not given, first device
            found will be returned

        :returns tuple: Device ID, Device Address, Firmware Version
        """
        if id is None:
            if not self.devices:
                raise ValueError('No default device for %s' % self.hardware_id)
            id, (device, version) = sorted(self.devices.items())[0]

        elif id in self.devices:
            device, version = self.devices[id]

        else:
            error = 'Unable to find device with ID %s' % id
            log.error(error)
            raise ValueError(error)

        log.info("Using COM Port: %s, Device ID: %s, Device Ver: %s",
                 device, id, version)
        return id, device, version

    def error(self, fail=True, action=''):
        """
        SHOULD BE PRIVATE METHOD
        """
        e = 'There was an unknown error communicating with the device.'
        if action:
            e = 'While %s: %s' % (action, e)
        log.error(e)
        if fail:
            raise IOError(e)

    def set_device_id(self, dev, id, baudrate=921600):
        """Set device ID to new value.

        :param str dev: Serial device address/path
        :param id: Device ID to set
        :param baudrate: Baudrate to use when connectinh (optional)
        """
        if id < 0 or id > 255:
            raise ValueError("ID must be an unsigned byte!")

        com = serial.Serial(dev, baudrate=baudrate, timeout=5)

        packet = util.generate_header(CMDTYPE.SETID, 1)
        packet.append(id)
        com.write(packet)

        resp = com.read(1)
        if len(resp) == 0:
            self.error(action='set_device_id')
        elif ord(resp) != RETURN_CODES.SUCCESS:
            raise_error(ord(resp))

    def get_device_id(self, dev, baudrate=921600):
        """Get device ID at given address/path.

        :param str dev: Serial device address/path
        :param baudrate: Baudrate to use when connectinh (optional)
        """
        packet = util.generate_header(CMDTYPE.GETID, 0)
        com = serial.Serial(dev, baudrate=baudrate, timeout=5)
        com.write(packet)
        resp = com.read(1)
        if resp:
            return resp
        self.error(action='get_device_id')

    def _get_device_version(self, dev, baudrate=921600):
        packet = util.generate_header(CMDTYPE.GETVER, 0)
        com = serial.Serial(dev, baudrate=baudrate, timeout=0.5)
        com.write(packet)
        ver = 0
        resp = com.read(1)
        if len(resp) > 0:
            resp = ord(resp)
            if resp == RETURN_CODES.SUCCESS:
                ver = ord(com.read(1))
        return ver

    def _read_response(self, com):
        resp = com.read(1)
        return RETURN_CODES.NO_RESPONSE if resp is None else ord(resp)
