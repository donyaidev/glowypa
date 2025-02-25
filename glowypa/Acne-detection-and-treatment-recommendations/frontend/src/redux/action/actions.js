import axios from "axios";

import { BASE_URL } from "../../configs/config";

import {
  INCREMENT,
  DECREMENT,
  DEVIDE,
  FETCH_USER_FAILURE,
  FETCH_USER_SUCCESS,
  FETCH_USER_REQUEST,
  REGIS_USER_FAILURE,
  REGIS_USER_SUCCESS,
  REGIS_USER_REQUEST,
  ACNE_DETECTION_DAILY_REQUEST,
  ACNE_DETECTION_DAILY_SUCCESS,
  ACNE_DETECTION_DAILY_FAILURE,
  ACNE_DETECTION_DAILY_CROP_EDIT,
  ACNE_DETECTION_DAILY_ACTIVE_SHOW,
  ACNE_DETECTION_DAILY_REQUEST_GET,
  ACNE_DETECTION_NOTIFICATION_SUCCESS_REQUEST,
  FETCH_USER_RESET,
  REGIS_USER_RESET,
  ACNE_DETECTION_DAILY_RESET,
  ACTIVE_DIALOG_SETTING,
  ACTIVE_DIALOG_RESET,
  CLOSE_DIALOG_SETTING,
  ACTIVE_DIALOG_UPLOAD_IMG,
  CLOSING_DIALOG_UPLOAD_IMG,
  CHATBOX_REQUESTION,
  CHATBOX_REQUESTION_DOCTOR,
  CHATBOX_RESPONSE,
  CHATBOX_RESET,
  CHATBOX_RAG,
  CHATBOX_MEDICAL_DB,
  CHATBOX_FAILURE,
  CHANGE_DISPLAY,
  SAVE_FAVOURITE,
  DELETE_FAVOURITE,
  REQUEST_FAVOURITE,
  REQUEST_FAILURE_FAVOURITE,
  REQUEST_SUCCESS_FAVOURITE,
  GET_FAVOURITE
} from "./types";

export const increaseCounter = (data) => {
  return {
    type: INCREMENT,
    payload: { name: "Nguyen Van A", data: data },
  };
};

export const decreaseCounter = () => {
  return {
    type: DECREMENT,
  };
};

export const devideCounter = () => {
  return {
    type: DEVIDE,
  };
};

// login
export const FetchUsers = (data) => {
  return async (dispatch, getState) => {
    console.log("dataRes", data);
    try {
      dispatch(fetchUserRequest());

      const res = await axios.post(`${BASE_URL}/api/user/login/`, data);
      const dataRes = res && res.data ? res.data : {};

      console.log("dataRes", dataRes);

      if (dataRes.token) {
        localStorage.setItem("authToken", dataRes.token);
        localStorage.setItem("userData", JSON.stringify(dataRes.data));
      }

      dispatch(fetchUserSuccess(dataRes));
    } catch (error) {
      console.error("Login error:", error);
      dispatch(fetchUserFailure(error));
    }
  };
};

export const fetchUserRequest = () => {
  return {
    type: FETCH_USER_REQUEST,
  };
};

export const fetchUserSuccess = (dataRes) => {
  console.log("dataRRRR", dataRes);
  return {
    type: FETCH_USER_SUCCESS,
    dataUser: dataRes,
  };
};

export const fetchUserFailure = (error) => {
  return {
    type: FETCH_USER_FAILURE,
    payload: error,
  };
};
export const fetchUserReset = () => {
  return {
    type: FETCH_USER_RESET,
  };
};

// regis user

export const regisUsers = (data) => {
  return async (dispatch, getState) => {
    try {
      dispatch(regisUserRequest());
      const res = await axios.post(`${BASE_URL}/api/user/register/`, data);
      dispatch(regisUserSuccess());
    } catch (error) {
      const dataRes = error.response.data["detail"];
      console.log("error", error);
      dispatch(regisUserFailure(dataRes));
    }
  };
};

