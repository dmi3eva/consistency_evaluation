import os

current_path = os.path.abspath(os.path.join(os.curdir, '..', '..'))
TM_TRASH_FILE = os.path.join(current_path, 'Evaluation', 'consistency', 'data', 'trash_source', 'ltc_ref.csv')
TEST_TRASH_FILE = os.path.join(current_path, 'Evaluation', 'consistency', 'data', 'trash_source', 'ltc_source.csv')
ROOT_FILE = os.path.join(current_path, 'Evaluation', 'consistency', 'data', 'root_source', 'un_root.csv')
ROOT_FAMILY_AMOUNT = 10