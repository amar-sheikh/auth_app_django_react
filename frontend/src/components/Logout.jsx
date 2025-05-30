import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { API } from '../api'
import { getCookie } from '../helper'
import { useAuth } from '../contexts/AuthContext'
import { Button } from 'react-bootstrap'

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
      setError('Something went wrong while logging out...!')
    }
  }

  const logoutFromAllDevices = async (e) => {
    setError('')
    const response = await fetch(API.logout_from_all_devices, {
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
            <h1>Logout</h1>
            <div className='error'>{error}</div>
            <h3 className='text-center text-secondary'>Do you want to logout or logged out from all devices?</h3>
            <div className='d-flex justify-content-around'>
              <Button variant='danger' onClick={logout}>Logout</Button>
              <Button variant='warning' onClick={logoutFromAllDevices}>Logout from all devices</Button>
            </div>
          </>
        ) : (
          <div>Loading....</div>
        )
      }
    </div>
  )
}

export default Logout