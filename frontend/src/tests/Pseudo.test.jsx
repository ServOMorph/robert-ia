import { render, screen, fireEvent } from '@testing-library/react'
import Pseudo from '../screens/Pseudo'

describe('Pseudo', () => {
  it('affiche le champ pseudo', () => {
    render(<Pseudo onStart={() => {}} />)
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  it('le bouton dit "Continuer anonymement" si champ vide', () => {
    render(<Pseudo onStart={() => {}} />)
    expect(screen.getByRole('button')).toHaveTextContent(/continuer anonymement/i)
  })

  it('le bouton change quand un pseudo est saisi', () => {
    render(<Pseudo onStart={() => {}} />)
    fireEvent.change(screen.getByRole('textbox'), { target: { value: 'Alice' } })
    expect(screen.getByRole('button')).toHaveTextContent(/bonjour, alice/i)
  })

  it('appelle onStart avec le pseudo saisi', () => {
    const onStart = vi.fn()
    render(<Pseudo onStart={onStart} />)
    fireEvent.change(screen.getByRole('textbox'), { target: { value: 'Alice' } })
    fireEvent.submit(screen.getByRole('textbox').closest('form'))
    expect(onStart).toHaveBeenCalledWith('Alice')
  })

  it('appelle onStart avec "Anonyme" si champ vide', () => {
    const onStart = vi.fn()
    render(<Pseudo onStart={onStart} />)
    fireEvent.submit(screen.getByRole('textbox').closest('form'))
    expect(onStart).toHaveBeenCalledWith('Anonyme')
  })
})
