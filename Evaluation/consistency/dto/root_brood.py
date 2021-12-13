import os
import pickle
from dto.sample import *

BROOD_FOLDER = "data/root_broods/exploring"


class RootBrood:
    def __init__(self, root: Sample):
        self.root = root
        self.ref = None
        self.contains = []

    def fill_ref(self, file_path: str, left_p: float = 0, right_p: float = 0):
        ref_for_tm = create_random_sample_by_root(self.root, file_path, left_proba=left_p, right_proba=right_p)
        self.ref = ref_for_tm

    def fill_contains(self, file_path: str, size: int, left_p: float = 0, right_p: float = 0):
        for _ in range(size):
            containing_sample = create_random_sample_by_root(self.root, file_path, left_proba=left_p, right_proba=right_p)
            self.contains.append(containing_sample)

    def serialize(self):
        file_path = os.path.join(BROOD_FOLDER, f"{self.root.id}.csv")
        pickle.dump(file_path)

    def deserialize(self):
        file_path = os.path.join(BROOD_FOLDER, f"{self.root.id}.csv")
        new_brood = pickle.load(file_path)
        self.root = new_brood.root
        self.ref = new_brood.ref
        self.contains = new_brood.contains


def create_random_root_blood(size: int, file_path_for_tm: str, file_path_for_test: str, l_tm: float, r_tm: float, l_test: float, r_test: float) -> RootBrood:
    root = create_random_root_sample(ROOT_FILE)
    root_brood = RootBrood(root)
    root_brood.fill_ref(file_path_for_tm, left_p=l_tm, right_p=r_tm)
    root_brood.fill_contains(file_path_for_test, size, left_p=l_test, right_p=r_test)
    return root_brood
