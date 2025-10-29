import csv
from pathlib import Path
from src.utils.logging_config import setup_logger
from typing import Optional

logger = setup_logger(__name__)


class CachedItemEntry:
    def __init__(self, content: str, is_pineapple: bool):
        self.content = content
        self.is_pineapple = is_pineapple


class CSVItemCacher:
    def __init__(self, csv_file: Path, delimiter: str = ","):
        self.csv_file = csv_file
        self.delimiter = delimiter
        self.data = self._load_data()

    def _load_data(self):
        """Loads data from the CSV file into a list."""
        data = []
        try:
            with open(self.csv_file, "r", newline="") as file:
                reader = csv.DictReader(file, delimiter=self.delimiter)
                for row in reader:
                    content = row["content"]
                    is_pineapple = row["is_pineapple"].lower() == "true"

                    data.append(CachedItemEntry(content, is_pineapple))
        except FileNotFoundError:
            logger.info(f"File not found: {self.csv_file}. Creating new one.")
            data = []
        except KeyError as e:
            logger.error(f"csv file is missing required column {e}")
            data = []
        except Exception as e:
            logger.error(f"Error loading data from csv: {e}")
            data = []
        return data

    def get(self, content: str) -> Optional[CachedItemEntry]:
        """Retrieves the is_pineapple value for the given content."""
        for entry in self.data:
            if entry.content == content:
                return entry
        return None

    def set(self, content: str, is_pineapple: bool):
        """Sets the is_pineapple value for the given content and writes to CSV."""
        for entry in self.data:
            if entry.content == content:
                entry.is_pineapple = is_pineapple
                self._save_data()
                return
        self.data.append(CachedItemEntry(content, is_pineapple))
        self._save_data()

    def _save_data(self):
        """Saves the data to the CSV file."""
        try:
            with open(self.csv_file, "w", newline="") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=["content", "is_pineapple"],
                    delimiter=self.delimiter,
                )
                writer.writeheader()
                for entry in self.data:
                    writer.writerow(
                        {"content": entry.content, "is_pineapple": entry.is_pineapple}
                    )
        except Exception as e:
            logger.error(f"Error saving data to CSV: {e}")


if __name__ == "__main__":
    # Example usage:
    cacher = CSVItemCacher(Path("my_data.csv"))

    # Get a value
    is_pineapple = cacher.get("apple")
    print(f"Is 'apple' pineapple? {is_pineapple}")

    # Set a value
    cacher.set("banana", True)
    print("Set 'banana' to pineapple.")

    # Get the updated value
    is_pineapple = cacher.get("banana")
    print(f"Is 'banana' pineapple? {is_pineapple}")
