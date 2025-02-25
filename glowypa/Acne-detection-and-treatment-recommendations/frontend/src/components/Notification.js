import React, { useState, useEffect } from "react";
import "./css/Notification.css";
import { useSelector, useDispatch } from "react-redux";
import { fetchUserReset, regisUserReset } from "../redux/action/actions";

const Notification = () => {
  const dispatch = useDispatch();
  const [notification, setNotification] = useState("");
  const [show, setShow] = useState(false);
  const [type, setType] = useState("");
  const errorRegisMessage = useSelector((state) => state.userRegis.errorRegisMessage);

  const isSuccessRegis = useSelector((state) => state.userRegis.isSuccess);
  const isErrorRegis = useSelector((state) => state.userRegis.isError);
  const isErrorLogin = useSelector((state) => state.user.isError);
  const isLoginSuccess = useSelector((state) => state.user.isLoginSuccess);
  const isPredictedSuccess = useSelector(
    (state) => state.acnePredictionDaily.isPredictedSuccess
  );
  const isPredictedError = useSelector(
    (state) => state.acnePredictionDaily.isError
  );

  useEffect(() => {
    let timer;

    if (isPredictedSuccess || isPredictedError) {
      setNotification(
        isPredictedSuccess
          ? "Acne detection successful"
          : "Failed to detect acne"
      );
      setType(isPredictedSuccess ? "success" : "error");
      setShow(true);
      timer = setTimeout(() => setShow(false), 4000);
    }


    return () => {
      clearTimeout(timer);
    };
  }, [
    isSuccessRegis,
    isErrorRegis,
    isPredictedSuccess,
    isPredictedError,
    dispatch,
  ]);

  useEffect(() => {
    let timer;

    if (isSuccessRegis || isErrorRegis) {
      setNotification(
        isSuccessRegis
          ? "Welcome to Glowypa!"
          : `Registration failed: ${errorRegisMessage}`
      );
      setType(isSuccessRegis ? "success" : "error");
      setShow(true);
      timer = setTimeout(() =>{ 
        setShow(false)
        dispatch(regisUserReset());
      }, 4000);
    }

    return () => {
      clearTimeout(timer);
    };
  }, [
    isSuccessRegis,
    isErrorRegis,
    dispatch,
  ]);


  useEffect(() => {
    let timer;

    if (isErrorLogin || isLoginSuccess) {
      console.log("isErrorLogin", isErrorLogin);
      setNotification(
        isLoginSuccess ? "Login Success" : "Login failure, please check again email and password!"
      );
      setType(isLoginSuccess ? "success" : "error");
      setShow(true);
      timer = setTimeout(() => {
        setShow(false);
        dispatch(fetchUserReset());
      }, 4000);
    }

    return () => {
      clearTimeout(timer);
    };
  }, [
    isErrorLogin,
    // isLoginSuccess,
    dispatch,
  ]);

  return (
    <div className={`notification ban--select ${show ? "show" : ""} ${type}`}>
      {notification}
    </div>
  );
};

export default Notification;
