import { useState, useRef, useEffect } from 'react'
import './Chat.css'

function generateSessionId() {
  return crypto.randomUUID()
}

export default function Chat({ pseudo, onEnd }) {
  const [sessionId] = useState(generateSessionId)
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `Bonjour${pseudo !== 'Anonyme' ? ` ${pseudo}` : ''} ! Je suis Robert, votre assistant local. Comment puis-je vous aider ?`,
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView?.({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    const text = input.trim()
    if (!text || loading) return

    const userMsg = { role: 'user', content: text }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, pseudo, message: text }),
      })
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail || `Erreur ${res.status}`)
      }
      const data = await res.json()
      setMessages((prev) => [...prev, { role: 'assistant', content: data.reply }])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: `Désolé, une erreur s'est produite : ${err.message}` },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-screen">
      <header className="chat-header">
        <span className="chat-logo-initial">R</span>
        <span className="chat-name">Robert</span>
        <button className="btn-secondary chat-end" onClick={onEnd} aria-label="Terminer la session">
          Terminer
        </button>
      </header>

      <main className="chat-messages" aria-live="polite" aria-label="Conversation">
        {messages.map((msg, i) => (
          <div key={i} className={`message message--${msg.role}`}>
            <div className="message-bubble">{msg.content}</div>
          </div>
        ))}
        {loading && (
          <div className="message message--assistant">
            <div className="message-bubble message-bubble--typing">
              <span />
              <span />
              <span />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </main>

      <form className="chat-form" onSubmit={sendMessage}>
        <input
          type="text"
          className="chat-input"
          placeholder="Écrivez votre message…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
          aria-label="Message"
          autoFocus
        />
        <button
          type="submit"
          className="btn-primary chat-send"
          disabled={!input.trim() || loading}
          aria-label="Envoyer"
        >
          Envoyer
        </button>
      </form>
    </div>
  )
}
