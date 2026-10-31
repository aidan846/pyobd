"""Connects to a simulated ELM327 adapter over TCP (the same way a WiFi
adapter is reached) and reads a few values.

Needs the ELM327-emulator package (pip install -r requirements-dev.txt);
the test is skipped when it isn't installed.
"""
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import obd  # noqa: E402  (the copy bundled with pyobd)


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def emulator_command():
    exe = shutil.which("elm", path=os.path.dirname(sys.executable)) or shutil.which("elm")
    return [exe] if exe else None


@unittest.skipUnless(emulator_command(), "ELM327-emulator is not installed")
class WifiAdapterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.port = free_port()
        cls.workdir = tempfile.mkdtemp()
        cls.emulator = subprocess.Popen(
            emulator_command() + ["-n", str(cls.port), "-s", "car",
                                  "-b", os.path.join(cls.workdir, "emulator.out")],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        deadline = time.time() + 30
        while time.time() < deadline:
            try:
                socket.create_connection(("127.0.0.1", cls.port), timeout=1).close()
                break
            except OSError:
                time.sleep(0.2)
        else:
            cls.emulator.kill()
            raise RuntimeError("emulator did not start")

    @classmethod
    def tearDownClass(cls):
        cls.emulator.terminate()
        cls.emulator.wait(timeout=10)
        shutil.rmtree(cls.workdir, ignore_errors=True)

    def connect(self, protocol=None):
        conn = obd.OBD("socket://127.0.0.1:%d" % self.port, protocol=protocol,
                       fast=False, timeout=2, check_voltage=False)
        self.addCleanup(conn.close)
        return conn

    def test_auto_protocol(self):
        conn = self.connect()
        self.assertEqual(conn.status(), obd.OBDStatus.CAR_CONNECTED)
        self.assertIsNotNone(conn.query(obd.commands.RPM).value)
        self.assertIsNotNone(conn.query(obd.commands.SPEED).value)

    def test_manual_protocol(self):
        conn = self.connect(protocol="6")
        self.assertEqual(conn.status(), obd.OBDStatus.CAR_CONNECTED)
        self.assertIn("CAN 11/500", conn.protocol_name())


if __name__ == "__main__":
    unittest.main()
