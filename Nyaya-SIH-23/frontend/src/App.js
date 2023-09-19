import React, { createContext, useEffect, useState } from 'react';
import "./App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { LoginPage, Profile } from "./Routes.js";
import { HomePage } from "./Routes.js";
import { SignupPage } from "./Routes.js";
import { LawyerSignup } from './Routes.js'
import { LawyerLogin } from './Routes.js';
import { Appointment } from './Routes.js';
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import LawyerProfile from './components/Profile/LawyerProfile';
import Personal_Family from './components/FliterPages/Personal_Family';
import axios from 'axios';
import UserProfile from './pages/UserProfile';
import { useDispatch, useSelector } from 'react-redux';
import { loadUser } from './redux/actions/user';
import ProtectedRoute from './ProtectedRoute';

export const DataContext = createContext()
const App = () => {

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    setLoading(true)
    axios
      .get("http://localhost:8000/admin/getall")
      .then((response) => {
        // setVal(response.data.people); // Update val using setVal
        setData(response.data.people);
        setLoading(false)
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setLoading(false)
      });
  }, []);

  const dispatch = useDispatch();

  const { userloading,isAuthenticated, error, message, user } = useSelector(state => state.user)

  useEffect(() => {
    if (error) {
      toast.error(error);
      dispatch({ type: "clearError" });
    }
    if (message) {
      toast.success(message);
      dispatch({ type: "clearMessage" });
    }
  }, [dispatch, message, error])

  useEffect(() => {
    dispatch(loadUser());
  }, [dispatch])

  return (
    <>
      {
        loading || userloading ? <div>
          Loading...
        </div> : <DataContext.Provider value={{ data, setData }}>
          <BrowserRouter>
            <Routes>
              <Route path='/' element={<HomePage />} />
              {/* <Route path='/login' element={<LoginPage />} />
              <Route path='/signup' element={<SignupPage />} /> */}
              <Route path='/admin/signup' element={<LawyerSignup />} />
              <Route path='/admin/login' element={<LawyerLogin />} />
              <Route path='/admin/me' element={<Profile />} />
              <Route path='/admin/profile/:id' element={<LawyerProfile />} />
              <Route path='/admin/profile/appointment/:id' element={<Appointment />} />
              <Route path='/products/personal/ family' element={<Personal_Family filter={'family'} />} />
              <Route path='/products/criminal' element={<Personal_Family filter={'criminal'} />} />
              <Route path='/products/civil' element={<Personal_Family filter={'civil'} />} />
              <Route path='/products/corporate' element={<Personal_Family filter={'corporate'} />} />
              <Route path='/products/ property' element={<Personal_Family filter={'property'} />} />
              <Route path='/products/debt' element={<Personal_Family filter={'debt'} />} />
              <Route path='/products/immigration' element={<Personal_Family filter={'immigration'} />} />
              <Route path='/products/international court' element={<Personal_Family filter={'international court'} />} />
              <Route path='/products/insurance' element={<Personal_Family filter={'insurance'} />} />
              <Route path='/products/others' element={<Personal_Family filter={'others'} />} />


              <Route path='/' element={<HomePage />} />
              <Route path='/login' element={
                isAuthenticated ? <Navigate to={'/'} /> : <LoginPage />
              } />
              <Route path='/signup' element={
                isAuthenticated ? <Navigate to={'/'} /> : <SignupPage />
              } />
              <Route path='/user-profile' element={
                <ProtectedRoute>
                  <UserProfile user={user} />
                </ProtectedRoute>} />

            </Routes>
            <ToastContainer
              position="bottom-center"
              autoClose={5000}
              hideProgressBar={false}
              newestOnTop={false}
              closeOnClick
              rtl={false}
              pauseOnFocusLoss
              draggable
              pauseOnHover
              theme="dark"
            />
          </BrowserRouter>
        </DataContext.Provider>
      }
    </>
  )
}

export default App