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

function App() {

  return (
    <Routes>
      <Route path='/' element={<Main />} />
      <Route path='/login' element={<Login />} />
      <Route path='/signup' element={<SignUp />} />

      <Route element={<ProtectedRoute />}>
        <Route path='/logout' element={<Logout />} />
        <Route path='/view' element={<View />} />
        <Route path='/edit-profile' element={<EditProfile />} />
        <Route path='/change-password' element={<ChangePassword />} />
      </Route>
    </Routes>
  )
}

export default App
