import { Outlet, Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const NonProtectedRoute = () => {
  const { user, loading } = useAuth()

  if (loading) { return <div>Loading...!</div> }
  if (user) { return <Navigate to='/' /> }

  return <Outlet />
}

export default NonProtectedRoute