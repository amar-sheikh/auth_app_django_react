import { Link } from 'react-router-dom'

const View = () => {
  return (
    <div>
      <hr />
      <Link to='/logout'>Logout</Link>
      <hr />
      <Link to='/edit-profile'>Edit Profile</Link>
      <hr />
      <Link to='/change-password'>Change Password</Link>
    </div>
  )
}

export default View