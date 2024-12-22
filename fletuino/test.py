import serial
import json

test = [{"type": "Text", "name": "t1", "text": "Test me", "size": 20},
        {"type": "Text", "name": "t2", "text": "Test me again", "size": 20},
        {"type": "Button", "name": "b1", "text": "Click me", "size": 20, "color": "red", "bgcolor": "yellow"},
        {"type": "Button", "name": "b2", "text": "Click me", "size": 30, "color": "red", "bgcolor": "yellow"},
        {"type": "Dropdown", "name": "dd1", "text": "Choose", "size": 20, "options":['down', 'above']},
        {"type": "Slider", "name": "sl1", "text": "Slide me", "size": 20, "color": "red", "bgcolor": "yellow"},]

if __name__ == "__main__":
    s = serial.Serial(port='Com3', baudrate=115200)
    for t in test:
        x = json.dumps(t) + '\n'
        s.write(x.encode())
