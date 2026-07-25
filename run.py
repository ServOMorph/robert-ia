#!/usr/bin/env python
"""Lance Robert-IA en local.

Par défaut : réplique la configuration du PC Linux (port 8001, contexte moulin_du_sud,
frontend statique servi par FastAPI, pas de rechargement automatique).
Avec --dev : backend sur 8001 avec --reload et serveur Vite sur 5173.
"""

import argparse
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

# Doivent rester alignés sur l'unité systemd du Linux (/etc/systemd/system/robert-ia.service)
# et sur scripts/start-backend.sh.
PROD_CONTEXT = "moulin_du_sud"
PROD_PORT = "8001"
PROD_MODEL = "gemma3:4b"


def relay_output(proc, label):
    for line in proc.stdout:
        print(f"[{label}] {line.rstrip()}")


def check_ollama():
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=10
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("⚠️  Ollama introuvable ou injoignable — le chat ne répondra pas.")
        return
    if PROD_MODEL not in result.stdout:
        print(f"⚠️  Modèle {PROD_MODEL} absent : lancer `ollama pull {PROD_MODEL}`.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dev",
        action="store_true",
        help="mode développement : rechargement auto + serveur Vite",
    )
    args = parser.parse_args()

    root = Path(__file__).parent
    backend_dir = root / "backend"
    frontend_dir = root / "frontend"

    if not backend_dir.exists():
        print(f"❌ Répertoire backend non trouvé: {backend_dir}")
        sys.exit(1)
    if not frontend_dir.exists():
        print(f"❌ Répertoire frontend non trouvé: {frontend_dir}")
        sys.exit(1)

    if not (frontend_dir / "dist" / "index.html").exists():
        print("❌ Frontend non compilé. Lancer : cd frontend && npm run build")
        sys.exit(1)

    venv_python = backend_dir / "venv" / (
        "Scripts/python.exe" if sys.platform == "win32" else "bin/python"
    )
    python_exe = str(venv_python) if venv_python.exists() else sys.executable

    check_ollama()

    backend_cmd = [python_exe, "-m", "uvicorn", "main:app", "--port", PROD_PORT]
    if args.dev:
        backend_cmd += ["--reload"]
    else:
        backend_cmd += ["--log-level", "warning"]

    backend_env = {**os.environ, "ROBERT_CONTEXT": PROD_CONTEXT}

    print(f"🚀 Démarrage backend (contexte {PROD_CONTEXT}, port {PROD_PORT})...")
    procs = [
        (
            "backend",
            subprocess.Popen(
                backend_cmd,
                cwd=backend_dir,
                env=backend_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            ),
        )
    ]

    if args.dev:
        print("🚀 Démarrage frontend (Vite)...")
        procs.append(
            (
                "frontend",
                subprocess.Popen(
                    ["npm", "run", "dev"],
                    cwd=frontend_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    shell=True,
                ),
            )
        )

    print("\n✅ Robert-IA est lancé :")
    print(f"   Application : http://localhost:{PROD_PORT}")
    if args.dev:
        print("   Vite (dev)  : http://localhost:5173")
    else:
        print("   Configuration identique au PC Linux (hors base SQLite, locale).")
    print("\nAppuie sur Ctrl+C pour arrêter.\n")

    for label, proc in procs:
        threading.Thread(
            target=relay_output, args=(proc, label), daemon=True
        ).start()

    try:
        while True:
            if any(proc.poll() is not None for _, proc in procs):
                print("\n❌ Un serveur s'est arrêté.")
                break
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt des serveurs...")

    for _, proc in procs:
        if proc.poll() is None:
            proc.terminate()
    for _, proc in procs:
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    print("✅ Serveurs arrêtés.")


if __name__ == "__main__":
    main()
