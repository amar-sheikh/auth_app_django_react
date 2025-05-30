import { useEffect, useState } from 'react';
import { Pagination, Table } from 'react-bootstrap';
import Card from 'react-bootstrap/Card';
import { API } from '../api';
import AddressFormModal from './AddressFormModal';
import AddressDeleteModel from './AddressDeleteModel';

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
			<div className='m-3 d-flex justify-content-end'>
				<AddressFormModal onSuccess={() => getAddresses()} />
			</div>
			<Card>
				<Card.Body>
					<Table>
						<thead>
							<tr>
								<th>#</th>
								<th>address</th>
								<th>postal code</th>
								<th>country</th>
								<th>actions</th>
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
										<td>
											<div className='d-flex gap-2'>
												<AddressFormModal address={address} onSuccess={() => getAddresses()} />
												<AddressDeleteModel address={address} onSuccess={() => getAddresses()} />
											</div>
										</td>
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