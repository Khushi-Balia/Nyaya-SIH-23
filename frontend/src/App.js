import React from 'react';
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LoginPage } from "./Routes.js";
import { SignupPage } from "./Routes.js";

const App = () => {
  return (
    <BrowserRouter>
    <Routes>
      <Route path='/login' element={<LoginPage/>} />
      <Route path='/signup' element={<SignupPage/>} />
    </Routes>
    </BrowserRouter>
  )
}

export default App