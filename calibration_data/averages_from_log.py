from pathlib import Path
import re
from sys import argv
from statistics import fmean


def print_average_values(averages: list[float]):
    labels = ["AccelX", "AccelY", "AccelZ", "GyroX", "GyroY", "GyroZ", "Temperature"]
    for label, value in zip(labels, averages):
        print(f"  {label}: {value:.3f}")


def print_averages_from_log(log_data: str):
    sensor_1_data: list[list[float]] = []
    sensor_2_data: list[list[float]] = []
    reading_index = -1
    previous_seconds = -1
    for line in log_data.splitlines():
        regex = r"\[..:..:(\d\d)]\[D]\[bmi160:243]: Got accel={x=([\-\.\d]+) m\/s², y=([\-\.\d]+) m\/s², z=([\-\.\d]+) m\/s²}, gyro={x=([\-\.\d]+) °\/s, y=([\-\.\d]+) °\/s, z=([\-\.\d]+) °\/s}. temp=([\-\.\d]+)°C"
        result = re.search(regex, line)
        if not result:
            continue
        reading_index += 1
        values = [float(value) for value in result.groups()]
        seconds = int(values.pop(0))
        if reading_index % 2 == 0:
            if previous_seconds == seconds:
                print(line)
                print(
                    f"Previous seconds={previous_seconds}, expected a change, got {seconds}"
                )
                raise ValueError(
                    f"Inconsistency in the data @{reading_index} (started at line printed above)"
                )
            previous_seconds = seconds
            sensor_1_data.append(values)
        else:
            if previous_seconds != seconds:
                print(line)
                print(
                    f"Previous seconds={previous_seconds}, expected the same, got {seconds}"
                )
                raise ValueError(
                    f"Inconsistency in the data @{reading_index} (started at line printed above)"
                )
            sensor_2_data.append(values)

    sensor_1_averages = [fmean(values) for values in zip(*sensor_1_data)]
    sensor_2_averages = [fmean(values) for values in zip(*sensor_2_data)]

    print("Sensor 1 averages:")
    print_average_values(sensor_1_averages)
    print()
    print("Sensor 2 averages:")
    print_average_values(sensor_2_averages)


if __name__ == "__main__":
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <log_file>")
        exit(1)

    log_file = Path(argv[1])
    with open(log_file, "r") as file:
        log_data = file.read()
        print_averages_from_log(log_data)
