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
					<h1>Update the address...</h1>
				) : (
					<h1>Create a new address...!</h1>
				)
			}
			<AddressFormModal address={address} onSuccess={getAddress} />
		</>
	)
}

export default Main