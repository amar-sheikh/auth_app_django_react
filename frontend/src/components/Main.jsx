import { useEffect, useState } from 'react'
import { Card, Row, Col, Alert } from 'react-bootstrap'
import { API } from '../api'
import { Link } from 'react-router-dom'

const Main = () => {
	const [addressCount, setAddressCount] = useState(0)
	const [transactionCount, setTransactionCount] = useState(0)
	const [error, setError] = useState('')

	useEffect(() => {
		const getAddressCount = async () => {
			const response = await fetch(`${API.addresses}/non_transaction_count`, {
				method: 'GET',
				credentials: 'include'
			})

			if (response.status == 200) {
				const data = await response.json()
				setAddressCount(data.count)
			}
			else {
				setError('Error fetching data...!')
			}
		}

		const getTransactionCount = async () => {
			const response = await fetch(`${API.transactions}/count`, {
				method: 'GET',
				credentials: 'include'
			})

			if (response.status == 200) {
				const data = await response.json()
				setTransactionCount(data.count)
			}
			else {
				setError('Error fetching data...!')
			}
		}

		getAddressCount()
		getTransactionCount()
	}, [])

	return (
		<>
			<h1>Dashboard</h1>
			{error && <Alert variant='danger'>{error} </Alert>}
			<Row>
				<Col>
					<Card>
						<Card.Body>You have <strong>{addressCount}</strong> address not linked to transaction.</Card.Body>
						<Card.Footer className='d-flex justify-content-end'><Link to='addresses'>See...</Link></Card.Footer>
					</Card>
				</Col>
				<Col>
					<Card>
						<Card.Body>You have made <strong>{transactionCount}</strong> transactions.</Card.Body>
						<Card.Footer className='d-flex justify-content-end'><Link to='addresses'>See...</Link></Card.Footer>
					</Card>
				</Col>
			</Row>
		</>
	)
}

export default Main