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

const SUGGESTIONS = ['Question A', 'Question B', 'Question C']

function mockFetch(suggestions = []) {
  return vi.fn((url) => {
    if (String(url).includes('/api/suggestions')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ suggestions }) })
    }
    return Promise.resolve(mockStreamResponse(['Bonjour']))
  })
}

describe('Chat — bandeau eau économisée', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    global.fetch = mockFetch()
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.restoreAllMocks()
  })

  it('affiche le disclaimer au démarrage', async () => {
    render(<ChatHarness />)
    await act(async () => {
      await Promise.resolve()
      await Promise.resolve()
    })
    expect(screen.getByText(/Robert peut faire des erreurs/i)).toBeInTheDocument()
  })

  it("bascule vers le message eau après le délai d'alternance", async () => {
    render(<ChatHarness initialLiters={1.2} />)
    await act(async () => {
      await Promise.resolve()
      await Promise.resolve()
    })
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

describe('Chat — suggestions de questions', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    global.fetch = mockFetch(SUGGESTIONS)
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.restoreAllMocks()
  })

  async function renderWithSuggestions() {
    render(<ChatHarness />)
    await act(async () => {
      await Promise.resolve()
      await Promise.resolve()
    })
  }

  it('affiche les suggestions du contexte avant le premier message', async () => {
    await renderWithSuggestions()
    SUGGESTIONS.forEach((question) => {
      expect(screen.getByRole('button', { name: question })).toBeInTheDocument()
    })
  })

  it("n'affiche rien quand le backend ne renvoie aucune suggestion", async () => {
    global.fetch = mockFetch([])
    await renderWithSuggestions()
    expect(screen.queryByLabelText('Suggestions de questions')).not.toBeInTheDocument()
  })

  it('envoie la question au clic et masque les suggestions', async () => {
    await renderWithSuggestions()

    fireEvent.click(screen.getByRole('button', { name: SUGGESTIONS[0] }))

    await act(async () => {
      await Promise.resolve()
      await Promise.resolve()
    })

    const chatCall = global.fetch.mock.calls.find(([url]) => String(url).includes('/api/chat'))
    expect(JSON.parse(chatCall[1].body).message).toBe(SUGGESTIONS[0])
    expect(screen.getByText(SUGGESTIONS[0], { selector: '.message-bubble' })).toBeInTheDocument()
    expect(screen.queryByLabelText('Suggestions de questions')).not.toBeInTheDocument()
  })
})
