import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { API } from '../api'
import { getCookie } from '../helper'
import { useAuth } from '../contexts/AuthContext'

const initialState = {
  id: '',
  first_name: '',
  last_name: '',
  username: '',
  email: '',
  date_joined: ''
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
      navigate('/view')
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
      <hr />
      <button onClick={() => navigate(-1)}>Go to back</button>
      <hr />
      <h1>Edit profile</h1>
      <form onSubmit={update} className='form'>
        <input
          name='first_name'
          type='hidden'
          value={formData.date_joined} />
        <div>
          <div className='form-item'>
            <label htmlFor='first_name'>First name</label>
            <input
              name='first_name'
              value={formData.first_name}
              onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
              placeholder='Enter first name' />
          </div>
          <div className='error'>{formErrors.first_name}</div>
        </div>
        <div>
          <div className='form-item'>
            <label htmlFor='last_name'>Last name</label>
            <input
              name='last_name'
              value={formData.last_name}
              onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
              placeholder='Enter last name' />
          </div>
          <div className='error'>{formErrors.last_name}</div>
        </div>
        <div>
          <div className='form-item'>
            <label htmlFor='username'>User name</label>
            <input
              name='username'
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              placeholder='Enter username' />
            <span>This name will be used for login</span>
          </div>
          <div className='error'>{formErrors.username}</div>
        </div>
        <div>
          <div className='form-item'>
            <label htmlFor='email'>Email</label>
            <input
              name='email'
              type='email'
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              placeholder='Enter email address' />
          </div>
          <div className='error'>{formErrors.email}</div>
        </div>
        <div className='form-item'>
          <button type='submit'>Update</button>
        </div>
      </form>
    </div>
  )
}

export default EditProfile