import { createReducer } from "@reduxjs/toolkit"

const initialState = {
    isAuthenticated: false
}

export const userReducer = createReducer(initialState, {
    registerRequest: (state) => {
        state.userlaoding = true;
    },
    registerSuccess: (state, action) => {
        state.userlaoding = false;
        state.isAuthenticated = true;
        state.message = action.payload;
    },
    registerFail: (state, action) => {
        state.userlaoding = false;
        state.isAuthenticated = false;
        state.error = action.payload;
    },
    loginRequest: (state) => {
        state.userlaoding = true;
    },
    loginSuccess: (state, action) => {
        state.userlaoding = false;
        state.isAuthenticated = true;
        state.message = action.payload;
    },
    loginFail: (state, action) => {
        state.userlaoding = false;
        state.isAuthenticated = false;
        state.error = action.payload;
    },
    logoutRequest: (state) => {
        state.userlaoding = true;
    },
    logoutSuccess: (state, action) => {
        state.userlaoding = false;
        state.isAuthenticated = false;
        state.user = null;
        state.message = action.payload;
    },
    logoutFail: (state, action) => {
        state.userlaoding = false;
        state.isAuthenticated = true;
        state.error = action.payload;
    },
    loadUserRequest: (state) => {
        state.userlaoding = true;
    },
    loadUserSuccess: (state, action) => {
        state.userlaoding = false;
        state.isAuthenticated = true;
        state.user = action.payload;
    },
    loadUserFail: (state, action) => {
        state.userlaoding = false;
        state.isAuthenticated = false;
    },
    clearError: (state) => {
        state.error = null
    },
    clearMessage: (state) => { 
        state.message=null;
    },
})