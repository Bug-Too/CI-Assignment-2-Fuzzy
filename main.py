def water_boiler_simulation(initial_temperature: float, desire_temperature: int, time_second: int):
    actual_temperature = initial_temperature
    mass = 1
    c = 1

    for i in range(time_second):
        watt_sec = watt_controller(actual_temperature, desire_temperature)
        boiling_change_temperature = watt_sec * 0.1 / (mass * c)
        actual_temperature += boiling_change_temperature

        if actual_temperature > 100:
            actual_temperature = 100

        actual_temperature -= 0.001

        print('time:', i, 'temp:', actual_temperature)


def watt_controller(temperature: float, desire_temperature: int) -> float:
    desire_fuzzy_temperature = find_desire_fuzzy_temperature(desire_temperature)
    actual_fuzzy_temperature = fuzzify_temperature(temperature)
    watt = de_fuzzify(desire_fuzzy_temperature, actual_fuzzy_temperature)
    return watt


def find_desire_fuzzy_temperature(desire_temperature: int) -> list[float]:
    if desire_temperature == 0:
        return [1, 0, 0]
    elif desire_temperature == 1:
        return [0, 1, 0]
    elif desire_temperature == 2:
        return [0, 0, 1]


def fuzzify_temperature(temperature: float) -> list[float]:
    cold = 0
    warm = 0
    hot = 0

    if temperature < 25:
        cold = 1
    elif temperature < 50:
        cold = (50 - temperature) / 10
        warm = (temperature - 25) / 10
    elif temperature < 70:
        warm = 1
    elif temperature < 100:
        warm = (100 - temperature) / 10
        hot = (temperature - 70) / 10
    else:
        hot = 1

    return [cold, warm, hot]


def de_fuzzify(desire_fuzzy_temperature: list[float], actual_fuzzy_temperature: list[float]) -> float:
    # firing_strength_cold_cold = min(desire_fuzzy_temperature[0], actual_fuzzy_temperature[0])
    firing_strength_cold_warm = min(desire_fuzzy_temperature[1], actual_fuzzy_temperature[0])
    firing_strength_cold_hot = min(desire_fuzzy_temperature[2], actual_fuzzy_temperature[0])
    firing_strength_warm_warm = min(desire_fuzzy_temperature[1], actual_fuzzy_temperature[1])
    firing_strength_warm_hot = min(desire_fuzzy_temperature[2], actual_fuzzy_temperature[1])
    firing_strength_hot_hot = min(desire_fuzzy_temperature[2], actual_fuzzy_temperature[2])

    sum_firing_strength = firing_strength_cold_warm + firing_strength_cold_hot + firing_strength_warm_warm + firing_strength_warm_hot + firing_strength_hot_hot
    if sum_firing_strength == 0:
        return 0
    watt = (firing_strength_cold_warm * 0.5 + firing_strength_cold_hot * 0.75 + firing_strength_warm_warm * 0 + firing_strength_warm_hot * 0.5 + firing_strength_hot_hot * 0) / sum_firing_strength
    print('watt:', watt)
    return watt


if __name__ == '__main__':
    water_boiler_simulation(26, 1, 10000)
