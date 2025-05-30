import { Outlet, Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import Layout from './Layout'

const ProtectedRoute = () => {
  const { user } = useAuth()

  if (user) {
    return <Layout><Outlet /></Layout>
  } else {
    return <Navigate to='/login' />
  }
}

export default ProtectedRoute