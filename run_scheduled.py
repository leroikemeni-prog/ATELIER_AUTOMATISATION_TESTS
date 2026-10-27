import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tester.runner import run_all
from storage import save_run

if __name__ == "__main__":
    res = run_all()
    save_run(res)
    print(res["timestamp"], res["summary"])
