import unittest
import bibliopixel

from bibliopixel.main import demo, main, run, set, show

from bibliopixel.threads import (
    animation_threading, compose_events, producer_consumer, task_thread,
    threads, update_threading)

from bibliopixel.drivers.SimPixel import driver, websocket

from bibliopixel import (
    animation,
    colors,
    data_maker,
    font,
    gamepad,
    gamma,
    image,
    layout,
    led,
    log,
    matrix,
    return_codes,
    # serial_gamepad,  # Needs gamepad, only available on Windows
    util,
)

from bibliopixel.drivers import (
    APA102,
    LPD8806,
    WS2801,
    driver_base,
    dummy_driver,
    hue,
    image_sequence,
    network,
    network_receiver,
    network_udp,
    serial_driver,
    spi_driver_base,
)


class ImportAllTest(unittest.TestCase):
    def test_all(self):
        # We pass just by successfully importing everything above.
        pass
