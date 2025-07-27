from pathlib import Path
import re
from sys import argv
from statistics import fmean

COLUMNS = ["AccelX", "AccelY", "AccelZ", "GyroX", "GyroY", "GyroZ", "Temperature"]


def print_values(values: list[float]):
    for label, value in zip(COLUMNS, values):
        print(f"  {label}: {value:.3f}")


def print_ranges(data: list[list[float]]):
    for label, values in zip(COLUMNS, zip(*data)):
        range = max(values) - min(values)
        print(f"  {label}: {range:.3f} ({min(values):.3f} to {max(values):.3f})")


def print_averages_from_log(log_data: str):
    sensor_1_data: list[list[float]] = []
    sensor_2_data: list[list[float]] = []
    reading_index = -1
    previous_seconds = -1
    lines = log_data.split("\n")
    for line_index in range(len(lines)):
        line = lines[line_index]
        regex = r"\[..:..:(\d\d)]\[D]\[bmi160:243]: Got accel={x=([\-\.\d]+) m\/s², y=([\-\.\d]+) m\/s², z=([\-\.\d]+) m\/s²}, gyro={x=([\-\.\d]+) °\/s, y=([\-\.\d]+) °\/s, z=([\-\.\d]+) °\/s}. temp=([\-\.\d]+)°C"
        result = re.search(regex, line)
        if not result:
            continue
        reading_index += 1
        values = [float(value) for value in result.groups()]
        seconds = int(values.pop(0))
        # We assume every even reading is from sensor 1 and every odd reading is from sensor 2
        if reading_index % 2 == 0:
            if values[0] > 0:
                print(
                    f"Warning: Expected negative AccelX reading from sensor 1, got {values[0]}"
                )
                print(f"  {line}")
            sensor_1_data.append(values)
        else:
            if values[0] < 0:
                print(
                    f"Warning: Expected positive AccelX reading from sensor 2, got {values[0]}"
                )
                print(f"  {line}")
            sensor_2_data.append(values)

    sensor_1_averages = [fmean(values) for values in zip(*sensor_1_data)]
    sensor_2_averages = [fmean(values) for values in zip(*sensor_2_data)]

    print("Sensor 1 averages:")
    print_values(sensor_1_averages)
    print()
    print("Sensor 2 averages:")
    print_values(sensor_2_averages)

    print()
    print("Sensor 1 ranges:")
    print_ranges(sensor_1_data)
    print()
    print("Sensor 2 ranges:")
    print_ranges(sensor_2_data)


if __name__ == "__main__":
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <log_file>")
        exit(1)

    log_file = Path(argv[1])
    with open(log_file, "r") as file:
        log_data = file.read()
        print_averages_from_log(log_data)
