import { useEffect, useState } from 'react'
import Loading from './screens/Loading'
import Welcome from './screens/Welcome'
import Pseudo from './screens/Pseudo'
import Chat from './screens/Chat'
import { WATER_LITERS_PER_REQUEST } from './utils/water'
import './styles/global.css'

const SCREENS = { LOADING: 'loading', WELCOME: 'welcome', PSEUDO: 'pseudo', CHAT: 'chat' }

const initialScreen = () => {
  if (import.meta.env.DEV) {
    const forced = new URLSearchParams(window.location.search).get('screen')
    if (Object.values(SCREENS).includes(forced)) return forced
  }
  return SCREENS.LOADING
}

export default function App() {
  const [screen, setScreen] = useState(initialScreen)
  const [pseudo, setPseudo] = useState('Anonyme')
  const [waterLiters, setWaterLiters] = useState(0)

  useEffect(() => {
    fetch('/api/water-stats')
      .then((res) => res.json())
      .then((data) => setWaterLiters(data.liters))
      .catch(() => {})
  }, [])

  const registerWaterUsage = () => setWaterLiters((liters) => liters + WATER_LITERS_PER_REQUEST)

  const handleConsent = () => setScreen(SCREENS.PSEUDO)

  const handleStart = (name) => {
    setPseudo(name)
    setScreen(SCREENS.CHAT)
  }

  const handleEnd = () => {
    setPseudo('Anonyme')
    setScreen(SCREENS.WELCOME)
  }

  if (screen === SCREENS.LOADING) return <Loading onReady={() => setScreen(SCREENS.WELCOME)} />
  if (screen === SCREENS.WELCOME) return <Welcome onConsent={handleConsent} waterLiters={waterLiters} />
  if (screen === SCREENS.PSEUDO) return <Pseudo onStart={handleStart} />
  if (screen === SCREENS.CHAT) {
    return (
      <Chat
        pseudo={pseudo}
        onEnd={handleEnd}
        waterLiters={waterLiters}
        onMessageSent={registerWaterUsage}
      />
    )
  }
}
