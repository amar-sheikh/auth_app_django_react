import './App.css'
import { Routes, Route } from 'react-router-dom'
import Login from './components/Login'
import Logout from './components/Logout'
import Main from './components/Main'
import SignUp from './components/SignUp'
import EditProfile from './components/EditProfile'
import View from './components/View'
import ChangePassword from './components/ChangePassword'
import ProtectedRoute from './components/ProtectedRoute'
import ForgetPassword from './components/ForgetPassword'
import ResetPassword from './components/ResetPassword'
import NonProtectedRoute from './components/NonProtectedRoute'
import NotFound from './components/NotFound'
import ConnectBackend from './components/ConnectBackend'

function App() {

  return (
    <Routes>
      <Route element={<NonProtectedRoute />} >
        <Route path='/login' element={<Login />} />
        <Route path='/signup' element={<SignUp />} />
        <Route path='/forget-password' element={<ForgetPassword />} />
        <Route path='/reset-password/:uid/:token' element={<ResetPassword />} />
      </Route>

      <Route element={<ProtectedRoute />}>
        <Route path='/' element={<Main />} />
        <Route path='/logout' element={<Logout />} />
        <Route path='/view' element={<View />} />
        <Route path='/edit-profile' element={<EditProfile />} />
        <Route path='/change-password' element={<ChangePassword />} />
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}

export default App
