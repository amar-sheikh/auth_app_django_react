import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { API } from '../api'
import { getCookie } from '../helper'
import { useAuth } from '../contexts/AuthContext'

const initialState = {
	old_password: '',
	new_password1: '',
	new_password2: '',
}

const ChangePassword = () => {
	const [formData, setFormData] = useState(initialState)
	const [formErrors, setFormErrors] = useState(initialState)
	const { setLoading } = useAuth()
	const navigate = useNavigate()

	const updatePassword = async (e) => {
		e.preventDefault();

		setFormErrors(initialState)

		const response = await fetch(API.update_password, {
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
			<h1>Change password</h1>
			<form onSubmit={updatePassword} className='form'>
				<div>
					<div className='form-item'>
						<label htmlFor='old_password'>Old password</label>
						<input
							name='old_password'
							type='password'
							value={formData.old_password}
							onChange={(e) => setFormData({ ...formData, old_password: e.target.value })}
							placeholder='Enter old password' />
					</div>
					<div className='error'>{formErrors.old_password}</div>
				</div>
				<div>
					<div className='form-item'>
						<label htmlFor='new_password1'>New Password</label>
						<input
							name='new_password1'
							type='password'
							value={formData.new_password1}
							onChange={(e) => setFormData({ ...formData, new_password1: e.target.value })}
							placeholder='Enter new password' />
					</div>
					<div className='error'>{formErrors.new_password1}</div>
				</div>
				<div>
					<div className='form-item'>
						<label htmlFor='new_password2'>Confirm password</label>
						<input
							name='new_password2'
							type='password'
							value={formData.new_password2}
							onChange={(e) => setFormData({ ...formData, new_password2: e.target.value })}
							placeholder='Enter confrim password' />
					</div>
					<div className='error'>{formErrors.new_password2}</div>
				</div>
				<div className='form-submit'>
					<button type='submit'>Update</button>
				</div>
			</form>
		</div>
	)
}

export default ChangePassword