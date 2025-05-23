import { Outlet, Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const ProtectedRoute = () => {
  const { user } = useAuth()

  if (user) {
    return <Outlet />
  } else {
    return <Navigate to='/login' />
  }
}

export default ProtectedRoute