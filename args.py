import argparse
import time


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "database_file", help="Database file name (Required)")
    parser.add_argument(
        "--host", help="Host for the server", default="localhost")
    parser.add_argument("--port", help="Port for the server",
                        default=5000, type=int)
    return parser.parse_args()


if __name__ == "__main__":
    get_args()
