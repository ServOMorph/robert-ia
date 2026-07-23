import { useState } from 'react'
import { render, screen, fireEvent, act } from '@testing-library/react'
import { vi } from 'vitest'
import Chat from '../screens/Chat'

function mockStreamResponse(tokens) {
  const encoder = new TextEncoder()
  let i = 0
  return {
    ok: true,
    body: {
      getReader: () => ({
        read: async () => {
          if (i < tokens.length) {
            const chunk = JSON.stringify({ token: tokens[i] }) + '\n'
            i += 1
            return { done: false, value: encoder.encode(chunk) }
          }
          return { done: true, value: undefined }
        },
      }),
    },
  }
}

function ChatHarness({ initialLiters = 0 }) {
  const [waterLiters, setWaterLiters] = useState(initialLiters)
  return (
    <Chat
      pseudo="Anonyme"
      onEnd={() => {}}
      waterLiters={waterLiters}
      onMessageSent={() => setWaterLiters((l) => l + 0.3)}
    />
  )
}

describe('Chat — bandeau eau économisée', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    global.fetch = vi.fn(() => Promise.resolve(mockStreamResponse(['Bonjour'])))
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.restoreAllMocks()
  })

  it('affiche le disclaimer au démarrage', () => {
    render(<ChatHarness />)
    expect(screen.getByText(/Robert peut faire des erreurs/i)).toBeInTheDocument()
  })

  it("bascule vers le message eau après le délai d'alternance", () => {
    render(<ChatHarness initialLiters={1.2} />)
    act(() => {
      vi.advanceTimersByTime(8000)
    })
    expect(screen.getByText(/~1,2 L/)).toBeInTheDocument()
  })

  it("incrémente le compteur eau après l'envoi d'un message", async () => {
    render(<ChatHarness />)

    const input = screen.getByLabelText('Message')
    fireEvent.change(input, { target: { value: 'Bonjour' } })
    fireEvent.submit(input.closest('form'))

    await act(async () => {
      await Promise.resolve()
      await Promise.resolve()
    })

    act(() => {
      vi.advanceTimersByTime(8000)
    })

    expect(screen.getByText(/~0,3 L/)).toBeInTheDocument()
  })
})
