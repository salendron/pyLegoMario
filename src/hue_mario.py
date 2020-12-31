"""
Phillips Hue Remote Sample
src/hue_mario.py shows howto use Lego Mario to control your Hue lights by
tilting Mario forward or backward.
You have to change light Ids in this sample to match your Hue setup. Use
DebugPrintAllLights method of the HueController to see which light ids 
you have and in which configuration your lights are the moment, so you can alter
the Scene Methods (SetBrightLights, SetCozyLights) to control your Hue lights
correctly.
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
from phue import Bridge

# Change this to match your Hue Bridge IP
HUE_BRIDGE_IP = "192.168.1.124"

class HueController:

    def __init__(self, bridge_ip):
        try:
            self.bridge_api = Bridge(bridge_ip)
        except:
            input("Press Hue Connect Button and then hit enter to continue")
            self.bridge_api = Bridge(bridge_ip)
            self.bridge_api.connect()

    def DebugPrintAllLights(self):
        lights = self.bridge_api.get_light_objects('id')

        for key in lights:
            l = lights[key]
            name = l.name
            on = l.on
            brightness = l.brightness

            try:
                hue = l.hue
            except KeyError:
                hue = None

            try:
                saturation = l.saturation
            except KeyError:
                saturation = None

            print("Key: %s, Name: %s, On: %s, Brightness: %s, Hue: %s, Saturation: %s" % (key, name, on, brightness, hue, saturation))

    def TurnAllLightsOff(self):
        lights = self.bridge_api.lights

        for l in lights:
            self.bridge_api.set_light(l.light_id, 'on', False)

    def SetBrightLights(self):
        lights = self.bridge_api.get_light_objects('id')
        light_group_ids = [1,2,8,14,15,24,25] 

        for l_id in light_group_ids:
            if l_id == 8: #hue iris
                lights[l_id].on = True
                lights[l_id].brightness = 254
                lights[l_id].hue = 12828
                lights[l_id].saturation = 52
            else: # hue color light bulps
                lights[l_id].on = True
                lights[l_id].brightness = 254
                lights[l_id].hue = 8404
                lights[l_id].saturation = 140

    def SetCozyLights(self):
        lights = self.bridge_api.get_light_objects('id')
        light_group_ids = [1,2,8,14,15,24,25] 

        for l_id in light_group_ids:
            lights[l_id].on = True

            if l_id == 1:
                lights[l_id].brightness = 117
                lights[l_id].hue = 56856
                lights[l_id].saturation = 148
            elif l_id == 2:
                lights[l_id].brightness = 117
                lights[l_id].hue = 49032
                lights[l_id].saturation = 152
            elif l_id == 8:
                lights[l_id].brightness = 146
                lights[l_id].hue = 5037
                lights[l_id].saturation = 220
            elif l_id == 14:
                lights[l_id].brightness = 117
                lights[l_id].hue = 48694
                lights[l_id].saturation = 216
            elif l_id == 15:
                lights[l_id].brightness = 117
                lights[l_id].hue = 48694
                lights[l_id].saturation = 216
            elif l_id == 24:
                lights[l_id].brightness = 230
                lights[l_id].hue = 49483
                lights[l_id].saturation = 140
            elif l_id == 25:
                lights[l_id].brightness = 215
                lights[l_id].hue = 52889
                lights[l_id].saturation = 230

    def MarioAccelerometerEventHandler(self, x, y, z):
        if x > -4 and x < 4 and y > 26 and y < 34 and z > -4 and z < 4:
            self.SetBrightLights()
        elif x > -4 and x < 4 and y > -4 and y < 4 and z > 26 and z < 34:
            self.TurnAllLightsOff()
        elif x > -4 and x < 4 and y > -4 and y < 4 and z < -26 and z > -34:
            self.SetCozyLights()

if __name__ == "__main__":
    hue = HueController(HUE_BRIDGE_IP)
    
    # Initialize Mario
    mario = Mario()

    # Add Hook Functions
    mario.AddAccelerometerHook(hue.MarioAccelerometerEventHandler)

    # turn of log. Turn it on if you need it.
    mario._doLog = False

    # Start searching and reading data from Mario
    print("Turn on Mario and press Bluetooth Button")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mario.Run())