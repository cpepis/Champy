# Champy/stats.py

import os
import math
import pandas as pd


def group_by(main_df, string):
    """
    Groups the DataFrame by the specified string and calculates the Geometric Mean.
    """
    df = main_df[
        main_df["Benchmark"].str.contains(f"champsim-{string}$", regex=True)
    ].reset_index(drop=True)
    df["Benchmark"] = df["Benchmark"].str.replace(f"-champsim-{string}", "")

    # Calculate Geometric Mean
    try:
        geomean = math.prod(df["IPC"]) ** (1 / len(df["IPC"]))
        geomean_df = pd.DataFrame([{"Benchmark": "Geomean", "IPC": geomean}])
        df = pd.concat([df, geomean_df], ignore_index=True)
    except ZeroDivisionError:
        print(f"Some IPC values are zero in {string} data, exiting...")
        exit(1)

    return df


def calculate_speedup(df, baseline_df):
    """
    Calculates the speedup of the given DataFrame with respect to the baseline DataFrame.
    """
    df["Speedup"] = ((df["IPC"] / baseline_df["IPC"]) - 1) * 100
    return df


def read_ipc(data_dir):
    """
    Reads the IPC from all files in the given directory and returns a DataFrame.
    """
    data = []  # List to store (benchmark, IPC) tuples
    for file in os.listdir(data_dir):
        if file.endswith(".txt"):

            if os.path.getsize(os.path.join(data_dir, file)) == 0:
                print(f"File {file} is empty, directory: {data_dir}, skipping...")
                continue

            found_ipc = False
            with open(os.path.join(data_dir, file), "r") as f:
                for line in f:
                    if "CPU 0 cumulative IPC:" in line:
                        found_ipc = True
                        try:
                            # Extract the IPC value
                            ipc_value = float(line.split("CPU 0 cumulative IPC:")[1].split()[0])
                            # Append to list
                            data.append((file.split(".txt")[0], ipc_value))
                        except (IndexError, ValueError):
                            print(f"Couldn't extract IPC value from line: {line}")

            if not found_ipc:
                print(f"IPC value not found in file: {file} in directory: {data_dir}")

    # Create DataFrame from the data
    df = pd.DataFrame(data, columns=["Benchmark", "IPC"])

    # Sort the DataFrame by Benchmark name
    df = df.sort_values(by=["Benchmark"])
    df = df.reset_index(drop=True)

    return df


def read_stat(data_dir, stat):
    """
    Reads the stats from all files in the given directory and returns a DataFrame.
    """
    data = []  # List to store (benchmark, stat) tuples
    for file in os.listdir(data_dir):
        if file.endswith(".txt"):

            if os.path.getsize(os.path.join(data_dir, file)) == 0:
                print(f"File {file} is empty, directory: {data_dir}, skipping...")
                continue

            found_stat = False
            with open(os.path.join(data_dir, file), "r") as f:
                for line in f:
                    if stat in line:
                        found_stat = True
                        try:
                            # Extract the stat value
                            stat_value = float(line.split(stat)[1])
                            # Append to list
                            data.append((file.split(".txt")[0], stat_value))
                        except (IndexError, ValueError):
                            print(f"Couldn't extract {stat} value from line: {line}")

            if not found_stat:
                print(f"{stat} value not found in file: {file} in directory: {data_dir}")

    # Create DataFrame from the data
    df = pd.DataFrame(data, columns=["Benchmark", stat])

    # Sort the DataFrame by Benchmark name
    df = df.sort_values(by=["Benchmark"])
    df = df.reset_index(drop=True)

    return df