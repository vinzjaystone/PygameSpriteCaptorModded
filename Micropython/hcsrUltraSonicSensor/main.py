#main.py
from machine import Pin

pin = ""
led = ""
def  setupTestPin():
    global pin
    pin = Pin(2, Pin.OUT)
    
def testToggleDelay():
    import time
    
    global pin
    for i in range(10):
        toggle(pin)
        time.sleep_ms(500)
        
def toggle(p):
    p.value(not p.value())
   
   
#interrupts test
def debounce(pin):
    prev = None
    for i in range(32):
        cv = pin.value()
        if prev != None and prev != cv:
            return None
        prev = cv
    return prev

def button_callback(pin):
    global led
    if debounce(pin) == None:
        return
    elif not debounce(pin):
        led.value(not led.value())
        print('Trigger found')

def main2():
    global led
    import time
    from machine import Pin, Timer
    led = Pin(2, Pin.OUT)
    #timer = Timer(-1)
    #timer.init(period=2500, mode=Timer.PERIODIC, callback=lambda t:led.value(not led.value()))
    button = Pin(0, Pin.IN, Pin.PULL_UP)
    button.irq(trigger=Pin.IRQ_FALLING, handler=button_callback)
    count = 0
    while True:
        time.sleep_ms(500)
        print('>> {}'.format(count))
        count+=1

def main():
    import time
    from machine import Pin
    from hcsr04 import HCSR04 as hc
    
    sensor = hc(trigger_pin=14, echo_pin=12, echo_timeout_us=1000000)
    try:
        while True:
            dist = sensor.distance_cm()
            print("Distance : {} cm".format(dist))
            time.sleep_ms(500)
    except KeyboardInterrupt:
        pass
            