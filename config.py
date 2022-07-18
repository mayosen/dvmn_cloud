from argparse import ArgumentParser
from dataclasses import dataclass
from os import environ


@dataclass
class Config:
    nolog: bool
    delay: float
    path: str


def parse_env() -> tuple:
    return environ.get("NOLOG"), environ.get("DELAY"), environ.get("PATH")


def load_config() -> Config:
    parser = ArgumentParser()
    parser.add_argument("-nl", "--nolog", action="store_true", help="disable logs")
    parser.add_argument("-d", "--delay", type=float, default=0, help="response delay (s)")
    parser.add_argument("-p", "--path", type=str, default="photos/", help="path to catalog with file archives")

    args = parser.parse_args()
    config = Config(args.nolog, args.delay, args.path)

    return config

