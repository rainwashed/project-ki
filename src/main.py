import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(project_root)

from server.server import run

if __name__ == "__main__":
    run()