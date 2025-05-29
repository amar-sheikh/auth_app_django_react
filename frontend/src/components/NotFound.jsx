import { useNavigate } from 'react-router-dom'

const NotFound = () => {
	const navigate = useNavigate()
	return (
		<div>
			<h1>Page not found</h1>
			<button onClick={() => navigate(-1)}>Go to back</button>
		</div>
	)
}

export default NotFound