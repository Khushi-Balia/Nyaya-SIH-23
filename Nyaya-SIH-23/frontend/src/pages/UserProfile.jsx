import React from 'react'
import UserProf from '../components/Profile/User'

function UserProfile({user}) {
  return (
    <div>
      <UserProf user={user} />
    </div>
  )
}

export default UserProfile