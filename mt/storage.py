# ==========================================================
# MONEY TRACKER - SAFE DATA STORAGE
# ==========================================================
import json
import os
import shutil
from datetime import datetime
from config import BACKUP_FOLDER, LEGACY_FILES

def _migrate_legacy_file(filename):
    if os.path.exists(filename): return
    legacy = LEGACY_FILES.get(filename)
    if legacy and os.path.exists(legacy):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        shutil.copy2(legacy, filename)

def load_json(filename, default):
    _migrate_legacy_file(filename)
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            return default
    return default

def _backup_file(filename):
    if not os.path.exists(filename): return None
    try:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup = os.path.join(BACKUP_FOLDER, f"{os.path.basename(filename)}.{stamp}.bak")
        shutil.copy2(filename, backup)
        return backup
    except Exception:
        return None

def save_json(filename, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    temp_file = filename + ".tmp"
    _backup_file(filename)
    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        file.flush(); os.fsync(file.fileno())
    os.replace(temp_file, filename)
