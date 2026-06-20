import { useEffect } from 'react'
import './Loading.css'

export default function Loading({ onReady }) {
  useEffect(() => {
    const check = async () => {
      try {
        const res = await fetch('/api/ready')
        const data = await res.json()
        if (data.ready) {
          onReady()
          return
        }
      } catch (_) {}
      setTimeout(check, 2000)
    }
    const t = setTimeout(check, 1000)
    return () => clearTimeout(t)
  }, [onReady])

  return (
    <div className="screen loading-screen">
      <div className="loading-card card">
        <div className="loading-logo">
          <img src="/logo_sereniatch.png" alt="SérénIATech" className="logo-img" />
        </div>
        <h1 className="loading-title">Robert</h1>
        <p className="loading-message">Démarrage en cours</p>
        <div className="loading-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  )
}
