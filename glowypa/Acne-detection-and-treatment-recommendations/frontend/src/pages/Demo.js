// Diagnosis.js
import React from "react";
import NavLeft from "../components/NavLeft";
import "./diagnosis.css";
import LoadingPage from "../components/LoadingPage";
import { useSelector } from "react-redux";
import "./Demo.css";
import Glowypa from "../assets/logo/logoIcon1.png";
import { useNavigate, useLocation } from "react-router-dom";

export default function Test() {
  const navigate = useNavigate();

  const isLoadingGet = useSelector(
    (state) => state.acnePredictionDaily.isLoadingGet
  );
  const handleClickNav = (path) => {
    navigate(path);
  };

  return (
    <>
      {isLoadingGet ? <LoadingPage /> : null}
      <div className="demo__background">
        <div className="area__left">
          <NavLeft />
        </div>
        <div className="main__demo">
          <div className="main__demo--left">
            <div className="main__demo--head">
              <div className="demo__background_para">
                <p className="main__demo--para1">
                  Revolutionizing Your Skincare Routine.
                </p>
              </div>
              
              <p className="main__demo--para2">Powered by AI.</p>
              <p className="main__demo--para3">
                Achieve Radiant Skin Effortlessly: Personalized Acne Solutions,
                Expert Guidance, and Real-Time Support{" "}
              </p>
              <button
                onClick={() => handleClickNav("/diagnosis")}
                className="btn__use box--shadow-btn"
              >
                Use Now
              </button>
            </div>
            <div className="main__demo--head">
              <div className="main__demo--video box--shadow-btn">
                <iframe
                  width="100%"
                  height="100%"
                  src="https://www.youtube.com/embed/i_NV6k7PqF0?si=UICH1odvBebS4K8m&autoplay=1&mute=1"
                  title="YouTube video player"
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                ></iframe>
              </div>{" "}
            </div>
            {/* <div className="footer__demo--container">
              <img className="logo" src={Glowypa} alt="" />
            </div> */}
          </div>
        </div>
      </div>
    </>
  );
}
