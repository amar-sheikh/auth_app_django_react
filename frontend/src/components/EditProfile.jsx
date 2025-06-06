import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { API } from '../api'
import { getCookie } from '../helper'
import { useAuth } from '../contexts/AuthContext'
import { Button } from 'react-bootstrap'

const initialState = {
  id: '',
  first_name: '',
  last_name: '',
  username: '',
  email: '',
}

const EditProfile = () => {
  const [formData, setFormData] = useState(initialState)
  const [formErrors, setFormErrors] = useState(initialState)
  const { user, setLoading } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    setFormData({
      ...user
    })
  }, [user])

  const update = async (e) => {
    e.preventDefault();

    setFormErrors(initialState)

    const response = await fetch(API.update, {
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
      navigate('/')
    } else {
      const data = await response.json()

      Object.entries(data.errors).forEach(([key, errors]) => {
        setFormErrors(prevErrors => ({
          ...prevErrors,
          [key]: errors.join(', ')
        }));
      });
    }
  }

  return (
    <div>
      <h1>Edit profile</h1>
      <form onSubmit={update} className='form gap-3'>
      <div className='mx-auto'>
        <div className='form-item'>
            <label htmlFor='first_name'>First name</label>
            <input
              className='form-control'
              name='first_name'
              value={formData.first_name}
              onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
              placeholder='Enter first name' />
          </div>
          <div className='error'>{formErrors.first_name}</div>
        </div>
      <div className='mx-auto'>
        <div className='form-item'>
            <label htmlFor='last_name'>Last name</label>
            <input
              className='form-control'
              name='last_name'
              value={formData.last_name}
              onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
              placeholder='Enter last name' />
          </div>
          <div className='error'>{formErrors.last_name}</div>
        </div>
        <div className='mx-auto'>
          <div className='form-item'>
            <label htmlFor='username'>User name</label>
            <input
              className='form-control'
              name='username'
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              placeholder='Enter username' />
          </div>
          <div className='error'>{formErrors.username}</div>
        </div>
        <div className='mx-auto'>
          <div className='form-item'>
            <label htmlFor='email'>Email</label>
            <input
              className='form-control'
              name='email'
              type='email'
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              placeholder='Enter email address' />
          </div>
          <div className='error'>{formErrors.email}</div>
        </div>
        <div className='form-submit'>
          <Button type='submit'>Update</Button>
        </div>
      </form>
    </div>
  )
}

export default EditProfile