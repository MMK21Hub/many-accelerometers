from csv import DictReader
from pathlib import Path


def print_averages_from_file(file_name: Path):
    with open(file_name) as file:
        reader = DictReader(file)
        data = [row for row in reader]

    averages = {
        key: sum(float(row[key]) for row in data) / len(data) for key in data[0]
    }
    for key, value in averages.items():
        print(f"{key.strip()}: {value:.3f}")


if __name__ == "__main__":
    print("Averages for sensor 1:")
    print_averages_from_file(Path(__file__).with_name("sensor_1.csv"))
    print()
    print("Averages for sensor 2:")
    print_averages_from_file(Path(__file__).with_name("sensor_2.csv"))
