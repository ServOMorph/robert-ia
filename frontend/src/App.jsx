import { useState } from 'react'
import Welcome from './screens/Welcome'
import Pseudo from './screens/Pseudo'
import Chat from './screens/Chat'
import './styles/global.css'

const SCREENS = { WELCOME: 'welcome', PSEUDO: 'pseudo', CHAT: 'chat' }

export default function App() {
  const [screen, setScreen] = useState(SCREENS.WELCOME)
  const [pseudo, setPseudo] = useState('Anonyme')

  const handleConsent = () => setScreen(SCREENS.PSEUDO)

  const handleStart = (name) => {
    setPseudo(name)
    setScreen(SCREENS.CHAT)
  }

  const handleEnd = () => {
    setPseudo('Anonyme')
    setScreen(SCREENS.WELCOME)
  }

  if (screen === SCREENS.WELCOME) return <Welcome onConsent={handleConsent} />
  if (screen === SCREENS.PSEUDO) return <Pseudo onStart={handleStart} />
  if (screen === SCREENS.CHAT) return <Chat pseudo={pseudo} onEnd={handleEnd} />
}
