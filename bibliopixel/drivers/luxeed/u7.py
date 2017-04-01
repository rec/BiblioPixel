from usb import core, util

ID_VENDOR = 0x04d8
ID_PRODUCT = 0xffcc

START_DATA = bytes([0xfb, 0xbf, 0xf1] + 61 * [0x00])


def endpoint():
    # https://github.com/walac/pyusb/blob/master/docs/tutorial.rst

    dev = core.find(idVendor=ID_VENDOR, idProduct=ID_PRODUCT)
    if not dev:
        raise ValueError('Luxeed U7 not found')

    dev.set_configuration()

    # get an endpoint instance
    cfg = dev.get_active_configuration()
    intf = cfg[(0,0)]

    def match_endpoint(e):
        # match the first OUT endpoint
        return util.endpoint_direction(e.bEndpointAddress) == util.ENDPOINT_OUT

    ep = util.find_descriptor(intf, custom_match=match_endpoint)
    if not ep:
        raise ValueError('Programmer error: Luxeed U7 endpoint not found.')

    ep.write(START_DATA)
    return ep
