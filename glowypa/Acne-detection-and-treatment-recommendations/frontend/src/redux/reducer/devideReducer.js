import {DEVIDE} from '../action/types';

const INITIAL_STATE = {
    devide: 10,
};

const devideReducer = (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case DEVIDE:
            return {
                ...state, devide: state.devide / 2,
            };
        default:
            return state;
    }
}

export default devideReducer;