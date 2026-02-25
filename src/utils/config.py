import os
import re

# Load .env if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env'))
except ImportError:
    pass

# Central config definitions 

# Project Base Paths
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(SRC_DIR)

MEMBER_RESULTS_DIR = os.path.join(PROJECT_ROOT, "member_results")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
RESOURCES_DIR = os.path.join(PROJECT_ROOT, "resources")
REPORTS_DIR = os.path.join(RESOURCES_DIR, "tournaments-reports")
NOTEBOOKLM_LOG_DIR = os.path.join(RESOURCES_DIR, "notebooklm-log")

# Competition Rules
RUN_MIN_DISTANCE = 1.0   # km — minimum for running activities
WALK_MIN_DISTANCE = 2.0  # km — minimum for walking activities
TEAM_SIZE = 10            # members per team

# Renaming logic regex pattern
RENAMED_PATTERN = re.compile(
    r'^([a-z]+)-(\d{4})-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)-(\d{2})(_\d+)?\.(jpg|jpeg|png)$',
    re.IGNORECASE
)

# Local Ollama LLM Config
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:8b")
OLLAMA_TEMPERATURE = float(os.environ.get("OLLAMA_TEMPERATURE", "0.7"))
OLLAMA_TOP_K = int(os.environ.get("OLLAMA_TOP_K", "40"))
OLLAMA_TOP_P = float(os.environ.get("OLLAMA_TOP_P", "0.9"))

# Agent-specific Ollama presets (override defaults per use case)
OLLAMA_PRESETS = {
    "precise":  {"temperature": 0.1, "top_k": 10, "top_p": 0.5},   # Coach: validation, parsing
    "balanced": {"temperature": 0.5, "top_k": 40, "top_p": 0.8},   # Running Coach: advice
    "creative": {"temperature": 0.7, "top_k": 40, "top_p": 0.9},   # Sports Analyst: content
    "fun":      {"temperature": 0.9, "top_k": 50, "top_p": 0.95},  # Reporter: motivation
}

# Google Drive Config
GOOGLE_DRIVE_FOLDER_ID = os.environ.get("GOOGLE_DRIVE_FOLDER_ID", "1FHh4VKxjO2zJF6Bx42UZgxv80cmpsEdG")

# Team Participants
TEAMS = {
    'Mandalorian': ['GIO', 'Boat', 'TORO', 'Toro', 'EM', 'Em', 'SAND', 'Sand', 'peck', 'Neung', 'fuse', 'Fuse', 'Chan', 'Mos'],
    'IT System': ['Oat', 'Game', 'O', 'Palm', 'Oum', 'Jojo', 'Tae', 'Boy', 'Ton', 'PAN']
}

def determine_team(name):
    """Maps a runner's name to their respective team name."""
    name_lower = name.lower()
    
    if name_lower in [n.lower() for n in TEAMS['Mandalorian']]: return 'Mandalorian'
    if name_lower in [n.lower() for n in TEAMS['IT System']]: return 'IT System'
    
    return 'Unknown'
