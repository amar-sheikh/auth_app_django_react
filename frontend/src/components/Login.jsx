import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { API } from '../api'
import { getCookie } from '../helper'
import { useAuth } from '../contexts/AuthContext'

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  })
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const { setLoading } = useAuth()

  const login = async (e) => {
    e.preventDefault();

    setError('')

    const response = await fetch(API.login, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify(formData),
      credentials: 'include'
    })

    if (response.status === 200) {
      setLoading(true)
      navigate('/view')
    }
    else {
      const data = await response.json()
      setError(data.error)
    }
  }

  return (
    <div>
      <h1>Login your account</h1>
      <form onSubmit={login} className='form'>
        <div className='error'>{error}</div>
        <div>
          <div className='form-item'>
            <label htmlFor='username'>User name</label>
            <input
              name='username'
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              placeholder='Enter username' />
          </div>
        </div>
        <div>
          <div className='form-item'>
            <label htmlFor='password'>Password</label>
            <input
              name='password'
              type='password'
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              placeholder='Enter password' />
          </div>
        </div>
        <div className='form-submit'>
          <button type='submit'>Login</button>
        </div>
      </form>
      <div><Link to='/forget-password' >Forget password?</Link></div>
      <div>
        Don't have account? <Link to='/signup'>Sign Up</Link>
      </div>
    </div>
  )
}

export default Login