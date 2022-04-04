# notecard test code sample
import board
import busio
import notecard
productUID = "com.example.name:project_name"
# Create bus object using our board's I2C port
i2c = busio.I2C(board.GP17, board.GP16)

# Create relay object
card = notecard.OpenI2C(i2c, 0, 0, debug=True)

req = {"req": "hub.set"}
req["product"] = productUID
req["mode"] = "periodic"
req["inbound"] = 120
req["outbound"] = 60
req["sync"] = True
rsp = card.Transaction(req)

while True:
    pass
