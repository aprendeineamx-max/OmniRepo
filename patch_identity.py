import os

files_to_patch = {
    r"c:/Users/Administrator/Analizador de repos/.agent/rules/02-nexus-protocol.md": [
        ("CODEX_OMEGA_HASH", "GEMINI_HASH")
    ],
    r"c:/Users/Administrator/Analizador de repos/.agent/rules/06-singularity-logic.md": [
        ("Eres CODEX-OMEGA.", "Eres GEMINI.")
    ]
}

def patch_files():
    for file_path, replacements in files_to_patch.items():
        if not os.path.exists(file_path):
            print(f"Skipping {file_path}, not found.")
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        for old, new in replacements:
            new_content = new_content.replace(old, new)
            
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Patched {file_path}")
        else:
            print(f"No changes needed for {file_path}")

if __name__ == "__main__":
    patch_files()
