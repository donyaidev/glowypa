import { changeDiaplay } from "../action/actions";
import {
    GET_FAVOURITE,
    SAVE_FAVOURITE,
    DELETE_FAVOURITE,
    REQUEST_FAVOURITE,
    REQUEST_FAILURE_FAVOURITE,
    REQUEST_SUCCESS_FAVOURITE
  } from "../action/types";
const INITIAL_STATE = {
    chatMessage: [],
    loading: false,
    isError: false,
    changeDisplay: false,
};

const favouritRoutineReducer = (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case SAVE_FAVOURITE:
            return {
                ...state, chatMessage: [...state.chatMessage, action.payload], loading: true, isError: false,
            };
        case DELETE_FAVOURITE:
            return {
                ...state, chatMessage: action.payload, isError: false, loading: false,
            };
        case REQUEST_SUCCESS_FAVOURITE:
            return{
                ...state, chatMessage: [...state.chatMessage, action.payload], loading: false, isError: false,
            }
        case REQUEST_FAILURE_FAVOURITE:
            return{
                ...state, loading: true, isError: false,
            }
        default:
            return state;
    }
}

export default favouritRoutineReducer;