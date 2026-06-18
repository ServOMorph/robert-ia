import { render, screen, fireEvent } from '@testing-library/react'
import Welcome from '../screens/Welcome'

describe('Welcome', () => {
  it('affiche le titre Robert', () => {
    render(<Welcome onConsent={() => {}} />)
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Robert')
  })

  it('le bouton Commencer est désactivé sans consentement', () => {
    render(<Welcome onConsent={() => {}} />)
    expect(screen.getByRole('button', { name: /commencer/i })).toBeDisabled()
  })

  it('le bouton Commencer est activé après cocher la case', () => {
    render(<Welcome onConsent={() => {}} />)
    fireEvent.click(screen.getByRole('checkbox'))
    expect(screen.getByRole('button', { name: /commencer/i })).not.toBeDisabled()
  })

  it('appelle onConsent au clic après consentement', () => {
    const onConsent = vi.fn()
    render(<Welcome onConsent={onConsent} />)
    fireEvent.click(screen.getByRole('checkbox'))
    fireEvent.click(screen.getByRole('button', { name: /commencer/i }))
    expect(onConsent).toHaveBeenCalledOnce()
  })

  it('affiche la notice RGPD', () => {
    render(<Welcome onConsent={() => {}} />)
    expect(screen.getByText(/anonyme/i)).toBeInTheDocument()
  })
})
