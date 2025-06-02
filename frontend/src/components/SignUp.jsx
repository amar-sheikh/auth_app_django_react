import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { API } from '../api'
import { getCookie } from '../helper'
import { Button } from 'react-bootstrap'

const initialState = {
  first_name: '',
  last_name: '',
  username: '',
  email: '',
  password1: '',
  password2: '',
}

const SignUp = () => {
  const [formData, setFormData] = useState(initialState)
  const [formErrors, setFormErrors] = useState(initialState)
  const navigate = useNavigate()

  const register = async (e) => {
    e.preventDefault();

    setFormErrors(initialState)

    const response = await fetch(API.register, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify(formData),
      credentials: 'include'
    })

    if (response.status === 201) {
      navigate('/login')
    }
    else {
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
    <div className='my-4'>
      <h1>Register an account</h1>
      <form onSubmit={register} className='form gap-3'>
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
        <div className='mx-auto'>
          <div className='form-item'>
            <label htmlFor='password1'>Password</label>
            <input
              className='form-control'
              name='password1'
              type='password'
              value={formData.password1}
              onChange={(e) => setFormData({ ...formData, password1: e.target.value })}
              placeholder='Enter password' />
          </div>
          <div className='error'>{formErrors.password1}</div>
        </div>
        <div className='mx-auto'>
          <div className='form-item'>
            <label htmlFor='password2'>Confirm password</label>
            <input
              className='form-control'
              name='password2'
              type='password'
              value={formData.password2}
              onChange={(e) => setFormData({ ...formData, password2: e.target.value })}
              placeholder='Enter confrim password' />
          </div>
          <div className='error'>{formErrors.password2}</div>
        </div>
        <div className='mx-auto form-submit'>
          <Button type='submit'>Sign Up</Button>
        </div>
      </form>
      <div className='d-flex justify-content-center'>
        <div>
          Already have account? <Link to='/login'>Login</Link>
        </div>
      </div>
    </div>
  )
}

export default SignUp