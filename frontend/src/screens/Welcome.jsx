import { useState } from 'react'
import './Welcome.css'

export default function Welcome({ onConsent }) {
  const [accepted, setAccepted] = useState(false)

  return (
    <div className="screen welcome-screen">
      <div className="welcome-card card fade-in-up">
        <div className="welcome-logo">
          <span className="logo-initial">R</span>
        </div>

        <h1 className="welcome-title">Robert</h1>
        <p className="welcome-subtitle">
          Votre assistant local, disponible sans connexion internet.
        </p>

        <div className="rgpd-notice">
          <h2>Informations sur vos données</h2>
          <ul>
            <li>Votre session est <strong>anonyme</strong> — aucun compte requis.</li>
            <li>Vos échanges restent <strong>sur cet appareil</strong>, ils ne sont jamais transmis à l'extérieur.</li>
            <li>L'historique peut être consulté par les animateurs de cet espace à des fins d'amélioration du service.</li>
            <li>Aucune donnée personnelle n'est collectée ni partagée.</li>
          </ul>
        </div>

        <label className="consent-checkbox">
          <input
            type="checkbox"
            checked={accepted}
            onChange={(e) => setAccepted(e.target.checked)}
            aria-label="J'ai lu et j'accepte les conditions d'utilisation"
          />
          <span>J'ai compris et j'accepte</span>
        </label>

        <button
          className="btn-primary"
          onClick={onConsent}
          disabled={!accepted}
          aria-disabled={!accepted}
        >
          Commencer
        </button>
      </div>
    </div>
  )
}
