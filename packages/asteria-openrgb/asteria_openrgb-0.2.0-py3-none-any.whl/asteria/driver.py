from . import instruments, metrics, scales
import logging
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor
import tomli
import time


MIN_SLEEP_MS = 100  # Always sleep at least this long between iterations
QUANTUM_MS = 500  # TODO: move into driver (with safety assertion)?
# Displayed if an instrument encounters an unhandled exception
ERROR_COLOUR = RGBColor.fromHEX("#FF0000")


class OpenRgbDriver:
    def __init__(
        self, config, address, port, termination_event, shut_off_on_disconnect=True
    ):
        self.address = address
        self.port = port
        self.client = OpenRGBClient(self.address, self.port, "asteria")
        self.finished = termination_event
        self.shut_off_on_disconnect = shut_off_on_disconnect
        with open(config, "rb") as f:
            self.config = tomli.load(f)
        self.zone_mapping = {}

        for device_name in self.config.keys():
            matching_devices = self.client.get_devices_by_name(device_name)
            num_matching_devices = len(matching_devices)
            if num_matching_devices != 1:
                raise RuntimeError(
                    f"Expected to find one matching device for '{device_name}', but found {num_matching_devices}; those devices are: {matching_devices}"
                )

            device = matching_devices[0]

            for zone_name in self.config[device_name].keys():
                matching_zones = [x for x in device.zones if x.name == zone_name]

                if not matching_zones:
                    raise RuntimeError(
                        f"Found no zones that match '{zone_name}' (for device {device_name})"
                    )

                # Helper to add context to error messages
                def add_context(s):
                    return f"{s} (for device '{device_name}', zone '{zone_name}')"

                for effect in self.config[device_name][zone_name]:
                    try:
                        metric = self.parse_metric(effect)
                    except RuntimeError as e:
                        raise RuntimeError(add_context(f"{e}"))

                    try:
                        scale = self.parse_scale(effect)
                    except RuntimeError as e:
                        raise RuntimeError(add_context(f"{e}"))

                    # A scale is always optional, but a scale without a metric doesn't make sense
                    if scale is not None and metric is None:
                        raise RuntimeError(
                            add_context(
                                f"Section 'scale' detected without an accompanying 'metric' section, which is required"
                            )
                        )

                    if scale and metric:
                        metric = scale(metric)

                    try:
                        instrument = self.parse_instrument(effect, metric)
                    except RuntimeError as e:
                        raise RuntimeError(add_context(f"{e}"))

                    for zone in matching_zones:
                        if zone in self.zone_mapping:
                            self.zone_mapping[zone].append(instrument)
                        else:
                            self.zone_mapping[zone] = [instrument]

        logging.info(f"Successfully configured {len(self.zone_mapping)} zone(s).")
        for zone, configured_instruments in self.zone_mapping.items():
            logging.info(
                f"Instruments registered for zone {zone}: {configured_instruments}"
            )

    def parse_metric(self, config):
        metric_config = config.get("metric")
        if not metric_config:
            return None

        try:
            # For now, functions need to be pre-defined in asteria.metrics
            # (purely for ease of implementation); ideally, users should be
            # able to bring their own functions
            metric_type = getattr(metrics, metric_config["type"])
        except KeyError:
            raise RuntimeError(
                f"Parameter 'type' is required for the 'metric' section, but is missing"
            )
        except AttributeError:
            raise RuntimeError(f"No metric named {metric_config['type']} found")
        metric_args = metric_config.get("args", {})
        # Partially apply any user-provided arguments, but remember that
        # `metric` needs to be a function for the instrument to periodically
        # call later (i.e., don't _evaluate_ metric now and call it a day)
        return lambda: metric_type(**metric_args)

    def parse_scale(self, config):
        scale_config = config.get("scale")
        if not scale_config:
            return None

        try:
            scale_type = getattr(scales, scale_config["type"])
        except KeyError:
            raise RuntimeError(
                f"Parameter 'type' is required for the 'scale' section, but is missing"
            )
        except AttributeError:
            raise RuntimeError(f"No scale named {scale_config['type']} found")
        scale_args = scale_config.get("args", {})
        return lambda metric: scale_type(metric, **scale_args)

    def parse_instrument(self, config, metric):
        try:
            instrument_type = getattr(instruments, config["instrument"]["type"])
            instrument_args = config["instrument"].get("args", {})

            if metric:
                instrument_args["metric_function"] = metric
        except KeyError:
            raise RuntimeError(f"Section 'instrument' is required, but is missing")
        except AttributeError:
            raise RuntimeError(
                f"No instrument named {config['instrument']['type']} found"
            )

        return instrument_type(**instrument_args)

    def tick(self):
        for zone, instruments in self.zone_mapping.items():
            zone_len = len(zone.leds)
            colours = []
            num_leds = zone_len // len(instruments)
            num_leftover_leds = zone_len % len(instruments)
            for i, instrument in enumerate(instruments):
                # Assign one extra "leftover" LED to each instrument until we run out
                num_instrument_leds = num_leds + (1 if i < num_leftover_leds else 0)
                try:
                    output = instrument.display(num_instrument_leds)
                except Exception as e:
                    logging.warn(
                        f"Observed exception when running instrument '{instrument}': {e}"
                    )
                    output = [ERROR_COLOUR] * num_instrument_leds
                colours.extend(output)

            assert zone_len == len(colours)
            zone.set_colors(colours)

    def run(self):
        while not self.finished.is_set():
            start = time.monotonic()  # measured in seconds
            quantum_end = start + QUANTUM_MS / 1000
            self.tick()
            time.sleep(max(quantum_end - time.monotonic(), MIN_SLEEP_MS / 1000))

        logging.info("Exited OpenRgbDriver's run() loop")
        if self.shut_off_on_disconnect:
            self.client.clear()
        self.client.disconnect()
        logging.info("Successfully disconnected from OpenRGB server")
