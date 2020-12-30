# pyLegoMario
src/mario.py is a little script that connects to Lego Mario and then reads its
acceleromter and tile sensor data. It does so until you call Stop() and turn of 
Mario. It also automatically reconnects to Mario if it it looses the connection.
To connect you have to turn Mario on and then press the Bluetooth Button.
See src/sample.py for a full sample on how to use it.


## TL;DR;
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
