import threading
import time
import os
import sys
import json
import shutil
import platform
from datetime import datetime

# Import Logger
# Adjusting path to ensure src can be found if running from root
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from src.core.logger import setup_logger

class NexusCore:
    def __init__(self, nexus_dir="nexus_link"):
        self.nexus_dir = nexus_dir
        self.commands_dir = os.path.join(self.nexus_dir, "commands")
        self.history_dir = os.path.join(self.nexus_dir, "history")
        self.status_file = os.path.join(self.nexus_dir, "status.json")
        self.logger = setup_logger(name="NexusCore")
        self.running = False
        
        # Try to import psutil
        try:
            import psutil
            self.psutil = psutil
        except ImportError:
            self.psutil = None
            self.logger.warning("psutil not found. Using dummy stats.")

    def _initialize_bunker(self):
        """Ensure Nexus directories exist."""
        for path in [self.nexus_dir, self.commands_dir, self.history_dir]:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
                self.logger.info(f"Initialized Nexus channel: {path}")

    def _get_vital_signs(self):
        """Collect system stats."""
        stats = {
            "status": "ALIVE",
            "timestamp": datetime.utcnow().isoformat(),
            "system": platform.system(),
        }
        
        if self.psutil:
            stats["cpu"] = self.psutil.cpu_percent(interval=None)
            stats["ram"] = self.psutil.virtual_memory().percent
        else:
            stats["cpu"] = "Unknown (pip install psutil)"
            stats["ram"] = "Unknown"
            
        return stats

    def _heartbeat_loop(self):
        """Writes status.json every 1s."""
        self.logger.info("Heartbeat Emitter [ONLINE]")
        while self.running:
            try:
                data = self._get_vital_signs()
                # Write atomic? For now simple write is enough for prototype
                with open(self.status_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                self.logger.error(f"Heartbeat failure: {e}")
            
            time.sleep(1)

    def _watcher_loop(self):
        """Watches commands/ folder for new .json files."""
        self.logger.info("Nexus Watcher [ONLINE]")
        while self.running:
            try:
                # Scan for json files
                if not os.path.exists(self.commands_dir):
                    time.sleep(1)
                    continue

                files = [f for f in os.listdir(self.commands_dir) if f.endswith('.json')]
                
                for filename in files:
                    file_path = os.path.join(self.commands_dir, filename)
                    
                    # Read command
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            command = json.load(f)
                        
                        self.logger.info(f"NEXUS SIGNAL RECEIVED: {filename} | Action: {command.get('action', 'UNKNOWN')}")
                        
                        # Process command (Stub for now, just acknowledge)
                        # In the future, this calls an Execution Engine
                        
                        # Archive command
                        dest_path = os.path.join(self.history_dir, filename)
                        shutil.move(file_path, dest_path)
                        self.logger.info(f"Archived signal to: {dest_path}")
                        
                    except json.JSONDecodeError:
                        self.logger.error(f"Corrupted signal received: {filename}")
                        shutil.move(file_path, os.path.join(self.history_dir, f"INVALID_{filename}"))
                    except Exception as e:
                        self.logger.error(f"Error processing signal {filename}: {e}")

            except Exception as e:
                self.logger.error(f"Watcher error: {e}")
            
            time.sleep(0.5)

    def start(self):
        self._initialize_bunker()
        self.running = True
        
        # Start Threads
        self.t_heartbeat = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.t_watcher = threading.Thread(target=self._watcher_loop, daemon=True)
        
        self.t_heartbeat.start()
        self.t_watcher.start()
        
        self.logger.info("Nexus Link Established. Listening...")
        
        try:
            # Keep main thread alive to allow background threads to run
            # In a real app this might be part of a bigger loop
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.logger.info("Severing Nexus Link...")
        self.running = False
        self.t_heartbeat.join(timeout=2)
        self.t_watcher.join(timeout=2)
        self.logger.info("Nexus Link Offline.")

if __name__ == "__main__":
    nexus = NexusCore()
    nexus.start()
