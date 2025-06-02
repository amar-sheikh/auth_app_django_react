import { useEffect, useState } from 'react'
import { Alert } from 'react-bootstrap'
import { API } from '../api'
import AddressFormModal from './AddressFormModal'

const Main = () => {
	const [address, setAddress] = useState(null)
	const [error, setError] = useState('')

	useEffect(() => {
		getAddress()
	}, [])

	const getAddress = async () => {
		const response = await fetch(`${API.addresses}/current_address`, {
			method: 'GET',
			credentials: 'include'
		})

		if (response.status == 200) {
			const data = await response.json()
			setAddress(data.current_address)
		}
		else {
			setError('Error fetching data...!')
		}
	}

	return (
		<>
			{error && <Alert variant='danger'>{error} </Alert>}
			{
				address ? (
					<>
						<h1>Update the address...</h1>
						<div className='d-flex flex-column mb-3'>
							<div className='mb-3'>line 1: <strong>{address.line1}</strong></div>
							<div className='mb-3'>line 2: <strong>{address.line2}</strong></div>
							<div className='mb-3'>City: <strong>{address.city}</strong></div>
							<div className='mb-3'>Country: <strong>{address.country}</strong></div>
							<div className='mb-3'>Postal Code: <strong>{address.postcode}</strong></div>
							<div className='mb-3'>Updated at: <strong>{address.updated_at}</strong></div>
							<div className='mb-3'>Created at: <strong>{address.created_at}</strong></div>
						</div>
					</>
				) : (
					<h1>Create a new address...!</h1>
				)
			}
			<AddressFormModal address={address} onSuccess={getAddress} />
		</>
	)
}

export default Main