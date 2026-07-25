import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import App from '../App'

describe('App — navigation', () => {
  beforeEach(() => {
    global.fetch = vi.fn((url) => {
      if (url === '/api/ready') {
        return Promise.resolve({ json: () => Promise.resolve({ ready: true }) })
      }
      if (url === '/api/water-stats') {
        return Promise.resolve({ json: () => Promise.resolve({ liters: 0 }) })
      }
      return Promise.reject(new Error(`fetch non mocké: ${url}`))
    })
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('démarre sur l\'écran Welcome', async () => {
    render(<App />)
    await waitFor(() => expect(screen.getByRole('checkbox')).toBeInTheDocument(), {
      timeout: 3000,
    })
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Robert')
  })

  it('passe à Pseudo après consentement', async () => {
    render(<App />)
    await waitFor(() => expect(screen.getByRole('checkbox')).toBeInTheDocument(), {
      timeout: 3000,
    })
    fireEvent.click(screen.getByRole('checkbox'))
    fireEvent.click(screen.getByRole('button', { name: /commencer/i }))
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  it('passe à Chat après saisie du pseudo', async () => {
    render(<App />)
    await waitFor(() => expect(screen.getByRole('checkbox')).toBeInTheDocument(), {
      timeout: 3000,
    })
    fireEvent.click(screen.getByRole('checkbox'))
    fireEvent.click(screen.getByRole('button', { name: /commencer/i }))
    fireEvent.submit(screen.getByRole('textbox').closest('form'))
    expect(screen.getAllByText(/Robert/).length).toBeGreaterThan(0)
    expect(screen.getByRole('button', { name: /terminer/i })).toBeInTheDocument()
  })

  it('revient à Welcome après Terminer', async () => {
    render(<App />)
    await waitFor(() => expect(screen.getByRole('checkbox')).toBeInTheDocument(), {
      timeout: 3000,
    })
    fireEvent.click(screen.getByRole('checkbox'))
    fireEvent.click(screen.getByRole('button', { name: /commencer/i }))
    fireEvent.submit(screen.getByRole('textbox').closest('form'))
    fireEvent.click(screen.getByRole('button', { name: /terminer/i }))
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Robert')
  })
})
