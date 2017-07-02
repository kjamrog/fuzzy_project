import numpy as np
import skfuzzy as fuzz

price_limit = 1200

#CPU
cpu_range = np.arange(1.5, 4.2, 0.1)
cpu_bslaby = fuzz.trapmf(cpu_range, [1, 1.5, 2.4, 2.6])
cpu_slaby = fuzz.trimf(cpu_range, [2.4, 2.6, 2.8])
cpu_sredni = fuzz.trimf(cpu_range, [2.65, 2.85, 3.1])
cpu_mocny = fuzz.trapmf(cpu_range, [2.9, 3.4, 5, 5.65])

#RAM
ram_range = np.arange(3, 10, 0.5)
ram_slaby = fuzz.trapmf(ram_range, [0.48, 2.7, 4, 5])
ram_sredni = fuzz.trimf(ram_range, [4.4, 5.4, 7])
ram_mocny = fuzz.trapmf(ram_range, [6, 7.5, 10.3, 12.5])

#DRIVE
driv_range = np.arange(256, 6150, 128)
driv_slaby = fuzz.trapmf(driv_range, [-1866, 0, 768, 1300])
driv_sredni = fuzz.trimf(driv_range, [1000, 1536, 2400])
driv_mocny = fuzz.trapmf(driv_range, [2000, 3000, 6386, 8272])

#PRICE
price_range = np.arange(0, 3000, 1)
price_acceptable = fuzz.trapmf(price_range, [-700, -80, price_limit, 1.15*price_limit])

#OUTPUT
out_range = np.arange(0, 1, 0.05)
out_slaby = fuzz.trapmf(out_range, [-1, -0.5, 0.25, 0.5])
out_sredni = fuzz.trimf(out_range, [0.25, 0.5, 0.75])
out_mocny = fuzz.trapmf(out_range, [0.5, 0.75, 1.25, 1.5])

#fuzzification
cpu = 0
ram = 0
drive = 0
price = 0
output = [0 for el in range(13)]

cpu_bslaby_level = ('bslaby', fuzz.interp_membership(cpu_range, cpu_bslaby, cpu))
cpu_slaby_level = ('slaby', fuzz.interp_membership(cpu_range, cpu_slaby, cpu))
cpu_sredni_level = ('sredni', fuzz.interp_membership(cpu_range, cpu_sredni, cpu))
cpu_mocny_level = ('mocny', fuzz.interp_membership(cpu_range, cpu_mocny, cpu))

ram_slaby_level = ('slaby', fuzz.interp_membership(ram_range, ram_slaby, ram))
ram_sredni_level = ('sredni', fuzz.interp_membership(ram_range, ram_sredni, ram))
ram_mocny_level = ('mocny', fuzz.interp_membership(ram_range, ram_mocny, ram))

driv_slaby_level = ('slaby', fuzz.interp_membership(driv_range, driv_slaby, drive))
driv_sredni_level = ('sredni', fuzz.interp_membership(driv_range, driv_sredni, drive))
driv_mocny_level = ('mocny', fuzz.interp_membership(driv_range, driv_mocny, drive))

price_acceptable_level = ('akceptowalna', fuzz.interp_membership(price_range, price_acceptable, price))

cpu_level = max([cpu_bslaby_level, cpu_slaby_level, cpu_sredni_level, cpu_mocny_level], key=lambda x: x[1])
ram_level = max([ram_slaby_level, ram_sredni_level, ram_mocny_level], key=lambda x: x[1])
drive_level = max([driv_slaby_level, driv_sredni_level, driv_mocny_level], key=lambda x: x[1])
price_level = price_acceptable_level

cpu = cpu_level[0]
ram = ram_level[0]
drive = drive_level[0]
price = 'akceptowalna' if price_level != 0 else 'nieakceptowalna'

'''
Tego wyliczania z MIN nie jestem pewien jeszcze
'''
#RULES
if price != 'akceptowalna':
    output[0] == ('slaby', price_level)
if cpu == 'mocny' and ram != 'slaby' and drive != 'slaby' and price == 'akceptowalna':
    output[1] == ('mocny', min([cpu_mocny_level, ram_sredni_level, ram_mocny_level, driv_sredni_level, driv_mocny_level, price_level], key=lambda x: x[1]))
if cpu == 'sredni' and ram == 'mocny' and drive == 'mocny' and price == 'akceptowalna':
    output[2] == ('mocny', min([cpu_sredni_level, ram_mocny_level, driv_mocny_level, price_level], key=lambda x: x[1]))
if cpu == 'sredni' and ram == 'slaby' and drive == 'slaby' and price == 'akceptowalna':
    output[3] == ('slaby', min([cpu_sredni_level, ram_slaby_level, driv_slaby_level, price_level], key=lambda x: x[1]))
if cpu == 'sredni' and ram == 'sredni' and price == 'akceptowalna':
    output[4] == ('sredni', min([cpu_sredni_level, ram_sredni_level, price_level], key=lambda x: x[1]))
if cpu == 'sredni' and drive == 'sredni' and price == 'akceptowalna':
    output[5] == ('sredni', min([cpu_sredni_level, driv_sredni_level, price_level], key=lambda x: x[1]))
if cpu == 'slaby' and ram != 'mocny' and drive != 'mocny' and price == 'akceptowalna':
    output[6] == ('slaby', min([cpu_slaby_level, ram_slaby_level, ram_sredni_level, driv_slaby_level, driv_sredni_level, price_level], key=lambda x: x[1]))
if cpu == 'slaby' and ram == 'mocny' and drive == 'mocny' and price == 'akceptowalna':
    output[7] == ('sredni', min([cpu_slaby_level, ram_mocny_level, driv_mocny_level, price_level], key=lambda x: x[1]))
if cpu == 'bslaby' and price == 'akceptowalna':
    output[8] == ('slaby', min([cpu_bslaby_level, price_level], key=lambda x: x[1]))
if cpu == 'mocny' and ram == 'slaby' and price == 'akceptowalna':
    output[9] == ('sredni', min([cpu_mocny_level, ram_slaby_level, price_level], key=lambda x: x[1]))
if cpu == 'mocny' and ram != 'mocny' and drive == 'slaby' and price == 'akceptowalna':
    output[10] == ('sredni', min([cpu_mocny_level, ram_slaby_level, ram_sredni_level, driv_slaby_level, price_level], key=lambda x: x[1]))
if cpu == 'mocny' and ram == 'mocny' and drive == 'slaby' and price == 'akceptowalna':
    output[11] == ('mocny', min([cpu_mocny_level, ram_mocny_level, driv_slaby_level, price_level], key=lambda x: x[1]))
if cpu == 'sredni' and ram != 'mocny' and drive != 'mocny' and price == 'akceptowalna':
    output[12] == ('sredni', min([cpu_sredni_level, ram_slaby_level, ram_sredni_level, driv_slaby_level, driv_sredni_level, price_level], key=lambda x: x[1]))



#0 0 0 -1 1
#4 -1 -1 1 3
#3 3 3 1 3
#3 1 1 1 1
#3 2 0 1 2
#3 0 2 1 2
#2 -3 -3 1 1
#2 3 3 1 2
#1 0 0 1 1
#4 1 0 1 2
#4 -3 1 1 2
#4 3 1 1 3
#3 -3 -3 1 2
