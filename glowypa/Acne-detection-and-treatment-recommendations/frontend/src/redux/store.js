import { createStore, applyMiddleware } from "redux";
import rootReducer from "./reducer/rootReducer.js";
// import { composeWithDevTools } from "redux-devtools-extension";
import thunkMiddleware from "redux-thunk";
// includes: reducers, middleware
const store = createStore(
    rootReducer, 
    // composeWithDevTools(applyMiddleware(thunkMiddleware))
    applyMiddleware(thunkMiddleware)
);

export default store;
