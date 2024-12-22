import serial
import threading
import controls
from datetime import datetime as dt

callbacks = list()
ser = serial.Serial('COM2', baudrate=115200, timeout=1)


def register_callback(callback):
    print(f'Register callback')
    callbacks.append(callback)


def unregister_callback(callback):
    print(f'Unregister callback')
    callbacks.remove(callback)


def on_message(message):
    print(f"{dt.now()} Received: {message}")
    print(f'SERIAL: Current number of callbacks {len(callbacks)}')
    for callback in callbacks:
        try:
            callback(message)
        except Exception as e:
            print(f'Exception Calling Serial Callback {e}')


def thread_serial_read_loop():
    while True:
        # time.sleep(1)
        # print('SerialComm loop')
        payload = ser.readline()
        if payload:
            on_message(payload)
            print(f'Serial Incoming Payload {payload}')


loop = threading.Thread(target=thread_serial_read_loop, args=())
