import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { API } from '../api'
import { getCookie } from '../helper'
import { useAuth } from '../contexts/AuthContext'
import { Button } from 'react-bootstrap'

const initialState = {
	uid: '',
	token: '',
	new_password1: '',
	new_password2: '',
}

const ResetPassword = () => {
	const [formData, setFormData] = useState(initialState)
	const [formErrors, setFormErrors] = useState(initialState)
	const { setLoading } = useAuth()
	const navigate = useNavigate()
	const params = useParams()

	useEffect(() => {
		setFormData({
			...formData,
			uid: params.uid,
			token: params.token
		})
	}, [params])

	const resetPassword = async (e) => {
		e.preventDefault();

		setFormErrors(initialState)

		const response = await fetch(API.reset_password, {
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
			navigate('/login')
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
		<div className='m-5'>
			<div className='d-flex justify-content-center'>
				<Button onClick={() => navigate(-1)}>Go to back</Button>
			</div>
			<hr />
			<h1>Reset password</h1>
			<form onSubmit={resetPassword} className='form gap-3'>
				<input
					name='uid'
					type='hidden'
					value={formData.uid} />
				<input
					name='token'
					type='hidden'
					value={formData.uid} />
				<div className='mx-auto'>
					<div className='form-item'>
						<label htmlFor='new_password1'>New Password</label>
						<input
							className='form-control'
							name='new_password1'
							type='password'
							value={formData.new_password1}
							onChange={(e) => setFormData({ ...formData, new_password1: e.target.value })}
							placeholder='Enter new password' />
					</div>
					<div className='error'>{formErrors.new_password1}</div>
				</div>
				<div className='mx-auto'>
					<div className='form-item'>
						<label htmlFor='new_password2'>Confirm password</label>
						<input
							className='form-control'
							name='new_password2'
							type='password'
							value={formData.new_password2}
							onChange={(e) => setFormData({ ...formData, new_password2: e.target.value })}
							placeholder='Enter confrim password' />
					</div>
					<div className='error'>{formErrors.new_password2}</div>
				</div>
				<div className='form-submit'>
					<Button type='submit'>Set Password</Button>
				</div>
			</form>
		</div>
	)
}

export default ResetPassword