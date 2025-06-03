import { useEffect, useState } from 'react';
import { Pagination, Table } from 'react-bootstrap';
import Card from 'react-bootstrap/Card';
import { API } from '../api';

const Addresses = () => {
	const [addresses, setAddresses] = useState({
		count: 0,
		next: null,
		previous: null,
		results: []
	})
	const [currentListUrl, setCurrentListUrl] = useState('')

	useEffect(() => {
		getAddresses()
	}, [currentListUrl])

	const getAddresses = async () => {
		const response = await fetch(`${currentListUrl || API.addresses}`, {
			method: 'GET',
			credentials: 'include'
		})

		if (response.status == 200) {
			setAddresses(await response.json())
		}
	}

	return (
		<>
			<h1>Addresses</h1>
			<Card>
				<Card.Body>
					<Table>
						<thead>
							<tr>
								<th>#</th>
								<th>address</th>
								<th>postal code</th>
								<th>country</th>
							</tr>
						</thead>
						<tbody>
							{
								addresses.results.map((address) => (
									<tr key={address.id}>
										<td>{address.id}</td>
										<td>{address.line1 + ' ' + address.line2}</td>
										<td>{address.postcode}</td>
										<td>{address.country ?? ''}</td>
									</tr>
								))
							}
						</tbody>
					</Table>
				</Card.Body>
				{
					addresses.next && addresses.previous && (

						<Card.Footer className='justify-content-around'>
							<Pagination>
								{addresses.previous && <Pagination.Item onClick={() => setCurrentListUrl(addresses.previous)}>Previous</Pagination.Item>}
								{addresses.next && <Pagination.Item onClick={() => setCurrentListUrl(addresses.next)}>Next</Pagination.Item>}
							</Pagination>
						</Card.Footer>
					)
				}
			</Card>
		</>
	)
}

export default Addresses