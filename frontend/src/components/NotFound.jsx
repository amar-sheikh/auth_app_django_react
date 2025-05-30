import { Button } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'

const NotFound = () => {
	const navigate = useNavigate()
	return (
		<div>
			<h1>Page not found</h1>
			<Button onClick={() => navigate(-1)}>Go to back</Button>
		</div>
	)
}

export default NotFound