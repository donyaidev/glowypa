import {
  REGIS_USER_FAILURE,
  REGIS_USER_SUCCESS,
  REGIS_USER_REQUEST,
} from "../action/types";

const INITIAL_STATE = {
  isLoading: false,
  isError: false,
  isClose: false,
  isSuccess: false,
  errorRegisMessage: "",
};

const userRegisReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case REGIS_USER_REQUEST:
      return {
        ...state,
        isLoading: true,
        isError: false,
        isSuccess: false,
      };
    case REGIS_USER_SUCCESS:
      return {
        ...state,
        isLoading: false,
        isError: false,
        isClose: true,
        isSuccess: true,
      };
    case REGIS_USER_FAILURE:
      
      return {
        ...state,
        isError: true,
        isLoading: false,
        isSuccess: false,
        errorRegisMessage: action.payload,
      };

    case "REGIS_USER_RESET":
      return {
        ...state,
        isError: false,
        isLoading: false,
        isSuccess: false,
        isClose: false,
      };
    default:
      return state;
  }
};

export default userRegisReducer;
