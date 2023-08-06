This is a library for Raspberry Pi Pico and AS7343 Spectral Sensor

requirements:
machine

example code:

import AS7343
as_7343=AS7343.AS7343(0,YOUR_SDA_PIN,YOUR_SCL_PIN,0x39)
as_7343.power(True) #start AS7343
as_7343.direct_config()
as_7343.set_cycle(3)
as_7343.optimizer(max_TINT=1000)#auto set
data=as_7343.get(output=dict)#get data
print(data)