"""
MARIO.PY
This is a little script that connects to Lego Mario and then reads its
acceleromter and tile sensor data. It does so until you call Stop() and turn of 
Mario. It also automatically reconnects to MArio if it it looses the connection.
To connect you have to turn Mario on and then press the Bluetooth Button.
See sample.py on how to use it.
###################################################################################
MIT License
Copyright (c) 2020 Bruno Hautzenberger
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import time
from bleak import BleakScanner, BleakClient

# BLE Connection and Event Subscription
LEGO_CHARACTERISTIC_UUID = "00001624-1212-efde-1623-785feabcd123"
SUBSCRIBE_IMU_COMMAND = bytearray([0x0A, 0x00, 0x41, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x01])
SUBSCRIBE_RGB_COMMAND = bytearray([0x0A, 0x00, 0x41, 0x01, 0x00, 0x05, 0x00, 0x00, 0x00, 0x01])

# TILE IDS
TILE_START = 0
TILE_GOAL = 1
TILE_RED = 2
TILE_GREEN = 3

class Mario:

    def __init__(self):
        self._tileEventHooks = []
        self._accelerometerEventHooks = []
        self._doLog = True
        self._run = True

    def _signed(self, char):
        return char - 256 if char > 127 else char

    def _log(self, msg):
        if self._doLog:
            print(msg)

    def AddTileHook(self, func):
        self._tileEventHooks.append(func)

    def AddAccelerometerHook(self, func):
        self._accelerometerEventHooks.append(func)

    def _callTileHooks(self, v):
        for func in self._tileEventHooks:
            func(v)

    def _callAccelerometerHooks(self, x, y, z):
        for func in self._accelerometerEventHooks:
            func(x, y, z)

    def _handle_events(self, sender, data):
        # Camera sensor data
        if data[0] == 8:
            # RGB code
            if data[5] == 0x0:
                if data[4] == 0xb8:
                    self._log("Start tile")
                    self._callTileHooks(TILE_START)
                if data[4] == 0xb7:
                    self._log("Goal tile")
                    self._callTileHooks(TILE_GOAL)
                self._log("Barcode: " + " ".join(hex(n) for n in data))
            # Red tile
            elif data[6] == 0x15:
                self._log("Red tile")
                self._callTileHooks(TILE_RED)
            # Green tile
            elif data[6] == 0x25:
                self._log("Green tile")
                self._callTileHooks(TILE_GREEN)
            # Unknow tile
            else:
                self._log("Unknown tile %s" % hex(data[6]))

        # Accelerometer data
        elif data[0] == 7:
            x = int(self._signed(data[4]))
            y = int(self._signed(data[5]))
            z = int(self._signed(data[6]))
            self._log("X: %i Y: %i Z: %i" % (x, y, z))
            self._callAccelerometerHooks(x, y, z)

    async def Run(self):
        self._run = True
        while self._run:
            self._log("Searching for Mario...")
            devices = await BleakScanner.discover()
            for d in devices:
                if d.name.lower().startswith("lego mario"):
                    try:
                        async with BleakClient(d.address) as client:
                            await client.is_connected()
                            self._log("Mario Connected")
                            await client.start_notify(LEGO_CHARACTERISTIC_UUID, self._handle_events)
                            await asyncio.sleep(0.1)
                            await client.write_gatt_char(LEGO_CHARACTERISTIC_UUID, SUBSCRIBE_IMU_COMMAND)
                            await asyncio.sleep(0.1)
                            await client.write_gatt_char(LEGO_CHARACTERISTIC_UUID, SUBSCRIBE_RGB_COMMAND)
                            while await client.is_connected() and self._run:
                                await asyncio.sleep(0.05)
                    except:
                        pass

    def Stop(self):
        self._run = False
