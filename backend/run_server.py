import os

import sys

os.chdir(r"C:\Users\G Harsha Vardhan\OneDrive\Desktop\Delloite\Smart-Banking-System\backend")
sys.path.insert(0, os.getcwd())

from main import app  # noqa: E402

import uvicorn


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
