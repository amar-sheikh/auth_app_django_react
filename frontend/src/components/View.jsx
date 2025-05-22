import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { API } from '../api'
import { getCookie } from '../helper'
import { useAuth } from '../contexts/AuthContext'

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