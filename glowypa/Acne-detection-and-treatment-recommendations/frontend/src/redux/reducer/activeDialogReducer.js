import { CLOSE_DIALOG_SETTING, ACTIVE_DIALOG_SETTING } from "../action/types";

const INITIAL_STATE = {
  isActiveDialogSetting: false,
  isActiveDialogUploadImg: false,
};

const dialogReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case "ACTIVE_DIALOG_SETTING":
      return {
        ...state,
        isActiveDialogSetting: true,
      };
    case "CLOSE_DIALOG_SETTING":
      return {
        ...state,
        isActiveDialogSetting: false,
      };
    case "ACTIVE_DIALOG_UPLOAD_IMG":
      return {
        ...state,
        isActiveDialogUploadImg: true,
      };
    case "CLOSING_DIALOG_UPLOAD_IMG":
      return {
        ...state,
        isActiveDialogUploadImg: false,
      };
    default:
      return state;
  }
};

export default dialogReducer;
