# pyLegoMario
src/mario.py is a little script that connects to Lego Mario and then reads its
acceleromter and tile sensor data. It does so until you call Stop() and turn of 
Mario. It also automatically reconnects to Mario if it it looses the connection.
To connect you have to turn Mario on and then press the Bluetooth Button.
See src/sample.py for a full sample on how to use it.


## TL;DR;
"just show me how to use it!"
```python
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
```

## Phillips Hue Remote Sample
src/hue_mario.py shows howto use Lego Mario to control your Hue lights by
tilting Mario forward or backward.
You have to change light Ids in this sample to match your Hue setup. Use
DebugPrintAllLights method of the HueController to see which light ids 
you have and in which configuration your lights are the moment, so you can alter
the Scene Methods (SetBrightLights, SetCozyLights) to control your Hue lights
correctly.

Here is a [Video](https://youtu.be/PqH4nL4g9cMt)  that shows how the Mario Hue Remote works.
