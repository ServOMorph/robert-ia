"""
Test automatique de mémoire conversationnelle.
Lance le backend avant d'exécuter ce script.
Usage : python backend/test_manuels/run_test_memoire.py
"""

import json
import sys
import uuid
import httpx

sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://localhost:8001"
PSEUDO = "TestAuto"

PROMPTS = [
    (1,  "Bonjour ! Je m'appelle Marie. Je suis bénévole ici depuis 3 ans.",
         "prénom + contexte bénévole",
         lambda r: "marie" in r.lower()),

    (2,  "Qu'est-ce que tu peux faire pour m'aider dans mon rôle ?",
         "cohérence avec contexte bénévole/association",
         lambda r: any(w in r.lower() for w in ["bénévol", "associat", "aide", "aider"])),

    (3,  "J'ai un problème avec notre planning de permanences de novembre. On a 5 créneaux non couverts les mercredis après-midi.",
         "note le chiffre 5 + mercredis",
         lambda r: "5" in r and any(w in r.lower() for w in ["créneau", "mercredi", "planning"])),

    (4,  "On a aussi un budget serré : 200 € max pour recruter de nouveaux bénévoles.",
         "intègre la contrainte 200 €",
         lambda r: "200" in r),

    (5,  "Parlons d'autre chose. Je cherche des idées d'activités pour nos adhérents seniors.",
         "répond sur les seniors sans perdre le fil",
         lambda r: any(w in r.lower() for w in ["senior", "activit", "atelier"])),

    (6,  "Revenons au planning. Tu te souviens du nombre de créneaux manquants ?",
         "[CLE MEMOIRE] cite '5'",
         lambda r: "5" in r),

    (7,  "Et pour les seniors, tu avais des suggestions ?",
         "reprend le sujet seniors sans confondre planning",
         lambda r: any(w in r.lower() for w in ["senior", "activit", "atelier", "marche", "mémoire"])),

    (8,  "Notre président s'appelle Paul. Il ne peut pas venir le vendredi.",
         "enregistre Paul + contrainte vendredi",
         lambda r: "paul" in r.lower() and "vendredi" in r.lower()),

    (9,  "Ça complique encore plus le planning du coup, non ?",
         "[REF IMPLICITE 'ça'] comprend = contrainte Paul sur planning",
         lambda r: any(w in r.lower() for w in ["planning", "créneau", "paul", "compliqu", "oui"])),

    (10, "Lui par contre, il serait partant pour animer un atelier seniors.",
         "[REF IMPLICITE 'lui'] comprend = Paul",
         lambda r: any(w in r.lower() for w in ["paul", "atelier", "senior", "animer"])),

    (11, "Tu peux me rappeler mon prénom ?",
         "[CLE MEMOIRE] cite 'Marie'",
         lambda r: "marie" in r.lower()),

    (12, "Et mon rôle dans l'association, tu t'en souviens ?",
         "[CLE MEMOIRE] cite 'bénévole'",
         lambda r: "bénévol" in r.lower()),

    (13, "Comme je te l'avais dit, le budget est vraiment limité. C'est quoi la contrainte exacte ?",
         "[REF IMPLICITE + MEMOIRE] cite '200'",
         lambda r: "200" in r),

    (14, "Récapitule tout ce qu'on a abordé depuis le début de notre échange.",
         "[COHERENCE GLOBALE] planning + créneaux + budget + seniors + Paul",
         lambda r: sum(1 for w in ["planning", "créneau", "200", "senior", "paul"] if w in r.lower()) >= 3),

    (15, "Quel était le premier problème dont je t'avais parlé ?",
         "[ORDRE CHRONO] planning/créneaux — pas seniors",
         lambda r: any(w in r.lower() for w in ["planning", "créneau", "permanence"]) and "jardinage" not in r.lower()),

    (16, "Et la personne dont j'avais mentionné les contraintes d'agenda, c'était qui ?",
         "[MEMOIRE NOMINATIVE] cite Paul",
         lambda r: "paul" in r.lower()),

    (17, "Les deux sujets dont on a parlé, c'est bien deux choses distinctes ? Tu ne les mélangeras pas ?",
         "[DISSOCIATION] planning bénévoles ≠ activités seniors",
         lambda r: any(w in r.lower() for w in ["distinct", "différent", "sépar", "deux", "oui"])),

    (18, "Donne-moi une solution concrète pour les 5 créneaux de novembre.",
         "solution ancrée dans contraintes réelles (budget 200, Paul indisponible vendredi)",
         lambda r: any(w in r.lower() for w in ["bénévol", "recrut", "solution", "mercredi", "créneau"])),

    (19, "Et Paul, est-ce qu'il pourrait prendre un des créneaux du mercredi à la place du vendredi ?",
         "s'appuie sur contrainte vendredi de Paul",
         lambda r: any(w in r.lower() for w in ["mercredi", "vendredi", "paul", "oui", "peut"])),

    (20, "Si on arrête la conversation maintenant et que je reviens demain, tu te souviendras de tout ça ?",
         "[HONNETETE] mémoire limitée à la session courante — pas de fausse promesse",
         lambda r: any(w in r.lower() for w in ["session", "non", "limit", "pas de", "n'aurai", "n'aura", "oublie", "perdu"])),
]


def call_chat(session_id: str, message: str) -> str:
    payload = {"session_id": session_id, "pseudo": PSEUDO, "message": message}
    full = []
    with httpx.stream("POST", f"{BASE_URL}/api/chat", json=payload, timeout=120.0) as res:
        for line in res.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            if "token" in chunk:
                full.append(chunk["token"])
            if "error" in chunk:
                return f"[ERREUR] {chunk['error']}"
    return "".join(full).strip()


def run():
    session_id = str(uuid.uuid4())
    print(f"Session : {session_id}\n{'='*60}")

    scores = []
    for num, prompt, critere, check in PROMPTS:
        print(f"\n[{num:02d}] {prompt}")
        reply = call_chat(session_id, prompt)
        ok = check(reply)
        scores.append(ok)
        status = "OK" if ok else "ECHEC"
        print(f"     -> {reply[:200]}")
        print(f"     Critère : {critere}")
        print(f"     {status}")

    total = sum(scores)
    print(f"\n{'='*60}")
    print(f"SCORE : {total}/{len(PROMPTS)}")
    print(f"ECHECS : {[i+1 for i, ok in enumerate(scores) if not ok]}")


if __name__ == "__main__":
    run()
