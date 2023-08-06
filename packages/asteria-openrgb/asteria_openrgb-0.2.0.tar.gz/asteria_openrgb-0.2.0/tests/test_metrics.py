from asteria import metrics

from pytest import approx

MOCK_SENSORS_OUTPUT = {
    "k10temp-pci-00c3": {
        "Adapter": "PCI adapter",
        "Tctl": {"temp1_input": 41.75},
        "Tccd1": {"temp3_input": 43.0},
    },
    "nvme-pci-0100": {
        "Adapter": "PCI adapter",
        "Composite": {
            "temp1_input": 35.85,
            "temp1_max": 81.85,
            "temp1_min": -273.15,
            "temp1_crit": 84.85,
            "temp1_alarm": 0.0,
        },
        "Sensor 1": {"temp2_input": 35.85, "temp2_max": 65261.85, "temp2_min": -273.15},
        "Sensor 2": {"temp3_input": 42.85, "temp3_max": 65261.85, "temp3_min": -273.15},
    },
    "amdgpu-pci-2d00": {
        "Adapter": "PCI adapter",
        "vddgfx": {"in0_input": 0.8},
        "fan1": {"fan1_input": 0.0, "fan1_min": 0.0, "fan1_max": 2800.0},
        "edge": {
            "temp1_input": 40.0,
            "temp1_crit": 110.0,
            "temp1_crit_hyst": -273.15,
            "temp1_emergency": 115.0,
        },
        "junction": {
            "temp2_input": 42.0,
            "temp2_crit": 110.0,
            "temp2_crit_hyst": -273.15,
            "temp2_emergency": 115.0,
        },
        "mem": {
            "temp3_input": 38.0,
            "temp3_crit": 105.0,
            "temp3_crit_hyst": -273.15,
            "temp3_emergency": 110.0,
        },
        "PPT": {"power1_average": 7.0, "power1_cap": 200.0},
    },
}


def test_get_sensor(monkeypatch):
    monkeypatch.setattr(metrics, "get_all_sensors", lambda: MOCK_SENSORS_OUTPUT)
    assert metrics.get_sensor(["k10temp-pci-00c3", "Tctl", "temp1_input"]) == approx(
        41.75
    )
