import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('Loading...')

  useEffect(() => {
    fetch('http://localhost:5000/api')  // Change the endpoint if needed
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((err) => setMessage('Error fetching data'))
  }, [])

  return (
    <div>
      <h1>Flask + React App</h1>
      <p>{message}</p>
    </div>
  )
}

export default App
