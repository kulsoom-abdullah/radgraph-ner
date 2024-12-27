# config.py
import os

# Paths to data
RAW_DATA_DIR = os.path.join("data", "raw")
PROCESSED_DATA_DIR = os.path.join("data", "processed")

# Filenames or file paths
SECTION_FINDINGS_FILE = os.path.join(RAW_DATA_DIR, "section_findings.json")
SECTION_IMPRESSION_FILE = os.path.join(RAW_DATA_DIR, "section_impression.json")

# If you eventually want a list:
JSON_FILES = [SECTION_FINDINGS_FILE, SECTION_IMPRESSION_FILE]

# EDA parameters (optional placeholders)
TOKEN_LENGTH_HIST_BINS = 50
ENTITY_TYPE_PLOT_SIZE = (10, 6)


# LATER
# Model hyperparameters (e.g., MODEL_NAME, NUM_LABELS, LEARNING_RATE).
# Logging or experiment settings.

# # USAGE
# import config

# # Use config variables
# print("Raw data directory:", config.RAW_DATA_DIR)
# print("Findings file:", config.SECTION_FINDINGS_FILE)
