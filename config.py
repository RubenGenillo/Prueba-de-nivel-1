import sys

DATABASE_PATH = "BaseDeDatos.csv"

if "pytest" in sys.argv[0]:
    DATABASE_PATH = "tests/BaseDeDatos.csv"
