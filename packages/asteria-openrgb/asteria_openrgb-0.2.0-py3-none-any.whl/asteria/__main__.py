import argparse
import logging
import signal
from threading import Event

from .driver import OpenRgbDriver


def main():
    parser = argparse.ArgumentParser(
        description="Asteria - a framework for driving an OpenRGB server",
    )
    parser.add_argument("config")
    parser.add_argument("--address", default="localhost")
    parser.add_argument("--port", default=6742)
    args = parser.parse_args()

    # TODO: make configurable
    logging.basicConfig(level=logging.INFO)

    # Set up the signal handler used to inform the driver when it's time to stop.
    finished = Event()

    def handle_sigint(signum, frame):
        signame = signal.Signals(signum).name
        logging.info(f"Handling signal {signame} (numeric value: {signum})")
        finished.set()

    signal.signal(signal.SIGINT, handle_sigint)

    driver = OpenRgbDriver(args.config, args.address, args.port, finished)
    driver.run()


if __name__ == "__main__":
    main()
