import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { API } from '../api'
import { getCookie } from '../helper'

const ForgetPassword = () => {
	const [username, setUsername] = useState('')
	const [error, setError] = useState('')
	const [success, setSuccess] = useState(false)
	const navigate = useNavigate()

	const sendResetPasswordMail = async (e) => {
		e.preventDefault();

		setError('')
		setSuccess(false)

		const response = await fetch(API.send_password_reset_email, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken'),
			},
			body: JSON.stringify({
				'username': username,
				'redirect': '/reset-password'
			}),
			credentials: 'include'
		})

		if (response.status === 200) {
			setSuccess(true)
		} else {
			const data = await response.json()
			setError(data.message)
		}
	}

	return (
		<div>
			<hr />
			<button onClick={() => navigate(-1)}>Go to back</button>
			<hr />
			<h1>Forget password</h1>
			<form onSubmit={sendResetPasswordMail} className='form'>
				<div className='error'>{error}</div>
				<div>
					<div className='form-item'>
						<label htmlFor='username'>Username</label>
						<input
							name='username'
							value={username}
							onChange={(e) => setUsername(e.target.value)}
							placeholder='Enter username ...' />
					</div>
				</div>
				<div className='form-submit'>
					<button type='submit'>Send mail</button>
				</div>
			</form>
			{success && <div>The password reset email send to you mail. You can reset your password now.</div>}
		</div>
	)
}

export default ForgetPassword