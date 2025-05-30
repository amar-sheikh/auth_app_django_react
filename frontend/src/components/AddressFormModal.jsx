import { useEffect, useState } from 'react'
import FormModel from './FormModel'
import { API } from '../api'
import { getCookie } from '../helper'
import { useAuth } from '../contexts/AuthContext'

const initialState = {
	user: '',
	transaction: '',
	line1: '',
	line2: '',
	country: '',
	city: '',
	postcode: '',
}

const AddressFormModal = ({ onSuccess, address = null }) => {
	const [formData, setFormData] = useState(initialState)
	const [formErrors, setFormErrors] = useState(initialState)
	const [transactions, setTransactions] = useState({
		count: 0,
		next: null,
		previous: null,
		results: []
	})
	const { user } = useAuth()

	useEffect(() => {
		const getTransactions = async () => {
			const response = await fetch(`${API.transactions}/without_address`, {
				method: 'GET',
				credentials: 'include'
			})

			if (response.status == 200) {
				setTransactions(await response.json())
			}
			else {
				setError('Error fetching data...!')
			}
		}

		setFormData(address ?? {
			user: user.id,
			transaction: '',
			line1: '',
			line2: '',
			country: '',
			city: '',
			postcode: '',
		})

		getTransactions()
	}, [address])

	const onSubmit = async () => {
		setFormErrors(initialState)

		let response

		if (address) {
			response = await fetch(`${API.addresses}/${address.id}/`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': getCookie('csrftoken'),
				},
				body: JSON.stringify(formData),
				credentials: 'include'
			})
		}
		else {
			response = await fetch(`${API.addresses}/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': getCookie('csrftoken'),
				},
				body: JSON.stringify(formData),
				credentials: 'include'
			})
		}

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
		<FormModel edit={!!address} title='address' onSubmit={onSubmit}>
			<>
				<input
					name='user'
					type='hidden'
					value={formData.user} />
				<div>
					<div className='form-item'>
						<label htmlFor='line1'>Line 1</label>
						<input
							className='form-control'
							name='line1'
							value={formData.line1}
							onChange={(e) => setFormData({ ...formData, line1: e.target.value })}
							placeholder='Enter address line 1' />
					</div>
					<div className='error'>{formErrors.line1}</div>
				</div>
				<div>
					<div className='form-item'>
						<label htmlFor='line2'>Line 2</label>
						<input
							className='form-control'
							name='line2'
							value={formData.line2}
							onChange={(e) => setFormData({ ...formData, line2: e.target.value })}
							placeholder='Enter address line 2' />
					</div>
					<div className='error'>{formErrors.line2}</div>
				</div>
				<div>
					<div className='form-item'>
						<label htmlFor='country'>country</label>
						<input
							className='form-control'
							name='country'
							value={formData.country}
							onChange={(e) => setFormData({ ...formData, country: e.target.value })}
							placeholder='Enter country' />
					</div>
					<div className='error'>{formErrors.country}</div>
				</div>
				<div>
					<div className='form-item'>
						<label htmlFor='city'>city</label>
						<input
							className='form-control'
							name='city'
							value={formData.city}
							onChange={(e) => setFormData({ ...formData, city: e.target.value })}
							placeholder='Enter city' />
					</div>
					<div className='error'>{formErrors.city}</div>
				</div>
				<div>
					<div className='form-item'>
						<label htmlFor='postcode'>Postal Code</label>
						<input
							className='form-control'
							name='postcode'
							value={formData.postcode}
							onChange={(e) => setFormData({ ...formData, postcode: e.target.value })}
							placeholder='Enter postcode' />
					</div>
					<div className='error'>{formErrors.postcode}</div>
				</div>
				<div>
					<div className='form-item'>
						<label htmlFor='transaction'>Transaction</label>
						<select
							className='form-control'
							name='transaction'
							onChange={(e) => setFormData({ ...formData, transaction: e.target.value })}
						>
							<option value=''>select</option>
							{
								transactions.results.map((transaction) => (
									<option
										value={transaction.id}
										key={transaction.id}

									>{transaction.idempotency_key}</option>
								))
							}
						</select>
					</div>
					<div className='error'>{formErrors.postcode}</div>
				</div>
			</>
		</FormModel>
	)
}

export default AddressFormModal