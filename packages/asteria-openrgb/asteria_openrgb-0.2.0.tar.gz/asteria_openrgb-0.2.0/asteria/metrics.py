from functools import reduce
import json
import subprocess


def get_all_sensors():
    # -j flag: return output as JSON
    sensors = subprocess.run(["sensors", "-j"], capture_output=True, check=True)
    return json.loads(sensors.stdout)


def get_sensor(keys: list[str]):
    """Run the `sensors` command and return the value identified by `keys`."""
    all_sensors = get_all_sensors()
    return reduce(lambda d, k: d[k], keys, all_sensors)


def used_memory_percent():
    cmd = subprocess.run(
        "free | awk '/Mem/ { print ($3 / $2) }'",
        shell=True,
        capture_output=True,
        check=True,
    )
    return float(cmd.stdout)
