import { useEffect, useState } from 'react'
import FormModel from './FormModel'
import { API } from '../api'
import { getCookie } from '../helper'
import { useAuth } from '../contexts/AuthContext'

const initialState = {
	idempotency_key: '',
	amount: '',
	additional_info: ''
}

const TransactionFormModal = ({ onSuccess }) => {
	const [formData, setFormData] = useState(initialState)
	const [formErrors, setFormErrors] = useState(initialState)
	const { user } = useAuth()

	useEffect(() => {
		setFormData(initialState)
	}, [])

	const onSubmit = async () => {
		const formDataWithUser = { ...formData, user: user.id };
		setFormErrors(initialState)

		const response = await fetch(`${API.transactions}/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken'),
			},
			body: JSON.stringify(formDataWithUser),
			credentials: 'include'
		})

		if (response.status === 200 || response.status === 201) {
			onSuccess?.()

			if (response.status === 201) {
				setFormData(initialState)
			}

			return true
		}
		else {
			const data = await response.json()

			Object.entries(data).forEach(([key, errors]) => {
				setFormErrors(prevErrors => ({
					...prevErrors,
					[key]: errors.join(', ')
				}));
			});
			return false
		}
	}

	return (
		<FormModel title='transcation' onSubmit={onSubmit}>
			<>
				<input
					name='user'
					type='hidden'
					value={user.id} />
				<div>
					<div className='form-item'>
						<label htmlFor='idempotency_key'>Key</label>
						<input
							className='form-control'
							name='idempotency_key'
							value={formData.idempotency_key}
							disabled
							onChange={(e) => setFormData({ ...formData, idempotency_key: e.target.value })}
							placeholder='Will be generated by the system' />
					</div>
					<div className='error'>{formErrors.idempotency_key}</div>
				</div>
				<div>
					<div className='form-item'>
						<label htmlFor='amount'>Amount</label>
						<input
							className='form-control'
							name='amount'
							value={formData.amount}
							onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
							placeholder='Enter amount' />
					</div>
					<div className='error'>{formErrors.amount}</div>
				</div>
				<div>
					<div className='form-item'>
						<label htmlFor='additional_info'>Additional Info</label>
						<textarea
							className='form-control'
							name='additional_info'
							value={formData.additional_info}
							onChange={(e) => setFormData({ ...formData, additional_info: e.target.value })}
							placeholder='Enter additional info' />
					</div>
					<div className='error'>{formErrors.additional_info}</div>
				</div>
			</>
		</FormModel>
	)
}

export default TransactionFormModal