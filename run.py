#!/usr/bin/env python
"""Lance le backend (FastAPI) et le frontend (Vite) en parallèle."""

import subprocess
import sys
import threading
import time
from pathlib import Path


def relay_output(proc, label):
    for line in proc.stdout:
        print(f"[{label}] {line.rstrip()}")


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

    # Utilise le venv du backend s'il existe, sinon le Python courant
    venv_python = backend_dir / "venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    python_exe = str(venv_python) if venv_python.exists() else sys.executable

    # Lance le backend
    print("🚀 Démarrage backend (FastAPI)...")
    backend_proc = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "main:app", "--reload"],
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

    # Relaie la sortie de chaque serveur dans un thread dédié
    threads = [
        threading.Thread(target=relay_output, args=(backend_proc, "backend"), daemon=True),
        threading.Thread(target=relay_output, args=(frontend_proc, "frontend"), daemon=True),
    ]
    for thread in threads:
        thread.start()

    try:
        while True:
            if backend_proc.poll() is not None or frontend_proc.poll() is not None:
                print("\n❌ Un serveur s'est arrêté.")
                break
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt des serveurs...")

    for proc in (backend_proc, frontend_proc):
        if proc.poll() is None:
            proc.terminate()
    for proc in (backend_proc, frontend_proc):
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    print("✅ Serveurs arrêtés.")

if __name__ == "__main__":
    main()
