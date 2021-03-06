from argparse import ArgumentParser
from dataclasses import dataclass


@dataclass
class Config:
    disable_logs: bool
    delay: float
    path: str


def load_config() -> Config:
    parser = ArgumentParser()
    parser.add_argument("-dl", "--disablelogs", action="store_true", help="disable logs")
    parser.add_argument("-d", "--delay", type=float, default=0, help="response delay (s)")
    parser.add_argument("-p", "--path", type=str, default="photos", help="path to root folder of archives")

    args = parser.parse_args()
    args.path = args.path.strip("/")
    config = Config(args.disablelogs, args.delay, args.path)

    return config
