from pathlib import Path
import re

LOG_DIR = Path("logs")

patterns = {
    "failed_authentication": re.compile(r"Failed password", re.I),
    "successful_authentication": re.compile(r"Accepted password", re.I),
    "sudo_activity": re.compile(r"sudo:", re.I),
    "shadow_access": re.compile(r"/etc/shadow", re.I),
    "external_payload": re.compile(r"198\.51\.100\.42", re.I),
    "suspicious_source": re.compile(r"203\.0\.113\.77", re.I),
    "cron_persistence": re.compile(r"crontab|@reboot", re.I),
    "data_staging": re.compile(r"appdata\.tar\.gz", re.I),
}

results = {name: [] for name in patterns}

for log_file in sorted(LOG_DIR.glob("*.log")):
    for number, line in enumerate(log_file.read_text().splitlines(), start=1):
        for name, pattern in patterns.items():
            if pattern.search(line):
                results[name].append(
                    f"{log_file.name}:{number}: {line}"
                )

for name, matches in results.items():
    print(f"\n=== {name.replace('_', ' ').upper()} ===")
    if matches:
        for match in matches:
            print(match)
    else:
        print("No matches found")
