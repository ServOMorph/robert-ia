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

    setMessages((prev) => [...prev, { role: 'user', content: text }])
    setInput('')
    setLoading(true)

    setMessages((prev) => [...prev, { role: 'assistant', content: '' }])

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, pseudo, message: text }),
      })
      if (!res.ok) {
        throw new Error(`Erreur ${res.status}`)
      }

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop()

        for (const line of lines) {
          if (!line.trim()) continue
          const chunk = JSON.parse(line)
          if (chunk.error) {
            setMessages((prev) => {
              const updated = [...prev]
              updated[updated.length - 1] = { role: 'assistant', content: `Erreur : ${chunk.error}` }
              return updated
            })
            return
          }
          if (chunk.token) {
            setMessages((prev) => {
              const updated = [...prev]
              updated[updated.length - 1] = {
                role: 'assistant',
                content: updated[updated.length - 1].content + chunk.token,
              }
              return updated
            })
          }
        }
      }
    } catch (err) {
      setMessages((prev) => {
        const updated = [...prev]
        updated[updated.length - 1] = {
          role: 'assistant',
          content: `Désolé, une erreur s'est produite : ${err.message}`,
        }
        return updated
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-screen">
      <header className="chat-header">
        <span className="chat-logo-initial">R</span>
        <div className="chat-header-info">
          <span className="chat-name">Robert</span>
          <span className="chat-disclaimer">Robert peut faire des erreurs. Gardez votre esprit critique.</span>
        </div>
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
