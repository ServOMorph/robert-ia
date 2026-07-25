import { useState } from 'react'
import { formatLiters } from '../utils/water'
import './Welcome.css'

export default function Welcome({ onConsent, waterLiters = 0 }) {
  const [accepted, setAccepted] = useState(false)
  const [showWaterInfo, setShowWaterInfo] = useState(false)

  return (
    <div className="screen welcome-screen">
      <div className="welcome-card card fade-in-up">
        <div className="welcome-logo">
          <img src="/logo_sereniatch.png" alt="SérénIATech" className="logo-img" />
        </div>

        <h1 className="welcome-title">Robert</h1>
        <p className="welcome-subtitle">
          Votre assistant local, disponible sans connexion internet.
        </p>

        <div className="welcome-water">
          <span className="welcome-water-drop">💧</span>
          <div className="welcome-water-figures">
            <strong>~{formatLiters(waterLiters)} L d'eau économisés</strong>
            <small>au total, comparé à une IA en ligne (estimation)</small>
          </div>
          <button
            type="button"
            className="welcome-water-info-btn"
            onClick={() => setShowWaterInfo(true)}
          >
            Plus d'infos
          </button>
        </div>

        {showWaterInfo && (
          <div
            className="water-info-overlay"
            role="dialog"
            aria-modal="true"
            aria-labelledby="water-info-title"
            onClick={() => setShowWaterInfo(false)}
          >
            <div className="water-info-modal" onClick={(e) => e.stopPropagation()}>
              <p id="water-info-title" className="water-info-title">Comment Robert économise de l'eau</p>
              <p className="water-info-body">
                Les IA en ligne (ChatGPT et autres) tournent dans des centres de données qui
                consomment de l'eau pour leur refroidissement, en plus de l'électricité nécessaire
                à leur fonctionnement. Robert fonctionne en local, sur cet ordinateur, sans passer
                par ces infrastructures : chaque message échangé ici évite cette consommation.
              </p>
              <p className="water-info-body">
                L'estimation retenue est de 0,3 L par message, une valeur prudente située entre les
                bornes documentées (0,26 ml pour le seul refroidissement direct selon Google, jusqu'à
                environ 0,5 L en intégrant la production électrique selon UC Riverside).
              </p>
              <button
                type="button"
                className="btn-primary water-info-close"
                onClick={() => setShowWaterInfo(false)}
              >
                Fermer
              </button>
            </div>
          </div>
        )}

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
      <p className="welcome-disclaimer">
        Robert est une expérimentation. Cette version tourne sur un ordinateur de récupération, sans connexion internet. Les réponses peuvent être lentes ou imparfaites — c'est normal, c'est un début.
      </p>
      <p className="welcome-version">v{__APP_VERSION__}</p>
    </div>
  )
}
