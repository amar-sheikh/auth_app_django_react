import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { API } from '../api'
import { getCookie } from '../helper'
import { useAuth } from '../contexts/AuthContext'

const Logout = () => {
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const { user, setUser, setLoading } = useAuth()

  const logout = async (e) => {
    setError('')

    const response = await fetch(API.logout, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      credentials: 'include'
    })

    if (response.status === 200) {
      setLoading(true)
      setUser(null)
      navigate('/login')
    }
    else {
      const data = await response.json()
      setError(data.message)
    }
  }

  return (
    <div>
      {
        user ? (
          <>
            <div className='error'>{error}</div>
            <h2>Hi {user.username} - Are you sure you want to logout?</h2>
            <button onClick={logout}>Logout</button>
            <button onClick={()=> navigate(-1)}>Go to back</button>
          </>
        ): (
          <div>Loading....</div>
        )
      }
    </div>
  )
}

export default Logout