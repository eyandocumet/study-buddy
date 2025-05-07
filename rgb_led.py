# Runs on boot - Controls RGB color spectrum of an LED
# Eyan Documet
from machine import Pin, PWM, ADC
from time import sleep

# Setup RGB PWM
r = PWM(Pin(14), freq=1000)
g = PWM(Pin(32), freq=1000)
b = PWM(Pin(15), freq=1000)

# Setup ADC for potentiometer
pot = ADC(Pin(26))
pot.atten(ADC.ATTN_11DB)  # 0–3.3V range
pin_in = Pin(12, Pin.IN)

def set_color(r_val, g_val, b_val):
    r.duty(int(r_val))
    g.duty(int(g_val))
    b.duty(int(b_val))

while True:
    val = pot.read()  # 0–4095
    ratio = val / 4095
    print(f"Potentiometer: {val} ({ratio:.2f})")
        
    # Interpolate between white (1023,1023,1023) and amber (1023, 300, 0)
    r_val = 1023 * (1 - pin_in.value())
    g_val = int(1023 - ratio * (1023 - 300)) * (1 - pin_in.value())
    b_val = int(1023 - ratio * 1023) * (1 - pin_in.value())

    set_color(r_val, g_val, b_val)
    sleep(0.05)

