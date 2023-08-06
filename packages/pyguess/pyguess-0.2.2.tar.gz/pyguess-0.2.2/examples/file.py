import csv

import tqdm

import pyguess
from pyguess import Config

config = Config(
    path_to_streets="../../misc/data/streets_data",
)
DELIMITER = "\t"
HEADER = ["orig_street", "orig_location", "guessed_street", "guessed_location"]

with open("../../misc/data_examples/examples.csv") as file_in:
    reader = csv.reader(file_in, delimiter=DELIMITER)
    next(reader)
    with open(
        "../../misc/data_examples/guessed_examples.csv",
        "w",
    ) as file_out:
        writer = csv.writer(file_out, delimiter=DELIMITER)
        writer.writerow(HEADER)
        for row in tqdm.tqdm(reader):
            street = row[0]
            place = row[1]
            candidate = pyguess.guess_address(street, place, config)
            guessed_street, guessed_location = None, None
            if candidate is not None:
                guessed_street, guessed_location = (
                    candidate.street,
                    candidate.location,
                )
            writer.writerow([street, place, guessed_street, guessed_location])
