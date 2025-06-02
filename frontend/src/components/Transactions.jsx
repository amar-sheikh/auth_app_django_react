import { useEffect, useState } from 'react';
import { Pagination, Table } from 'react-bootstrap';
import Card from 'react-bootstrap/Card';
import { API } from '../api';
import TransactionFormModal from './TransactionFormModal';

const Transactions = () => {
	const [transactions, setTranscations] = useState({
		count: 0,
		next: null,
		previous: null,
		results: []
	})
	const [currentListUrl, setCurrentListUrl] = useState('')

	useEffect(() => {
		getTranscations()
	}, [currentListUrl])

	const getTranscations = async () => {
		const response = await fetch(`${currentListUrl || API.transactions}`, {
			method: 'GET',
			credentials: 'include'
		})

		if (response.status == 200) {
			setTranscations(await response.json())
		}
	}

	return (
		<>
			<h1>Transcations</h1>
			<div className='m-3 d-flex justify-content-end'>
				<TransactionFormModal onSuccess={getTranscations} />
			</div>
			<Card>
				<Card.Body>
					<Table>
						<thead>
							<tr>
								<th>#</th>
								<th>Address ID</th>
								<th>Idempotency Key</th>
								<th>Amount</th>
								<th>Additional Information</th>
							</tr>
						</thead>
						<tbody>
							{
								transactions.results.map((transaction) => (
									<tr key={transaction.id}>
										<td>{transaction.id}</td>
										<td>{transaction.address}</td>
										<td>{transaction.idempotency_key}</td>
										<td>{transaction.amount}</td>
										<td>{transaction.additional_info ?? ''}</td>
									</tr>
								))
							}
						</tbody>
					</Table>
				</Card.Body>
				{
					transactions.next && transactions.previous && (

						<Card.Footer className='justify-content-around'>
							<Pagination>
								{transactions.previous && <Pagination.Item onClick={() => setCurrentListUrl(transactions.previous)}>Previous</Pagination.Item>}
								{transactions.next && <Pagination.Item onClick={() => setCurrentListUrl(transactions.next)}>Next</Pagination.Item>}
							</Pagination>
						</Card.Footer>
					)
				}
			</Card>
		</>
	)
}

export default Transactions