export const regisUserRequest = () => {
  return {
    type: REGIS_USER_REQUEST,
  };
};

export const regisUserSuccess = () => {
  return {
    type: REGIS_USER_SUCCESS,
  };
};

export const regisUserReset = () => {
  return {
    type: REGIS_USER_RESET,
  };
};

export const regisUserFailure = (error) => {
  return {
    type: REGIS_USER_FAILURE,
    payload: error,
  };
};

// detection skin daily
export const detectionAcneDaily = (data, user_id) => {
  return async (dispatch, getState) => {
    try {
      dispatch(detectionAcneDailyRequest());

      const token = localStorage.getItem("authToken");
      const res = await axios.post(
        `${BASE_URL}/api/acne_detection_daily/${user_id}`,
        data,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      const detectionResult = res && res.data ? res.data.data : null;
      console.log("dadaad---", detectionResult);
      console.log("data",res.data.status_put)
      console.log("dada",data)
        try {
          // Only proceed with treatment advice if detection was successful
          if (detectionResult) {
            // Prepare message with detection results
            const adviceMessage = {
              user_id: user_id,
              role: "bot",
              message: '',
              rag: true,
              db: true,
              history_chat: [],
            };
  
            // Get treatment advice
            const resAdvice = await axios.post(
              `${BASE_URL}/api/chatbox_ance/`, 
              adviceMessage, 
              {
                headers: { Authorization: `Bearer ${token}` },
              }
            );
  
            const treatmentAdvice = resAdvice && resAdvice.data ? resAdvice.data.chatbox : null;
            console.log(treatmentAdvice)
            // Update UI with treatment advice
            if (treatmentAdvice) {
              dispatch(chatboxResponse(treatmentAdvice));
            } else {
              dispatch(chatboxFailure({ message: "No treatment advice generated" }));
            }
          } else {
            dispatch(chatboxFailure({ message: "Acne detection results not available" }));
          }
        } catch (error) {
          dispatch(chatboxFailure(error));
          console.log("Treatment advice error:", error);
        }
      
      dispatch(detectionAcneDailySuccess(detectionResult));
      dispatch(detectionAcneDailySuccessNoti());
      dispatch(closeDialogUploadImg());
    } catch (error) {
      dispatch(detectionAcneDailyFailure(error));
      console.log("error", error);
    }
  };
};
export const detectionAcneDailyPut = (data, user_id) => {
  return async (dispatch, getState) => {
    try {
      // Start detection request
      dispatch(detectionAcneDailyRequest());
      const token = localStorage.getItem("authToken");

      // Step 1: Upload and detect acne
      const res = await axios.put(
        `${BASE_URL}/api/acne_detection_daily/deleteAndPut/${user_id}`,
        data,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      const detectionResult = res && res.data ? res.data.data : null;
      console.log("data",res)
      console.log("dadaad---", detectionResult);

      if(res.data.status_put){
        try {
          // Only proceed with treatment advice if detection was successful
          if (detectionResult) {
            // Prepare message with detection results
            const adviceMessage = {
              user_id: user_id,
              role: "bot",
              message: '',
              rag: true,
              db: true,
              history_chat: [],
            };
  
            // Get treatment advice
            const resAdvice = await axios.post(
              `${BASE_URL}/api/chatbox_ance/`, 
              adviceMessage, 
              {
                headers: { Authorization: `Bearer ${token}` },
              }
            );
  
            const treatmentAdvice = resAdvice && resAdvice.data ? resAdvice.data.chatbox : null;
            console.log(treatmentAdvice)
            // Update UI with treatment advice
            if (treatmentAdvice) {
              dispatch(chatboxResponse(treatmentAdvice));
            } else {
              dispatch(chatboxFailure({ message: "No treatment advice generated" }));
            }
          } else {
            dispatch(chatboxFailure({ message: "Acne detection results not available" }));
          }
        } catch (error) {
          dispatch(chatboxFailure(error));
          console.log("Treatment advice error:", error);
        }
      }
      console.log("deted", detectionResult)
      dispatch(detectionAcneDailySuccess(detectionResult));
      dispatch(detectionAcneDailySuccessNoti());
      dispatch(closeDialogUploadImg());
    } catch (error) {
      dispatch(detectionAcneDailyFailure(error));
      console.log("Detection error:", error);
    }
  };
};


export const getDetectionAcneDailyPut = (user_id) => {
  return async (dispatch, getState) => {
    try {
      dispatch(detectionAcneDailyRequestGet());

      const token = localStorage.getItem("authToken");
      const res = await axios.get(
        `${BASE_URL}/api/acne_detection_daily/${user_id}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      const dataRes = res && res.data ? res.data.data : null;
        dispatch(detectionAcneDailySuccess(dataRes));
    } catch (error) {
      dispatch(detectionAcneDailyFailure(error));
      console.log("error", error);
    }
  };
};


export const updateLike = (routine_id, product) => {
  return async (dispatch, getState) => {
    try {
      const token = localStorage.getItem("authToken");
      const res = await axios.put(
        `${BASE_URL}/api/skincare-routine/${routine_id}/${product}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      console.log("like success")
    } catch (error) {
      dispatch(detectionAcneDailyFailure(error));
      console.log("error", error);
    }
  };
};




export const detectionAcneDailyRequest = () => {
  return {
    type: ACNE_DETECTION_DAILY_REQUEST,
  };
};

export const detectionAcneDailyRequestGet = () => {
  return {
    type: ACNE_DETECTION_DAILY_REQUEST_GET,
  };
};

export const detectionAcneDailySuccess = (dataRes) => {
  return {
    type: ACNE_DETECTION_DAILY_SUCCESS,
    dataAcnePredictionDaily: dataRes,
  };
};

export const detectionAcneDailySuccessNoti = () => {
  return {
    type: ACNE_DETECTION_NOTIFICATION_SUCCESS_REQUEST,
  };
};

export const detectionAcneDailyFailure = (error) => {
  return {
    type: ACNE_DETECTION_DAILY_FAILURE,
    payload: error,
  };
};
// edit image crop
export const detectionAcneDailyCropEdit = (data) => {
  return {
    type: ACNE_DETECTION_DAILY_CROP_EDIT,
    dataCropEdit: data,
  };
};
// show image active
export const detectionAcneDailyActiveShow = (image_id) => {
  return {
    type: ACNE_DETECTION_DAILY_ACTIVE_SHOW,
    image_id_active: image_id,
  };
};

// ACTIVE DIALOG
export const activeDialogSetting = () => {
  return {
    type: ACTIVE_DIALOG_SETTING,
  };
};

export const closeDialogSetting = () => {
  return {
    type: CLOSE_DIALOG_SETTING,
  };
};

export const activeDialogUploadImg = () => {
  return {
    type: ACTIVE_DIALOG_UPLOAD_IMG,
  };
};

export const closeDialogUploadImg = () => {
  return {
    type: CLOSING_DIALOG_UPLOAD_IMG,
  };
};

// chatbox
export const chatboxRequestUser = (data) => {
  return {
    type: CHATBOX_REQUESTION,
    payload: data,
  };
};

export const chatboxRequestDoctorAdvice = (data) => {
  return {
    type: CHATBOX_REQUESTION_DOCTOR,
    payload: data,
  };
};

export const chatboxRequestion = (data) => {
  return async (dispatch, getState) => {
    try {
      dispatch(chatboxRequestDoctorAdvice(data));
      const token = localStorage.getItem("authToken");
      console.log("dataRes-----|", data);
      const res = await axios.post(`${BASE_URL}/api/chatbox/`, data, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const dataRes = res && res.data ? res.data.chatbox : null;
      console.log("dadaad---", dataRes);
      dispatch(chatboxResponse(dataRes));
    } catch (error) {
      dispatch(chatboxFailure(error));
      console.log("error", error);
    }
  };
};

export const RecommendProduct = (data) => {
  return async (dispatch, getState) => {
    try {
      dispatch(chatboxRequestDoctorAdvice(data));
      const token = localStorage.getItem("authToken");
      console.log("dataRes-----|", data);
      const res = await axios.post(`${BASE_URL}/api/skincare-routine/routine_acne/`, data, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const dataRes = res && res.data ? res.data.chatbox : null;
      console.log("dadaad---", dataRes);
      dispatch(chatboxResponse(dataRes));
    } catch (error) {
      dispatch(chatboxFailure(error));
      console.log("error", error);
    }
  };
};

export const chatboxResponse = (data) => {
  return {
    type: CHATBOX_RESPONSE,
    payload: data,
  };
};

export const chatboxReset = () => {
  return {
    type: CHATBOX_RESET,
  };
};

export const chatboxRag = () => {
  return {
    type: CHATBOX_RAG,
  };
};

export const chatboxMedicalDb = () => {
  return {
    type: CHATBOX_MEDICAL_DB,
  };
};

export const chatboxFailure = (error) => {
  return {
    type: CHATBOX_FAILURE,
    payload: error,
  };
};

export const changeDiaplay = () => {
  console.log('to here--')
  return {
    type: CHANGE_DISPLAY,
  }
}

export const favouriteSuccess = (dataRes) => {
  return {
    type: REQUEST_SUCCESS_FAVOURITE,
    payload: dataRes,
  };
};

export const favouriteFailure = (error) => {
  return {
    type: REQUEST_FAILURE_FAVOURITE,
    payload: error,
  };
};

export const getFavourite = (user_id) => {
  return async (dispatch, getState) => {
    try {
      const token = localStorage.getItem("authToken");
      const res = await axios.get(
        `${BASE_URL}/api/v1/storage-recommend-messages/${user_id}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      console.log("routine_data", res.data);
      const dataRes = res && res.data ? res.data : null;

      if (dataRes && Array.isArray(dataRes)) {
        // Loop through dataRes and dispatch each item
        for (let i = 0; i < dataRes.length; i++) {
          console.log('1')
          dispatch(favouriteSuccess(dataRes[i]));
        }
      } else {
        console.log("dataRes is not an array or is null");
      }
    } catch (error) {
      dispatch(favouriteFailure(error));
      console.log("error", error);
    }
  };
};


export const postFavourite = (data) => {
  return async (dispatch, getState) => {
    try {
      console.log(data)
      const token = localStorage.getItem("authToken");
      const res = await axios.post(
        `${BASE_URL}/api/v1/storage-recommend-message/`, data,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      const dataRes = res && res.data ? res.data : null;

      if (dataRes && Array.isArray(dataRes)) {
        for (let i = 0; i < dataRes.length; i++) {
          console.log('1')
          dispatch(favouriteSuccess(dataRes[i]));
        }
      } else {
        console.log("dataRes is not an array or is null");
      }
    } catch (error) {
      dispatch(favouriteFailure(error));
      console.log("error", error);
    }
  };
};

export const deleteFavourit = (data) => {
  return {
    type: DELETE_FAVOURITE,
    payload: data,
  };
};

export const deleteFavourite = (data) => {
  return async (dispatch, getState) => {
    try {
      console.log(data)
      const token = localStorage.getItem("authToken");
      const res = await axios.delete(
        `${BASE_URL}/api/v1/storage-recommend-message/${data.id}/${data.user_id}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      const dataRes = res && res.data ? res.data : null;
      dispatch(deleteFavourit(dataRes));
    } catch (error) {
      dispatch(favouriteFailure(error));
      console.log("error", error);
    }
  };
};


export const requestGetFavourit = (data) => {
  return {
    type: REQUEST_FAVOURITE,
    payload: data,
  };
};