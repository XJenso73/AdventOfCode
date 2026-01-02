import time

START_TIME = time.perf_counter()


def import_data(file_path: str) -> list[str]:
    print("_" * 50, "\n")
    with open(file_path) as f:
        data = [line.rstrip("\n") for line in f]
    print(f"Daten aus {file_path} importiert ...")
    print("-" * 50)
    return data


def calculate_duration():
    print("-" * 50)
    duration = time.perf_counter() - START_TIME
    print(f"Duration: {duration:.4f} second")
    print("_" * 50, "\n")
