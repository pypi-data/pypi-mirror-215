import glob
import json
import os
import typing

from dare_datasets.dataset_abc import Dataset
from dare_datasets.processing.qr2t_benchmark.qr2t_to_totto import to_totto
from dare_datasets.processing.qr2t_benchmark.totto_to_concise_input import \
    to_compact
from dare_datasets.utils.downloader import get_file_from_gdrive, requires_files

GDRIVE_URL = "https://drive.google.com/drive/folders/1LCD4gObeX-PBxkNYNuZxSmrTBvzEK095?usp=sharing"
DATASET_NAME = "QR2T_Benchmark"


class QR2TBenchmark(Dataset):
    def __init__(self, cache_dir: typing.Optional[str] = None) -> None:
        super().__init__(DATASET_NAME, cache_dir)

    def get_info(self) -> dict[str, str]:
        """
        Returns a dictionary containing information about the dataset.
        """
        return {
            "name": "QR2T Benchmark",
            "description": "QR2T Benchmark is an extension of the Spider dataset for the QR2T task.",
            "url": GDRIVE_URL,
            "original_url": "-",
            "formats": ["json"],
            "dataset_folder": self.dataset_folder if self.data is not None else "NOT_YET_LOADED"
        }

    def _init_data(self):
        get_file_from_gdrive(url=GDRIVE_URL, cache_dir=self.cache_dir, folder_name=DATASET_NAME)

        self.data = {}
        for file in glob.glob(self.dataset_folder + "*"):
            self.data[os.path.basename(file).split('.')[0]] = json.load(open(file))

    @requires_files
    def get_raw(self):
        """
        Returns a dictionary containing `train`, `dev`, and `eval` splits.
        Each datapoint is a separate dictionary with the following keys:


        ```
        {
            "table_id": "staff",
            "query": "SELECT last_name, email_address FROM staff WHERE email_address LIKE '%wrau%'",
            "table_name": "staff",
            "query_description": "Find the last name of the staff whose email address contains \"wrau\".",
            "results_description": [
                "The staff member whose last name is Erdman has the following email: wrau@example.com",
                "The staff with last name Erdman has the email address wrau@example.com.",
                "The last name is Erdman and the email address is wrau@example.com"
            ],
            "result": ",last_name,email_address\\n0,Erdman,wrau@example.com\\n",
            "difficulty": "small_select"
        }
        ```
        """
        return self.data

    @requires_files
    def get(self):
        """
        Returns a dictionary containing `train`, `dev`, and `eval` splits.
        Each datapoint is a dictionary containing the serialized input of the query results and the verbalisations.

        !!! warning "Train vs. Dev and Evaluation splits"

            The `train` split contains a single verbalisation (`string`) per datapoint while the `dev` and `eval` splits
            contain a list of possible verbalisations (`list[string]`) per datapoint as shown below.

        ```
        {
            'subtable_and_metadata': '<query> club_rank <table> club_rank <col0> Total | NUMERIC | 6 <col1> count of club_rank | NUMERIC | 2 ',
            'final_sentence': ['Two clubs have six medals.', 'There are 2 clubs with 6 medals', 'There are 2 clubs with 6 total medals.']}
        }
        ```
        """
        return {key: to_compact(to_totto(data)) for key, data in self.data.items()}
