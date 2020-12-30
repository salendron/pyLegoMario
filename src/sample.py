"""
SAMPLE.PY
This is a sample on how to use mario.py. It shows how to register event hook 
functions and how to let the script run as an endless loop.
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
from mario import Mario

def my_tile_hook(t):
    """
    Test Function which will be called as soon as a tile is detected by Mario.
    t will contain the ID of the tile that was deteced.

    START = 0
    GOAL = 1
    RED = 2
    GREEN = 3
    """
    print(t)

def my_accelerometer_hook(x, y, z):
    """
    Test Function which will be called for every change in x, y or z accelerometer value.
    """
    print("X: %i Y: %i Z: %i" % (x, y, z))


if __name__ == "__main__":
    # Initialize Mario
    mario = Mario()

    # Add Hook Functions
    mario.AddAccelerometerHook(my_accelerometer_hook)
    mario.AddTileHook(my_tile_hook)

    # turn of log. Turn it on if you need it.
    mario._doLog = False

    # Start searching and reading data from Mario
    print("Turn on Mario and press Bluetooth Button")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mario.Run())