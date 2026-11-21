"""soulcal: the SOUL-Calibrate engine (personal baseline, fusion, speak / ask / quiet, situation memory,
words-vs-expression disagreement, personal pattern graph). Author: Emanuele De Bernardis. MIT License."""

from .engine import EngineConfig, SoulEngine, calibrate_thresholds
from .schema import STATES, Decision, Profile, Reading, basic_emotions_to_states, read_csv, write_csv

__all__ = ["EngineConfig", "SoulEngine", "calibrate_thresholds", "STATES", "Decision", "Profile", "Reading",
           "basic_emotions_to_states", "read_csv", "write_csv"]
__version__ = "0.1.0"
