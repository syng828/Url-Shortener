import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--database_file",
        help="Database file name",
        required=True,
        type=str)
    parser.add_argument(
        "--host",
        help="Host for the server",
        default="localhost",
        type=str)
    parser.add_argument(
        "--port",
        help="Port for the server",
        default=5000,
        type=int)
    print(parser.parse_args())


if __name__ == "__main__":
    get_args()
