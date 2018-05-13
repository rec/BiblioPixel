import os, time, queue, unittest
from bibliopixel.control import artnet
from bibliopixel.util import artnet_message, udp, json
from .. project import make
from .. import mark_tests
from test.bibliopixel.util.network import udp_test


class ArtNetControlTest(unittest.TestCase):
    @mark_tests.fails_in_travis
    def test_artnet_control(self):
        project = make_project(ARTNET_CONTROL)
        results = []
        project.test_callback = results.append
        project.controls[0].set_root(project)
        sender = udp.QueuedSender(SEND_ADDRESS)

        with project.controls[0].joiner(), sender.joiner():
            sender.send(OUTGOING_MESSAGE)

        self.assertTrue(results)
        self.assertEquals(results[0], TEST_DATA)

    @mark_tests.fails_in_travis
    def test_artnet_integration(self):
        sender = udp.QueuedSender(SEND_ADDRESS)
        receiver = udp.QueuedReceiver(RECEIVE_ADDRESS)
        project = make_project(ARTNET_PROJECT)

        with sender.joiner(), receiver.joiner():
            project.start()
            time.sleep(0.01)
            sender.queue.put(OUTGOING_MESSAGE)
            project.join()

        result = []
        while True:
            try:
                result.append(receiver.queue.get(timeout=0.1))
            except queue.Empty:
                break

        msgs = [artnet_message.bytes_to_message(i) for i in result]
        data = [m.data for m in msgs]
        self.assertEqual(len(msgs), 3)
        self.assertTrue(not any(data[0]))
        self.assertTrue(not any(data[2]))
        actual = bytearray(data[1])

        # We expect to lose the last two bytes because we have uneven sizes.
        # TODO: perhaps we should round UP instead of DOWN?
        self.assertEqual(actual[:-2], TEST_DATA[:-2])
        self.assertEqual(actual[-2], 0)
        self.assertEqual(actual[-1], 0)


def make_project(datafile):
    data = json.loads(datafile, '.yml')
    return make.make_project(data)


ROOT_DIR = os.path.dirname(__file__)
TEST_DATA = bytearray(range(256)) + bytearray(range(256))
OUTGOING_MESSAGE = artnet_message.dmx_message(data=TEST_DATA)
PIXEL_COUNT = len(TEST_DATA) // 3

IP_ADDRESS = '127.0.0.1'
ARTNET_PORT = artnet_message.UDP_PORT
ALTERNATE_PORT = ARTNET_PORT + 1
SEND_ADDRESS = IP_ADDRESS, ARTNET_PORT
RECEIVE_ADDRESS = IP_ADDRESS, ALTERNATE_PORT


ARTNET_CONTROL = """
shape: 1

animation: animation

controls:
  typename: artnet
  ip_address: {IP_ADDRESS}
  pre_routing: ".test_callback()"
  extractor:
    omit: [type, net, subUni]
  verbose: True

run:
  threaded: true
""".format(**globals())


ARTNET_PROJECT = """
shape: {PIXEL_COUNT}

animation: animation

controls:
  typename: artnet
  ip_address: {IP_ADDRESS}
  port: {ARTNET_PORT}

  extractor:
    omit: [net, subUni]

  routing:
    dmx: animation.color_list

  verbose: True

driver:
  typename: artnet
  ip_address: {IP_ADDRESS}
  port: {ALTERNATE_PORT}

run:
  fps: 10
  max_steps: 3
  threaded: true
""".format(**globals())
