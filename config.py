from argparse import ArgumentParser
from dataclasses import dataclass
from os import environ


@dataclass
class Config:
    log: bool
    delay: float
    path: str


def load_config() -> Config:
    parser = ArgumentParser()
    parser.add_argument("-nl", "--nolog", action="store_true", help="disable logs")
    parser.add_argument("-d", "--delay", type=float, default=0, help="response delay (s)")
    parser.add_argument("-p", "--path", type=str, default="photos", help="path to catalog with file archives")

    args = parser.parse_args()
    args.path = args.path.strip("/")
    config = Config(not args.nolog, args.delay, args.path)

    return config
