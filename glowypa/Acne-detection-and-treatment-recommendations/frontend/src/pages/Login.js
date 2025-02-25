import React, { useEffect, useState } from "react";
import "./Login.css";
import { ReactComponent as ViewOnImg } from "../assets/icons/view-on.svg";
import { ReactComponent as ViewOffImg } from "../assets/icons/view-off.svg";
import LogoImg from "../assets/logo/lowypa1.png";
import RegistrationDialog from "../components/RegistrationDialog";
import { useSelector, useDispatch } from "react-redux";
import {
  FetchUsers,
  getDetectionAcneDailyPut,
  fetchUserSuccess,
  regisUserReset,
  getFavourite,
} from "../redux/action/actions";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

const Login = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const isClose = useSelector((state) => state.userRegis.isClose);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [viewPassword, setViewPassword] = useState(false);
  const [regisOpen, setRegisOpen] = useState(false);

  const user = useSelector((state) => state.user.user);
  const isLoading = useSelector((state) => state.user.isLoading);
  const isLoggedIn = useSelector((state) => state.user.isLoggedIn);

  function isTokenExpired(token) {
    if (!token || token === true) {
      return true;
    }
    try {
      const decoded = jwtDecode(token);
      console.log("decoded", decoded);
      const currentTime = Date.now() / 1000;
      return decoded.exp < currentTime;
    } catch (error) {
      console.error("Invalid token:", error);
      return true;
    }
  }

  useEffect(() => {
    const token = localStorage.getItem("authToken");
    const data = localStorage.getItem("userData");
    const isToken = isTokenExpired(token);
    
    if (token && isToken) {
      localStorage.removeItem("authToken");
      localStorage.removeItem("userData");
      window.location.href = "/";
    } else if (token && data && !isToken) {
      dispatch(fetchUserSuccess({ data: JSON.parse(data) }));
    }
  }, [dispatch]);

  useEffect(() => {
    if (isLoggedIn && user) {
      dispatch(getDetectionAcneDailyPut(user.id));
      dispatch(getFavourite(user.id));
      navigate("/diagnosis");
    }
    console.log(user);
  }, [isLoggedIn, user, dispatch, navigate]);

  const handleChangeRegisOpen = () => {
    setRegisOpen((prev) => !prev);
  };

  const handleViewPassword = () => {
    setViewPassword((prev) => !prev);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      email: email,
      password: password,
    };
    dispatch(FetchUsers(data));
  };

  useEffect(() => {
    if (isClose) {
      setRegisOpen(false);
    }
  }, [isClose]);

  return (
    <>
      {regisOpen && (
        <RegistrationDialog handleChangeRegisOpen={handleChangeRegisOpen} />
      )}
      <div className="login__background ban--select">
        <div className="login__background--split">
          <div className="sologan__background">
            <img
              className="sologan__background--logo"
              src={LogoImg}
              alt="Logo"
            />
            <p className="title">Skin Diagnosis</p>
            <p className="sologan__background-p">
              Detect early, treat smart, care for skin for life
            </p>
          </div>
          <div className="form__login box--shadow-btn">
            <form onSubmit={handleSubmit} className="login">
              <p className="title">Login</p>
              <div className="login__email">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="Email"
                />
              </div>
              <div className="login__password">
                <input
                  type={viewPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="Password"
                  minLength={8}
                />
                {viewPassword ? (
                  <ViewOffImg
                    onClick={handleViewPassword}
                    className="icon--element-view"
                  />
                ) : (
                  <ViewOnImg
                    onClick={handleViewPassword}
                    className="icon--element-view"
                  />
                )}
              </div>
              <div className="forget__func">
                <span>Forget password?</span>
              </div>
              <button className="login__submit--btn" type="submit">
                Login
              </button>
            </form>
            <div className="hr__split"></div>
            <div className="login_func">
              <button
                className="login__submit--btn "
                onClick={handleChangeRegisOpen}
              >
                Register
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Login;