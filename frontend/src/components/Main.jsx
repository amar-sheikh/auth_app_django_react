import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { API } from '../api'

const Main = () => {
	const [message, setMessage] = useState('Connecting to database...!')
	const navigate = useNavigate()

	useEffect(() => {
		fetch(API.health, {
			method: 'GET'
		})
		.then(response => {
			if (response.status === 200) {
				setTimeout(() => {
					setMessage('Backend connected successfully...!')
					navigate('/login')
				}, 300)
			}
		})
		.catch(() => {
			setMessage('Error connecting backend...!')
		})
	}, [])

	return (
		<div>{message}</div>
	)
}

export default Main