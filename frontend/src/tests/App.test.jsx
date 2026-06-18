import { render, screen, fireEvent } from '@testing-library/react'
import App from '../App'

describe('App — navigation', () => {
  it('démarre sur l\'écran Welcome', () => {
    render(<App />)
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Robert')
  })

  it('passe à Pseudo après consentement', () => {
    render(<App />)
    fireEvent.click(screen.getByRole('checkbox'))
    fireEvent.click(screen.getByRole('button', { name: /commencer/i }))
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  it('passe à Chat après saisie du pseudo', () => {
    render(<App />)
    fireEvent.click(screen.getByRole('checkbox'))
    fireEvent.click(screen.getByRole('button', { name: /commencer/i }))
    fireEvent.submit(screen.getByRole('textbox').closest('form'))
    expect(screen.getAllByText(/Robert/).length).toBeGreaterThan(0)
    expect(screen.getByRole('button', { name: /terminer/i })).toBeInTheDocument()
  })

  it('revient à Welcome après Terminer', () => {
    render(<App />)
    fireEvent.click(screen.getByRole('checkbox'))
    fireEvent.click(screen.getByRole('button', { name: /commencer/i }))
    fireEvent.submit(screen.getByRole('textbox').closest('form'))
    fireEvent.click(screen.getByRole('button', { name: /terminer/i }))
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Robert')
  })
})
