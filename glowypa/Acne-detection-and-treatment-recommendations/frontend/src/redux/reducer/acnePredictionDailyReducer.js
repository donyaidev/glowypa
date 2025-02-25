import {
  ACNE_DETECTION_DAILY_REQUEST,
  ACNE_DETECTION_DAILY_SUCCESS,
  ACNE_DETECTION_DAILY_FAILURE,
  ACNE_DETECTION_DAILY_CROP_EDIT,
  ACNE_DETECTION_DAILY_ACTIVE_SHOW,
  ACNE_DETECTION_DAILY_REQUEST_GET,
  ACNE_DETECTION_NOTIFICATION_SUCCESS_REQUEST,
} from "../action/types";

const INITIAL_STATE = {
  id_daily_acne_detection: "",
  id_user: "",
  images: [],
  predicted_images: [],
  date: "",
  image_active: "",
  isLoading: false,
  isError: false,
  isLoadingGet: false,
  isPredictedSuccess: false,
};

const acnePredictionDailyReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case ACNE_DETECTION_DAILY_REQUEST:
      return {
        ...state,
        isLoading: true,
        isError: false,
       isPredictedSuccess: false
      };
    case ACNE_DETECTION_DAILY_SUCCESS:
      if (action.dataAcnePredictionDaily.length === 0) {
        return {
          ...state,
          isLoading: false,
          isError: false,
          isLoadingGet: false,
        };
      }
      if (action.dataAcnePredictionDaily !== null) {
        return {
          ...state,
          id_daily_acne_detection: action.dataAcnePredictionDaily.id,
          id_user: action.dataAcnePredictionDaily.id_user,
          images: action.dataAcnePredictionDaily.images,
          predicted_images: action.dataAcnePredictionDaily.predicted_images,
          date: action.dataAcnePredictionDaily.date,
          image_active:
            action.dataAcnePredictionDaily.images[0]?.image_id || "", // Sử dụng optional chaining
          isLoading: false,
          isError: false,
          isLoadingGet: false,
        };
      } else {
        return {
          ...state,
          isLoadingGet: false,
          isLoading: false,
          isError: true,
        };
      }
    case ACNE_DETECTION_DAILY_REQUEST_GET:
      return {
        ...state,
        isError: false,
        isLoadingGet: true,
      };
    case ACNE_DETECTION_DAILY_FAILURE:
      return {
        ...state,
        isError: true,
        isLoading: false,
      };
    case ACNE_DETECTION_NOTIFICATION_SUCCESS_REQUEST:
      return {
        ...state,
        isPredictedSuccess: true,
        isPredictedFailure: false,
      };
    case ACNE_DETECTION_DAILY_CROP_EDIT:
      return {
        ...state,
        images: action.dataCropEdit,
        image_active:
          action.dataCropEdit.length > 0 ? action.dataCropEdit[0].image_id : "",
      };
    case ACNE_DETECTION_DAILY_ACTIVE_SHOW:
      console.log("action.image_id_active", action.image_id_active);
      return {
        ...state,
        image_active: action.image_id_active,
      };
    default:
      return state;
  }
};

export default acnePredictionDailyReducer;
