import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { API } from '../api'

const Main = () => {
	const [message, setMessage] = useState('Connecting to database...!')
	const navigate = useNavigate()

	useEffect(() => {
		const connect = async () => {
			try {
				const response = await await fetch(API.health, {
					method: 'GET'
				})

				if (response.status === 200) {
					setTimeout(() => { 
						setMessage('Backend connected successfully...!')
						navigate('/signup')
					}, 300)
				}
			}
			catch {
				setTimeout(() => setMessage('Error connecting backend...!'), 300)
			}
		}

		connect()
	}, [])

	return (
		<div>{message}</div>
	)
}

export default Main