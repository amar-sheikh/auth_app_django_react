import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('Connecting to database...!')

  useEffect(()=>{
    const connect = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/health', {
          method: 'GET'
        })

        if (response.status === 200) {
          setTimeout(()=> setMessage('Backend connected successfully...!'), 300)
        }
      }
      catch {
        setTimeout(()=> setMessage('Error connecting backend...!'), 300)
      }
    }

    connect()
  },[])

  return (
    <div>{message}</div>
  )
}

export default App
