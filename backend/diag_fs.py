import os
import sys
from pathlib import Path

log_file = "diag_results.txt"

def log(msg):
    with open(log_file, "a") as f:
        f.write(msg + "\n")
    print(msg)

if os.path.exists(log_file):
    os.remove(log_file)

user_home = str(Path.home())
onedrive = os.path.join(user_home, "OneDrive")

paths = [
    user_home,
    os.path.join(user_home, "Desktop"),
    os.path.join(user_home, "Documents"),
    os.path.join(user_home, "Downloads"),
    os.path.join(user_home, "OneDrive"),
    os.path.join(onedrive, "Desktop"),
    os.path.join(onedrive, "Documents"),
]

log(f"User Home: {user_home}")
log(f"OneDrive Path: {onedrive}")
log(f"OneDrive Exists: {os.path.exists(onedrive)}")

for p in paths:
    log(f"\nChecking Path: {p}")
    exists = os.path.exists(p)
    log(f"  Exists: {exists}")
    if exists:
        log(f"  Is Dir: {os.path.isdir(p)}")
        log(f"  Is Link: {os.path.islink(p)}")
        try:
            entries = os.listdir(p)
            log(f"  Entries Count: {len(entries)}")
            if entries:
                log(f"  Sample: {entries[0]}")
        except Exception as e:
            log(f"  ListDir Error: {e}")

log("\nNormalization Tests:")
p_doc = os.path.join(user_home, "Documents")
log(f"Original: {p_doc}")
log(f"Abspath: {os.path.abspath(p_doc)}")
log(f"Realpath: {os.path.realpath(p_doc)}")
log(f"Casefolded: {p_doc.lower()}")
