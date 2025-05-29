import configparser
import pathlib

# path = pathlib.Path(__file__).parent.joinpath("config.ini")
path = pathlib.Path(__file__).parent / "config.ini"
parser = configparser.ConfigParser()
parser.read(path)

DB_NAME = parser.get("DB", "DB_NAME")
