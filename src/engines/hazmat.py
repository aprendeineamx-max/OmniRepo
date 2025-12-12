import os
import re
import json
import sys

# Add root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from src.core.logger import setup_logger

class HazmatEngine:
    def __init__(self, target_path="vault/repo_target"):
        self.target_path = os.path.join(root_dir, target_path)
        self.report_path = os.path.join(root_dir, "vault", "security_audit.json")
        self.logger = setup_logger(name="HazmatEngine")
        
        # Threat Signatures
        self.signatures = {
            "DESTRUCTION": r"(rm\s+-rf|mkfs\.|:(){:|dd\s+if=)", # Basic fork bomb or deletion
            "EXECUTION": r"(eval\(|exec\(|subprocess\.call|os\.system\(|subprocess\.Popen)",
            "OBFUSCATION": r"([A-Za-z0-9+/]{50,}={0,2})", # Long B64 strings
            "C2_COMMS": r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", # IPv4
        }
        
        self.ignored_dirs = {".git", "__pycache__", "venv"}

    def scan(self):
        """
        Scans all files in target for threats.
        """
        self.logger.info(f"DEFCON 3: Initiating Hazmat Scan on {self.target_path}")
        
        audit_log = {
            "threats_found": [],
            "defcon_level": 5, # 5=Normal, 1=Critical
            "scanned_files": 0
        }
        
        if not os.path.exists(self.target_path):
            self.logger.error("Target missing!")
            return False

        for root, dirs, files in os.walk(self.target_path):
            # Filtering ignored dirs
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                self._scan_file(file_path, audit_log)

        # Determine DEFCON
        if audit_log["threats_found"]:
            audit_log["defcon_level"] = 1
            self.logger.hazmat(f"SCAN COMPLETE. THREATS DETECTED: {len(audit_log['threats_found'])}. DEFCON 1 ACTIVATED.")
        else:
            self.logger.info("Scan Clean. No active threats detected.")

        self._save_report(audit_log)

    def _scan_file(self, file_path, audit_log):
        audit_log["scanned_files"] += 1
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    for threat_type, regex in self.signatures.items():
                        if re.search(regex, line):
                            # FOUND ONE
                            threat = {
                                "type": threat_type,
                                "file": file_path,
                                "line": line_num,
                                "content": line.strip()[:100] # Truncate for safety
                            }
                            audit_log["threats_found"].append(threat)
                            
                            # Log immediately
                            self.logger.hazmat(f"THREAT DETECTED [{threat_type}] in {os.path.basename(file_path)}:{line_num}")
                            
        except Exception as e:
            self.logger.warning(f"Could not read {file_path}: {e}")

    def _save_report(self, data):
        try:
            with open(self.report_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            self.logger.info(f"Security Report saved to: {self.report_path}")
        except Exception as e:
            self.logger.error(f"Failed to save report: {e}")

if __name__ == "__main__":
    hazmat = HazmatEngine()
    hazmat.scan()
