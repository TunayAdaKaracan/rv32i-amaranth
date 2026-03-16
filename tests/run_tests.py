import os, shutil
from tests.test_alu import get_alu_tests

TEST_RESULTS_DIR = "test_results"

def create_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)

def run_tests(type: str, clear: bool = False):
    if clear:
        shutil.rmtree(TEST_RESULTS_DIR)
        os.mkdir(TEST_RESULTS_DIR)

    to_run = []
    if type == None:
        to_run.append(get_alu_tests)
    elif type == "alu":
        to_run.append(get_alu_tests)
    
    for information in to_run:
        info = information()
        create_if_not_exists(os.path.join(TEST_RESULTS_DIR, info["results_dir"]))
        info["test_function"]()