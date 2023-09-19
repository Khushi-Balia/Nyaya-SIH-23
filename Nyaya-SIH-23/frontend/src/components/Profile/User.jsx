import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import Header from '../Layout/Header'
import { TbEdit } from 'react-icons/tb';
import { logoutUser } from '../../redux/actions/user';

function UserProf({user}) {
    const [name, setName] = useState(user && user.name);
    const [email, setEmail] = useState(user && user.email);

    
    const dispatch=useDispatch();
    function handleLogout() {
        dispatch(logoutUser());
    }
    return (
        <>
            <Header />
            <div className='h-full flex justify-center items-center my-4'>
                <div class="flex flex-col justify-center border p-6 shadow-xl rounded-xl sm:px-12 ">
                    <img src="https://source.unsplash.com/150x150/?portrait?3" alt="" class="w-32 h-32 mx-auto rounded-full dark:bg-gray-500 aspect-square" />
                    <div class="space-y-4 text-center divide-y divide-gray-700">
                        <div class="my-2 space-y-1">
                            <div className='flex items-center justify-center gap-2'>
                                <h2 class="text-xl font-semibold sm:text-2xl">{name}</h2> <TbEdit className='cursor-pointer mt-1' />
                            </div>
                            <p class="px-5 text-xs sm:text-base">{email}</p>
                        </div>
                    </div>
                    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full my-4" onClick={handleLogout}>
                        Logout
                    </button>
                    {/* <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full">
                        Update Password
                    </button> */}
                </div>
            </div>
        </>
    )
}
export default UserProf