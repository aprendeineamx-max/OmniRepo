import os
import sys
import time
import json
import threading

# Add root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from src.core.config import settings
from src.core.logger import setup_logger
from src.nexus.core import NexusCore
from src.engines.ingestor import Ingestor
from src.engines.recon import ReconEngine
from src.engines.polyglot import PolyglotEngine
from src.engines.hazmat import HazmatEngine

class AutopsyOrchestrator:
    def __init__(self):
        self.logger = setup_logger(name="Orchestrator")
        self.nexus = NexusCore()
        self.ingestor = Ingestor()
        self.recon = ReconEngine()
        self.polyglot = PolyglotEngine()
        self.hazmat = HazmatEngine()
        
        self.logger.info(f"Orchestrator initialized. Project: {settings.get('project_name')}")

    def run(self, url):
        """
        Executes the full Autopsy Sequence V1.
        """
        print("\n" + "="*60)
        print(f"🚀 INITIATING AUTOPSY SEQUENCE FOR: {url}")
        print("="*60 + "\n")
        
        # 1. Activate Nexus (The Nervous System)
        if not self.nexus.running:
            self.logger.info("Sparking Nexus Synapses...")
            # Run nexus start in a separate thread so it doesn't block main
            nexus_thread = threading.Thread(target=self.nexus.start, daemon=True)
            nexus_thread.start()
            time.sleep(1) # Let it warm up
        
        print("[1/5] 📡 Nexus Link: STARTED")

        # 2. Ingestions (The Mouth)
        print("[2/5] 📥 Ingestion: CLONING...")
        if not self.ingestor.clone_repo(url):
            self.logger.critical("Aborting Autopsy: Ingestion Failed.")
            return
        print("      -> Ingestion COMPLETE")

        # 3. Surface Recon (The Eyes)
        print("[3/5] 🛰️ Recon: SCANNING...")
        self.recon.scan()
        print("      -> Recon COMPLETE")

        # 4. Language Analysis (The Frontal Lobe)
        print("[4/5] 🗣️ Polyglot: ANALYZING...")
        self.polyglot.analyze()
        print("      -> Polyglot COMPLETE")

        # 5. Hazmat Scan (The Immune System)
        print("[5/5] ☣️ Hazmat: SWEEPING...")
        self.hazmat.scan()
        print("      -> Hazmat COMPLETE")

        # Final Verdict
        self._check_vitals()

    def _check_vitals(self):
        """
        Reviews reports to determine go/no-go.
        """
        report_path = os.path.join(root_dir, "vault", "security_audit.json")
        try:
            with open(report_path, 'r') as f:
                data = json.load(f)
            
            defcon = data.get("defcon_level", 5)
            threats = len(data.get("threats_found", []))
            
            print("\n" + "-"*60)
            if defcon == 1:
                print(f"🚨 CRITICAL ALERT: DEFCON 1 ACTIVATED ({threats} threats found)")
                print("   SYSTEM LOCKED DOWN. MANUAL INTERVENTION REQUIRED.")
            else:
                print("✅ SISTEMA LISTO PARA AUTOPSIA PROFUNDA")
                print(f"   Status: NOMINAL (DEFCON {defcon})")
            print("-"*60 + "\n")

        except Exception as e:
            self.logger.error(f"Failed to read security report: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = "https://github.com/octocat/Spoon-Knife"
        
    orchestrator = AutopsyOrchestrator()
    orchestrator.run(target_url)
