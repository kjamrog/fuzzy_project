import numpy as np
import skfuzzy as fuzz


def inference_norm(norm, variables):
    cut_level = 1
    for i in range(len(variables)):
        cut_level = norm(cut_level, variables[i])
    return cut_level


# Hamacher T-norm (product)
# ( ab ) / ( a + b - ab )
# Hamacher T-conorm (sum)
# (a + b - 2ab) / (1 - ab)
def hamacher_norm(a, b):
    if a == 0 or b == 0:
        return 0
    return (a * b) / (a + b - a * b)


def calculate(max_price, computer, norm=hamacher_norm):
    # max_price = 1200 #given as argument

    # CPU
    cpu_range = np.arange(1.5, 4.2, 0.1)
    cpu_bslaby = fuzz.trapmf(cpu_range, [1, 1.5, 2.4, 2.6])
    cpu_slaby = fuzz.trimf(cpu_range, [2.4, 2.6, 2.8])
    cpu_sredni = fuzz.trimf(cpu_range, [2.65, 2.85, 3.1])
    cpu_mocny = fuzz.trapmf(cpu_range, [2.9, 3.4, 5, 5.65])

    # RAM
    ram_range = np.arange(3, 10, 0.1)
    ram_slaby = fuzz.trapmf(ram_range, [0.48, 2.7, 4, 5])
    ram_sredni = fuzz.trimf(ram_range, [4.4, 5.4, 7])
    ram_mocny = fuzz.trapmf(ram_range, [6, 7.5, 10.3, 12.5])

    # DRIVE
    driv_range = np.arange(256, 6150, 128)
    driv_slaby = fuzz.trapmf(driv_range, [-1866, 0, 768, 1300])
    driv_sredni = fuzz.trimf(driv_range, [1000, 1536, 2400])
    driv_mocny = fuzz.trapmf(driv_range, [2000, 3000, 6386, 8272])

    # PRICE
    price_range = np.arange(0, 3000, 1)
    price_acceptable = fuzz.trapmf(price_range, [-700, -80, max_price, 1.05 * max_price])

    # OUTPUT
    out_range = np.arange(0, 1, 0.05)
    out_slaby = fuzz.trapmf(out_range, [-1, -0.5, 0.25, 0.5])
    out_sredni = fuzz.trimf(out_range, [0.25, 0.5, 0.75])
    out_mocny = fuzz.trapmf(out_range, [0.5, 0.75, 1.25, 1.5])

    # FUZZIFICATION
    # get specific laptop data
    '''
    cpu = self.cpu_rate
    ram = self.ram_rate
    drive = self.drive_rate
    price 
    '''
    cpu = float(computer.cpu_rate)
    ram = float(computer.ram_rate)
    drive = float(computer.drive_rate)
    price = float(computer.price)
    output_cut_levels = [[] for el in range(13)]

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
    price = 'akceptowalna' if price_level[1] != 0 else 'nieakceptowalna'

    #print("CPU: {}\nRAM: {}\nDRIV: {}\nPRICE: {}, {}\n-------------------------------".format(cpu_level, ram_level, drive_level, price, price_level[1]))

    # RULES
    active_rules = []
    if price != 'akceptowalna':
        output_cut_levels[0] = ('slaby', price_level[1])
        active_rules.append(0)
    if cpu == 'mocny' and ram != 'slaby' and drive != 'slaby' and price == 'akceptowalna':
        # output_cut_levels[1] = ('mocny', (min([cpu_mocny_level, ram_sredni_level, ram_mocny_level, driv_sredni_level, driv_mocny_level, price_level], key=lambda x: x[1]))[1])
        output_cut_levels[1] = ('mocny', min(price_level[1], inference_norm(norm, [x[1] for x in
                                                                                            [cpu_mocny_level,
                                                                                             locals()['ram_'+ram+"_level"],
                                                                                             locals()['driv_'+drive+'_level']]])))
        active_rules.append(1)
    if cpu == 'sredni' and ram == 'mocny' and drive == 'mocny' and price == 'akceptowalna':
        # output_cut_levels[2] = ('mocny', (min([cpu_sredni_level, ram_mocny_level, driv_mocny_level, price_level], key=lambda x: x[1]))[1])
        output_cut_levels[2] = ('mocny', min(price_level[1], inference_norm(norm, [x[1] for x in
                                                                                            [cpu_sredni_level,
                                                                                             ram_mocny_level,
                                                                                             driv_mocny_level]])))
        active_rules.append(2)
    if cpu == 'sredni' and ram == 'slaby' and drive == 'slaby' and price == 'akceptowalna':
        # output_cut_levels[3] = ('slaby', (min([cpu_sredni_level, ram_slaby_level, driv_slaby_level, price_level], key=lambda x: x[1]))[1])
        output_cut_levels[3] = ('slaby', min(price_level[1], inference_norm(norm, [x[1] for x in
                                                                                            [cpu_sredni_level,
                                                                                             ram_slaby_level,
                                                                                             driv_slaby_level]])))
        active_rules.append(3)
    if cpu == 'sredni' and ram == 'sredni' and price == 'akceptowalna':
        # output_cut_levels[4] = ('sredni', (min([cpu_sredni_level, ram_sredni_level, price_level], key=lambda x: x[1]))[1])
        output_cut_levels[4] = ('sredni', min(price_level[1], inference_norm(norm, [x[1] for x in
                                                                                             [cpu_sredni_level,
                                                                                              ram_sredni_level]])))
        active_rules.append(4)
    if cpu == 'sredni' and drive == 'sredni' and price == 'akceptowalna':
        # output_cut_levels[5] = ('sredni', (min([cpu_sredni_level, driv_sredni_level, price_level], key=lambda x: x[1]))[1])
        output_cut_levels[5] = ('sredni', min(price_level[1], inference_norm(norm, [x[1] for x in
                                                                                             [cpu_sredni_level,
                                                                                              driv_sredni_level]])))
        active_rules.append(5)
    if cpu == 'slaby' and ram != 'mocny' and drive != 'mocny' and price == 'akceptowalna':
        # output_cut_levels[6] = ('slaby', (min([cpu_slaby_level, ram_slaby_level, ram_sredni_level, driv_slaby_level, driv_sredni_level, price_level], key=lambda x: x[1]))[1])
        output_cut_levels[6] = ('slaby', min(price_level[1], inference_norm(norm, [x[1] for x in
                                                                                            [cpu_slaby_level,
                                                                                             locals()['ram_'+ram+'_level'],
                                                                                             locals()['driv_'+drive+'_level']]])))
        active_rules.append(6)
    if cpu == 'slaby' and ram == 'mocny' and drive == 'mocny' and price == 'akceptowalna':
        # output_cut_levels[7] = ('sredni', (min([cpu_slaby_level, ram_mocny_level, driv_mocny_level, price_level], key=lambda x: x[1]))[1])
        output_cut_levels[7] = ('sredni', min(price_level[1], inference_norm(norm, [x[1] for x in
                                                                                             [cpu_slaby_level,
                                                                                              ram_mocny_level,
                                                                                              driv_mocny_level]])))
        active_rules.append(7)
    if cpu == 'bslaby' and price == 'akceptowalna':
        # output_cut_levels[8] = ('slaby', (min([cpu_bslaby_level, price_level], key=lambda x: x[1]))[1])
        output_cut_levels[8] = ('slaby', (min(filter(lambda x: x[1], [cpu_bslaby_level, price_level])))[1])
        active_rules.append(8)
    if cpu == 'mocny' and ram == 'slaby' and price == 'akceptowalna':
        # output_cut_levels[9] = ('sredni', (min([cpu_mocny_level, ram_slaby_level, price_level], key=lambda x: x[1]))[1])
        output_cut_levels[9] = ('sredni', min(price_level[1], inference_norm(norm, [x[1] for x in
                                                                                             [cpu_mocny_level,
                                                                                              ram_slaby_level]])))
        active_rules.append(9)
    if cpu == 'mocny' and ram != 'mocny' and drive == 'slaby' and price == 'akceptowalna':
        # output_cut_levels[10] = ('sredni', (min([cpu_mocny_level, ram_slaby_level, ram_sredni_level, driv_slaby_level, price_level], key=lambda x: x[1]))[1])
        output_cut_levels[10] = ('sredni', min(price_level[1], inference_norm(norm, [x[1] for x in
                                                                                              [cpu_mocny_level,
                                                                                               locals()['ram_'+ram+'_level'],
                                                                                               driv_slaby_level]])))
        active_rules.append(10)
    if cpu == 'mocny' and ram == 'mocny' and drive == 'slaby' and price == 'akceptowalna':
        # output_cut_levels[11] = ('mocny', (min([cpu_mocny_level, ram_mocny_level, driv_slaby_level, price_level], key=lambda x: x[1]))[1])
        output_cut_levels[11] = ('mocny', min(price_level[1], inference_norm(norm, [x[1] for x in
                                                                                             [cpu_mocny_level,
                                                                                              ram_mocny_level,
                                                                                              driv_slaby_level]])))
        active_rules.append(11)
    if cpu == 'sredni' and ram == 'mocny' and drive != 'mocny' and price == 'akceptowalna':
        # output_cut_levels[12] = ('sredni', (min([cpu_sredni_level, ram_slaby_level, ram_sredni_level, driv_slaby_level, driv_sredni_level, price_level], key=lambda x: x[1]))[1])
        output_cut_levels[12] = ('sredni', min(price_level[1], inference_norm(norm, [x[1] for x in
                                                                                              [cpu_sredni_level,
                                                                                               ram_mocny_level,
                                                                                               locals()['driv_'+drive+'_level']]])))
        active_rules.append(12)

    # CUT_OUTPUTS
    output_cuts = [[] for o in range(len(active_rules))]
    for cut in range(len(active_rules)):
        (out_var, level) = output_cut_levels[active_rules[cut]]
        output_cuts[cut] = [el if el < level else level for el in locals()['out_' + out_var]]

    # print(locals()['out_slaby'])
    # AGGREGATE_OUTPUTS
    out_aggregated = []
    if len(output_cuts) <= 0:
        raise Exception
    elif len(output_cuts) == 1:
        out_aggregated = output_cuts[0]
    else:
        out_aggregated = [0 for i in range(len(out_range))]
        for n in range(len(output_cuts) - 1):
            out_aggregated = np.fmax(np.fmax(output_cuts[n], output_cuts[n + 1]), out_aggregated)

    # DEFUZZIFY
    result_defuzz = fuzz.defuzzify.centroid(out_range, out_aggregated)
    result_defuzz2 = sum(x * y for (x, y) in zip(out_range, out_aggregated)) / sum(out_aggregated)  # Wynik nieco różny od defuzzify.centroid

    return result_defuzz

    # print(result_defuzz)
    # print(result_defuzz2)
    # 0 0 0 -1 1
    # 4 -1 -1 1 3
    # 3 3 3 1 3
    # 3 1 1 1 1
    # 3 2 0 1 2
    # 3 0 2 1 2
    # 2 -3 -3 1 1
    # 2 3 3 1 2
    # 1 0 0 1 1
    # 4 1 0 1 2
    # 4 -3 1 1 2
    # 4 3 1 1 3
    # 3 -3 -3 1 2


