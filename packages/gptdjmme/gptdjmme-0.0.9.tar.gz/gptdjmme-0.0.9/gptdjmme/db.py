from dataclasses import dataclass
from pathlib import Path

# This class represents a simple database that stores its data as files in a directory.
class DB:
    """A simple key-value store, where keys are filenames and values are file contents."""

    def __init__(self, path):
        self.path = Path(path).absolute()

        self.path.mkdir(parents=True, exist_ok=True)

        # create memory/memory file if it doesnt exist:
        if not Path("dbs/memory/memory").is_file():
            Path("dbs/memory/memory").touch()


    def __getitem__(self, key):
        full_path = self.path / key

        if not full_path.is_file():
            raise KeyError(key)
        with full_path.open("r", encoding="utf-8") as f:
            return f.read()

    # get all key-value pairs from the database and return them as a dict.
    def get_all(self):
        return {f.name: f.read_text() for f in self.path.iterdir() if f.is_file()}

    def __setitem__(self, key, val):
        full_path = self.path / key
        full_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(val, str):
            # if it doesnt exist, create it
            if not full_path.is_file():
                full_path.touch()
            full_path.write_text(val, encoding="utf-8")
        else:
            # If val is neither a string nor bytes, raise an error.
            raise TypeError("val must be either a str or bytes")

    def __delitem__(self, key):
        full_path = self.path / key

        if not full_path.is_file():
            raise KeyError(key)
        full_path.unlink()


# dataclass for all dbs:
@dataclass
class DBs:
    memory: DB
    identity: DB