import os
from dataclasses import dataclass
from typing import Final, Iterator


SAVE_DIR_NAME: Final[str] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


@dataclass(frozen=True)
class DatasetNames:
    alkox: str = "alkox"
    benzylation: str = "benzylation"
    colors_bob: str = "colors_bob"
    colors_n9: str = "colors_n9"
    fullerenes: str = "fullerenes"
    hplc: str = "hplc"
    photo_pce10: str = "photo_pce10"
    photo_wf3: str = "photo_wf3"
    snar: str = "snar"
    suzuki: str = "suzuki"

    def __getitem__(self, index: int) -> str:
        return str(list(self.__dict__.values())[index])

    def __iter__(self) -> Iterator:
        return (name for name in self.__dict__.values())

    def __len__(self) -> int:
        return len(self.__dict__.values())


DATASET_NAMES = DatasetNames()
