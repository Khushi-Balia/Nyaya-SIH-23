import axios from "axios";
import { server } from "../store";
// import { useNavigate } from "react-router-dom";

// load user
export const loadUser = () => async (dispatch) => {
    try {
        dispatch({
            type: "loadUserRequest"
        })

        const {data} = await axios.post(`${server}/users/me`,{
          "token":localStorage.getItem("usertoken")
        },{
            "withCredentials": true,
          });
          console.log(data);
        
        const user=await data.user          
        dispatch({
            type: "loadUserSuccess",
            payload: user
        })
    } catch (error) {
        console.log(error)
        const err = await error.response && error.response.data.msg
        dispatch({
            type: "loadUserFail",
            payload: err
        })
    }
}

export const registerUser = (name,email,password) => async(dispatch)=>{
    try {
        dispatch({
            type:"registerRequest"
        })
        const {data} = await axios.post(`${server}/users/signup`, {
          name: name,
          email: email,
          password: password
        },{
          "withCredentials": true,
        })
        console.log(data);
        const token=await data.token;
        localStorage.setItem("usertoken",token);
        dispatch({type:"registerSuccess",payload:data.msg})
      } catch (error) {
        // console.log(error.response.data.msg)
        console.log(error); 
        const err = await error.response && error.response.data.msg
        dispatch({type: "registerFail", payload: err})
      }
}

export const loginUser = (email,password) => async(dispatch)=>{
    try {
        dispatch({type:"loginRequest"})
        const {data} = await axios.post(`${server}/users/login`, {
          email: email,
          password: password
        },{
          "withCredentials": true,
        })
        console.log(data);
        const token=await data.token;
        localStorage.setItem("usertoken",token);
        dispatch({type: "loginSuccess", payload: data.msg});
      } catch (error) {
        // console.log(error)
        console.log(error); 
        const err = await error.response && error.response.data.msg
        dispatch({type: "loginFail", payload: err})
      }
}

export const logoutUser = () => async (dispatch) => {
  try{
      dispatch({type: "logoutRequest"});

      const {data} = await axios.get(`${server}/users/logout`,{
          "withCredentials": true,
      });
      console.log(data);
      localStorage.removeItem("usertoken");
      dispatch({type: "logoutSuccess", payload: data.msg});
  }catch(error){
    console.log(error); 
    const err = await error.response && error.response.data.msg
    dispatch({type: "logoutFail", payload: err})
  }
}
