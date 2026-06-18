#!/usr/bin/env python
"""Lance le backend (FastAPI) et le frontend (Vite) en parallèle."""

import subprocess
import sys
import os
from pathlib import Path

def main():
    root = Path(__file__).parent
    backend_dir = root / "backend"
    frontend_dir = root / "frontend"

    # Vérifier les répertoires
    if not backend_dir.exists():
        print(f"❌ Répertoire backend non trouvé: {backend_dir}")
        sys.exit(1)
    if not frontend_dir.exists():
        print(f"❌ Répertoire frontend non trouvé: {frontend_dir}")
        sys.exit(1)

    # Lance le backend
    print("🚀 Démarrage backend (FastAPI)...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--reload"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Lance le frontend
    print("🚀 Démarrage frontend (Vite)...")
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        shell=True
    )

    print("\n✅ Les deux serveurs sont lancés :")
    print("   Backend  : http://localhost:8000")
    print("   Frontend : http://localhost:5173")
    print("\nAppuie sur Ctrl+C pour arrêter.\n")

    # Affiche la sortie
    try:
        while True:
            if backend_proc.poll() is not None or frontend_proc.poll() is not None:
                print("\n❌ Un serveur s'est arrêté.")
                break

            # Lire les lignes disponibles (non-bloquant sur Windows)
            try:
                line = backend_proc.stdout.readline()
                if line:
                    print(f"[backend] {line.rstrip()}")
            except:
                pass

            try:
                line = frontend_proc.stdout.readline()
                if line:
                    print(f"[frontend] {line.rstrip()}")
            except:
                pass
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt des serveurs...")
        backend_proc.terminate()
        frontend_proc.terminate()
        backend_proc.wait(timeout=5)
        frontend_proc.wait(timeout=5)
        print("✅ Serveurs arrêtés.")

if __name__ == "__main__":
    main()
