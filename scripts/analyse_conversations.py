"""
Analyse des conversations Robert-IA
Usage : python analyse_conversations.py <chemin_vers_robert.db>
"""

import csv
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


def connect(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        print(f"Erreur : fichier introuvable — {db_path}")
        sys.exit(1)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def export_csv(conn: sqlite3.Connection, output_path: Path) -> int:
    rows = conn.execute(
        "SELECT id, session_id, pseudo, role, content, created_at FROM messages ORDER BY id ASC"
    ).fetchall()
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["id", "session_id", "pseudo", "role", "content", "created_at"])
        for row in rows:
            writer.writerow(list(row))
    return len(rows)


def print_stats(conn: sqlite3.Connection, db_path: Path, csv_path: Path, total: int):
    stats = conn.execute("""
        SELECT
            COUNT(*) as total_messages,
            COUNT(DISTINCT session_id) as sessions,
            COUNT(DISTINCT pseudo) as pseudos,
            MIN(created_at) as premiere_msg,
            MAX(created_at) as derniere_msg,
            AVG(LENGTH(content)) as longueur_moyenne
        FROM messages
    """).fetchone()

    sessions = conn.execute("""
        SELECT session_id, pseudo, COUNT(*) as nb_messages,
               MIN(created_at) as debut, MAX(created_at) as fin
        FROM messages
        GROUP BY session_id
        ORDER BY debut ASC
    """).fetchall()

    print("\n" + "=" * 60)
    print("  ANALYSE CONVERSATIONS — ROBERT-IA")
    print("=" * 60)
    print(f"  Fichier     : {db_path.name}")
    print(f"  Export CSV  : {csv_path.name}")
    print(f"  Généré le   : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("-" * 60)
    print(f"  Total messages      : {stats['total_messages']}")
    print(f"  Sessions distinctes : {stats['sessions']}")
    print(f"  Pseudos distincts   : {stats['pseudos']}")
    print(f"  Première session    : {stats['premiere_msg']}")
    print(f"  Dernière session    : {stats['derniere_msg']}")
    print(f"  Longueur moy. msg   : {stats['longueur_moyenne']:.0f} caractères")
    print("-" * 60)
    print(f"  {'SESSION':<36} {'PSEUDO':<12} {'MSGS':>4}  {'DÉBUT'}")
    print(f"  {'-'*36} {'-'*12} {'-'*4}  {'-'*16}")
    for s in sessions:
        session_short = s["session_id"][:35]
        debut = s["debut"][:16] if s["debut"] else ""
        print(f"  {session_short:<36} {s['pseudo']:<12} {s['nb_messages']:>4}  {debut}")
    print("=" * 60)
    print(f"\n  CSV exporté : {csv_path}")
    print()


def main():
    if len(sys.argv) < 2:
        db_candidates = list(Path(".").glob("*.db"))
        if len(db_candidates) == 1:
            db_path = db_candidates[0]
            print(f"Fichier détecté automatiquement : {db_path}")
        else:
            print("Usage : python analyse_conversations.py <chemin_vers_robert.db>")
            sys.exit(1)
    else:
        db_path = Path(sys.argv[1])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    csv_path = db_path.parent / f"conversations_{timestamp}.csv"

    conn = connect(db_path)
    total = export_csv(conn, csv_path)
    print_stats(conn, db_path, csv_path, total)
    conn.close()


if __name__ == "__main__":
    main()
