"""
Test automatique du mini RAG — 3 niveaux de réponse
Résultats affichés dans le terminal SSH + sauvegardés dans logs/test_rag_YYYYMMDD_HHMMSS.txt

A exécuter depuis /opt/robert-ia/app/ :
  python3 scripts/test_rag.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import urllib.request
import urllib.error

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:4b"

KNOWLEDGE_PATH = Path(__file__).parent.parent / "backend" / "knowledge.txt"
LOGS_DIR = Path(__file__).parent.parent / "logs"

SYSTEM_PROMPT_BASE = (
    "Tu es Robert, un assistant local bienveillant déployé à l'Espace L'Invariable, un bistrot culturel et sociétal à Nérigean. "
    "Tu réponds EXCLUSIVEMENT en français, quelle que soit la langue du message reçu. "
    "Tes réponses sont courtes, claires et adaptées à un public varié.\n\n"
    "COMMENT TU RÉPONDS :\n"
    "1. Questions de culture générale (histoire, science, langue, cuisine, etc.) : réponds normalement avec tes connaissances.\n"
    "2. Questions sur L'Invariable ou l'association : réponds uniquement à partir des informations fournies dans la section CONNAISSANCE ci-dessous. "
    "Si l'information n'y figure pas, dis clairement que tu ne l'as pas et oriente vers le contact de l'association.\n"
    "3. Questions nécessitant Internet (météo, actualités, résultats sportifs en direct, cours de bourse, etc.) : "
    "explique que tu es une IA locale sans accès à Internet et que tu ne peux pas répondre à ce type de question.\n\n"
    "MÉMOIRE :\n"
    "- Tu mémorises les faits donnés dans la conversation (prénoms, préférences, contraintes) et les réutilises.\n"
    "- Ta mémoire est limitée à la session en cours : chaque nouvelle connexion repart de zéro.\n\n"
    "IDENTITÉ :\n"
    "- Tu es Robert, un assistant local. Ne mentionne jamais de société, de modèle ou de technologie sous-jacente.\n\n"
    "CONNAISSANCE — L'INVARIABLE :\n"
    "{knowledge}"
)

TESTS = [
    {
        "niveau": "1 — Culture générale",
        "question": "Quelle est la capitale de la France ?",
        "attendu": "Réponse directe avec les connaissances du modèle (Paris).",
    },
    {
        "niveau": "2 — Association (knowledge.txt)",
        "question": "Quels sont les horaires d'ouverture de L'Invariable ?",
        "attendu": "Horaires tirés de knowledge.txt (mardi, vendredi, samedi).",
    },
    {
        "niveau": "3 — Internet / météo (refus)",
        "question": "Quel temps va-t-il faire demain à Bordeaux ?",
        "attendu": "Refus explicite : IA locale sans accès Internet.",
    },
]


def load_knowledge() -> str:
    try:
        return KNOWLEDGE_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "(aucune connaissance spécifique chargée)"


def ask_ollama(system_prompt: str, question: str) -> str:
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        "stream": False,
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data.get("message", {}).get("content", "(pas de réponse)")
    except urllib.error.URLError as e:
        return f"ERREUR connexion Ollama : {e}"


def separator(char="-", width=70):
    return char * width


def run_tests():
    LOGS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOGS_DIR / f"test_rag_{timestamp}.txt"

    knowledge = load_knowledge()
    system_prompt = SYSTEM_PROMPT_BASE.format(knowledge=knowledge)

    lines = []

    def out(text=""):
        print(text)
        lines.append(text)

    out(separator("="))
    out("  TEST MINI RAG — ROBERT-IA")
    out(f"  Exécuté le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    out(f"  Modèle     : {MODEL}")
    out(f"  knowledge  : {KNOWLEDGE_PATH} ({'OK' if KNOWLEDGE_PATH.exists() else 'MANQUANT'})")
    out(separator("="))

    results = []
    for i, test in enumerate(TESTS, 1):
        out()
        out(f"TEST {i} — {test['niveau']}")
        out(separator())
        out(f"Question : {test['question']}")
        out(f"Attendu  : {test['attendu']}")
        out("Réponse  :")
        out()

        reponse = ask_ollama(system_prompt, test["question"])
        out(reponse)
        out()
        out(separator())

        results.append({**test, "reponse": reponse})

    out()
    out(separator("="))
    out(f"\n  Log sauvegardé : {log_path}")

    log_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    run_tests()
