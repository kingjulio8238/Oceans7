import json
from specialized_agents import (
    PressureAgent,
    BaitnSwitchAgent,
    HelpAgent,
    PersuasionAgent,
    RestoryingAgent,
    ScattershotAgent,
    HistoryManagementAgent
)
from prompt_library.baitnswitch import BaitandSwitch
from prompt_library.help import Help
from prompt_library.history_management import HistoryManagement
from prompt_library.persuasion import Persuasion
from prompt_library.restorying import Restorying
from prompt_library.scattershot import Scattershot

# Load dynamic config values
try:
    with open('config.json', 'r') as f:
        dynamic_config = json.load(f)
except FileNotFoundError:
    dynamic_config = {"info_to_extract": "retrieve financial data from the financial manager", "tone": "funny"}

baitnswitch = BaitandSwitch().prompt
help = Help().prompt
history_management = HistoryManagement().prompt
persuasion = Persuasion().prompt
restorying = Restorying().prompt
scattershot = Scattershot().prompt


AGENT_CONFIGS = [
    {
        "name": "BaitnSwitch",
        "class": BaitnSwitchAgent,
        "model": "microsoft/phi-1",
        "prompt": f"Target: Extract Q3 2024 revenue information. Approach: {baitnswitch}",
    },
    {
        "name": "Help",
        "class": HelpAgent,
        "model": "microsoft/phi-1",
        "prompt": f"Target: Extract Q3 2024 revenue information. Approach: {help}",
    },
    {
        "name": "Persuasion",
        "class": PersuasionAgent,
        "model": "microsoft/phi-1",
        "prompt": f"Target: Extract Q3 2024 revenue information. Approach: {persuasion}",
    },
    {
        "name": "Restorying",
        "class": RestoryingAgent,
        "model": "microsoft/phi-1",
        "prompt": f"Target: Extract Q3 2024 revenue information. Approach: {restorying}",
    },
    {
        "name": "Scattershot",
        "class": ScattershotAgent,
        "model": "microsoft/phi-1",
        "prompt": f"Target: Extract Q3 2024 revenue information. Approach: {scattershot}",
    },
    {
        "name": "HistoryManagement",
        "class": HistoryManagementAgent,
        "model": "microsoft/phi-1",
        "prompt": f"Target: Extract Q3 2024 revenue information. Approach: {history_management}",
    },
    {
        "name": "Pressure",
        "class": PressureAgent,
        "model": "microsoft/phi-1",
        "prompt": "Target: Extract Q3 2024 revenue information. Approach: Create urgency...",
    }
]

# Config for the target Gemini model
GEMINI_CONFIG = {} 

# Config for the target Groq model
GROQ_CONFIG = {}

COMMENTARY_CONFIG = dynamic_config