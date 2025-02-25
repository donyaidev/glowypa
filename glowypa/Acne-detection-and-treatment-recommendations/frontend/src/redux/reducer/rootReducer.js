import { combineReducers } from "redux";
import counterReducer from './counterReducer';
import devideReducer from './devideReducer';
import userReducer from "./userReducer";
import userRegisReducer from "./userRegisReducer";
import acnePredictionDailyReducer from "./acnePredictionDailyReducer";
import activeDialog from "./activeDialogReducer";
import treatmentAdviceChatbox from "./treatmentAdviceChatboxReducer";
import favouritRoutineReducer from "./favouritRoutineReducer";

const rootReducer = combineReducers({
    counter: counterReducer,
    devide: devideReducer,
    user: userReducer,
    userRegis: userRegisReducer,
    acnePredictionDaily: acnePredictionDailyReducer,
    activeDialog: activeDialog,
    adviceChatbox: treatmentAdviceChatbox,
    favoriteRoutine: favouritRoutineReducer,
});

export default rootReducer;