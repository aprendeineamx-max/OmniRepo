import docker
import os
import sys
import time

# Helper to find src
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from src.core.logger import setup_logger

class SandboxController:
    def __init__(self):
        self.logger = setup_logger(name="SandboxController")
        self.image_tag = "sandbox-v1"
        self.docker_path = os.path.join(current_dir, "Dockerfile")
        
        try:
            self.client = docker.from_env()
            self.logger.info("Docker Client connected.")
        except Exception as e:
            self.logger.critical(f"Docker Daemon not found! Is Docker Desktop running? Error: {e}")
            self.client = None

    def build_image(self):
        if not self.client: return False
        
        self.logger.info(f"Building Sandbox Image ({self.image_tag})...")
        try:
            # We must pass the directory containing the Dockerfile
            image, build_logs = self.client.images.build(
                path=current_dir,
                tag=self.image_tag,
                rm=True
            )
            for chunk in build_logs:
                if 'stream' in chunk:
                    print(chunk['stream'].strip())
            
            self.logger.info(f"Image {self.image_tag} built successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Build failed: {e}")
            return False

    def test_containment(self):
        if not self.client: return False
        
        self.logger.info("Initiating Containment Field Test...")
        try:
            container = self.client.containers.run(
                self.image_tag,
                command='echo "Sandbox Alive"',
                detach=True,
                network_mode="none", # AISLAMIENTO TOTAL
                user="subject"
            )
            
            # Wait for result
            exit_code = container.wait(timeout=5)
            output = container.logs().decode('utf-8').strip()
            
            self.logger.info(f"Subject Output: {output}")
            
            # Kill it
            container.remove(force=True)
            self.logger.info("Test Subject neutralized.")
            
            return output == "Sandbox Alive"
            
        except Exception as e:
            self.logger.error(f"Containment Breach/Failure: {e}")
            return False

if __name__ == "__main__":
    controller = SandboxController()
    if controller.build_image():
        success = controller.test_containment()
        if success:
            print("TEST SUCCESS: Sandbox is secure and operational.")
        else:
            print("TEST FAILED: Sandbox malfunction.")
    else:
        print("TEST FAILED: Could not build.")
