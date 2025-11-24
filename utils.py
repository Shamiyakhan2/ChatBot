import yaml
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
KB_DIR = DATA_DIR / "knowledge"

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")


def load_rules():
    return [
        "Eat more fruits and vegetables.",
        "Drink at least 8 glasses of water a day.",
        "Avoid too much sugar and junk food."
    ]