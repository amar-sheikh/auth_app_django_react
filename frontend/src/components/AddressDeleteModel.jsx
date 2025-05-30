import { useState } from 'react'
import DeleteModel from './DeleteModel'
import { API } from '../api'
import { getCookie } from '../helper'

const AddressDeleteModel = ({ onSuccess, address }) => {
	const [error, setError] = useState('')

	const deleteAddress = async () => {
		setError('')

		const response = await fetch(`${API.addresses}/${address.id}/`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken'),
			},
			credentials: 'include'
		})

		if (response.status === 200 || response.status === 204) {
			onSuccess?.()
			return true
		}
		else {
			setFormError('Something went wrong while deleting...')
			return false
		}
	}

	return (
		<DeleteModel title={address.line1 + ' ' + address.line2} onDelete={deleteAddress} >
			{error}
		</DeleteModel>
	)
}

export default AddressDeleteModel