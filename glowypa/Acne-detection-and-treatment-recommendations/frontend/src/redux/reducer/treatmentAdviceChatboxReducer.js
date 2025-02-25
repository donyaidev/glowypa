import { changeDiaplay } from "../action/actions";
import {
    CHATBOX_REQUESTION,
    CHATBOX_RESPONSE,
    CHATBOX_RESET,
    CHATBOX_RAG,
    CHATBOX_MEDICAL_DB,
    CHATBOX_FAILURE,
    CHANGE_DISPLAY,
    CHATBOX_REQUESTION_DOCTOR
  } from "../action/types";
const INITIAL_STATE = {
    chatMessage: [],
    loading: false,
    isError: false,
    rag: true,
    medicaldb: false,
    changeDisplay: false,
};

const treatmentAdviceChatbox = (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case CHATBOX_REQUESTION:
            return {
                ...state, chatMessage: [...state.chatMessage, action.payload], loading: true, isError: false,
            };
        case CHATBOX_REQUESTION_DOCTOR:
            return {
                ...state, chatMessage: [...state.chatMessage, action.payload], loading: true, isError: false,
            };
        case CHATBOX_RESPONSE:
            return {
                ...state, chatMessage: [...state.chatMessage, action.payload], loading: false, isError: false,
            };
        case CHATBOX_RESET:
            return {
                ...state, chatMessage: [], loading: false, isError: false,
            };
        case CHATBOX_RAG:
            return {
                ...state, rag: !state.rag,
            };
        case CHATBOX_MEDICAL_DB:
            return {
                ...state, medicaldb: !state.medicaldb,
            };
        case CHATBOX_FAILURE:
            return {
                ...state, isError: true, loading: false,
            };
        case CHANGE_DISPLAY:
            return{
                ...state, changeDisplay: !state.changeDisplay
            }
        default:
            return state;
    }
}

export default treatmentAdviceChatbox;