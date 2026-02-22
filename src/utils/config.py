import os
import re

# Central config definitions 

# Project Base Paths
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(SRC_DIR)

MEMBER_RESULTS_DIR = os.path.join(PROJECT_ROOT, "member_results")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")

# Competition Rules
RUN_MIN_DISTANCE = 1.0   # km — minimum for running activities
WALK_MIN_DISTANCE = 2.0  # km — minimum for walking activities
TEAM_SIZE = 10            # members per team

# Renaming logic regex pattern
RENAMED_PATTERN = re.compile(
    r'^([a-z]+)-(\d{4})-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)-(\d{2})(_\d+)?\.(jpg|jpeg|png)$',
    re.IGNORECASE
)

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
