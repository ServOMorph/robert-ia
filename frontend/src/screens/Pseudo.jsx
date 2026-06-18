import { useState } from 'react'
import './Pseudo.css'

export default function Pseudo({ onStart }) {
  const [pseudo, setPseudo] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    const name = pseudo.trim() || 'Anonyme'
    onStart(name)
  }

  return (
    <div className="screen pseudo-screen">
      <div className="pseudo-card card fade-in-up">
        <h2 className="pseudo-title">Comment souhaitez-vous être appelé(e) ?</h2>
        <p className="pseudo-hint">Optionnel — laissez vide pour rester anonyme.</p>

        <form className="pseudo-form" onSubmit={handleSubmit}>
          <input
            type="text"
            className="pseudo-input"
            placeholder="Votre prénom ou pseudo"
            value={pseudo}
            onChange={(e) => setPseudo(e.target.value)}
            maxLength={32}
            autoFocus
            aria-label="Prénom ou pseudo"
          />
          <button type="submit" className="btn-primary">
            {pseudo.trim() ? `Bonjour, ${pseudo.trim()} !` : 'Continuer anonymement'}
          </button>
        </form>
      </div>
    </div>
  )
}
