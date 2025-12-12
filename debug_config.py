from src.core.config import settings

def debug():
    print(f"Project: {settings.get('project_name')}")
    print(f"Version: {settings.get('version')}")
    print(f"Límite de Repositorio: {settings.get('limits.max_repo_size_mb')} MB")
    print(f"Vault Path: {settings.get('paths.vault')}")
    print(f"Hazmat Level: {settings.get('security.hazmat_level')}")

if __name__ == "__main__":
    debug()
