import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ["OLLAMA_BASE_URL"] = "http://test-ollama:11434"
os.environ["MAX_CHUNK_SIZE"] = "2000"
os.environ["CHUNK_OVERLAP"] = "200"
