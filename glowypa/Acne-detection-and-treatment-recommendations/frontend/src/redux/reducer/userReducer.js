import {
  FETCH_USER_FAILURE,
  FETCH_USER_SUCCESS,
  FETCH_USER_REQUEST,
  FETCH_USER_RESET,

} from "../action/types";

const INITIAL_STATE = {
  user: [],
  isLoggedIn: false,
  isLoading: false,
  isError: false,
  isLoginSuccess: false,
};

const userReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case FETCH_USER_REQUEST:
      return {
        ...state, isLoading: true, isError: false, isLoginSuccess: false,
      };
    case FETCH_USER_SUCCESS:
      return {
        ...state, user: action.dataUser.data, isLoading: false, isError: false, isLoggedIn: true, isLoginSuccess: true,
      };
    case FETCH_USER_FAILURE:
      return {
        ...state, isError: true, isLoading: false, isLoginSuccess: false,
      };
    case FETCH_USER_RESET:
      console.log('check reset')
      return {
        ...state, isError: false, isLoading: false, isLoginSuccess: false
      }
    default:
      return state;
  }
};

export default userReducer;
