import './App.css'
import { Routes, Route } from 'react-router-dom'
import Login from './components/Login'
import Logout from './components/Logout'
import Main from './components/Main'
import SignUp from './components/SignUp'
import EditProfile from './components/EditProfile'
import View from './components/View'
import ChangePassword from './components/ChangePassword'

function App() {

  return (
    <Routes>
      <Route path='/' element={<Main />} />
      <Route path='/login' element={<Login />} />
      <Route path='/logout' element={<Logout />} />
      <Route path='/signup' element={<SignUp />} />
      <Route path='/view' element={<View />} />
      <Route path='/edit-profile' element={<EditProfile />} />
      <Route path='/change-password' element={<ChangePassword />} />
    </Routes>
  )
}

export default App
