import json
from pathlib import Path


class SchedulerStorage:
    def __init__(self) -> None:
        self.reviews_path = Path(__file__).parent / "reviews.json"

    def set_pdp_storage(self, data: list) -> None:
        if self.reviews_path.exists():
            with open(self.reviews_path, "r", encoding="utf-8") as f:
                storage = json.load(f)
        else:
            storage = []

        storage.extend(data)

        with open(self.reviews_path, "w", encoding="utf-8") as f:
            json.dump(storage, f, indent=2, ensure_ascii=False)
