import math
#Input specifications:
'''
time = duration of the test (UNIT OF TIME)
amplitude = defines the peak intensity of traffic (NUMBER)
frequency = frequency of peaks for a set time frame (HZ)
baseline = baseline traffic level to simulate continuous background activity

specific-functions variables
time_scale  = controls the size of the sinewave per time frame (NUMBER)
power       = controls the power of the polynomial
'''
#function that returns a binary value
def signal_function(value):
    if value >= 0:
        return 1
    return 0

def sine_wave_function(amplitude = 10, baseline = 50, frequency = 0.1, current_time=1):
    return int(abs(baseline+(amplitude*math.sin(2*math.pi*frequency*current_time))))

def sudden_waves_function(amplitude=100, baseline=50, frequency=1, current_time=1):
    sine_value = math.sin(2 * math.pi * frequency * current_time)
    return int(baseline + amplitude * signal_function(sine_value))

def polynomial_function(amplitude=50, baseline=50, time_normalizer=20, current_time=1, power=2):
    #ensure time is not 0 to prevent division errors
    if time_normalizer <= 0:
        raise ValueError("DIVISION BY ZERO: time_normalizer variable is not set properly")
    
    normalized_time = current_time / time_normalizer
    return int(baseline + (amplitude*(normalized_time))** power)