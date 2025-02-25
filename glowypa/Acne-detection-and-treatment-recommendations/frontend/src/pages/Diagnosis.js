// Diagnosis.js
import React from "react";
import NavLeft from "../components/NavLeft";
import RightDiagnosis from "../components/RightDiagnosis";
import "./diagnosis.css";
import LoadingPage from "../components/LoadingPage";
import { useSelector } from "react-redux";

export default function Diagnosis() {
  const isLoadingGet = useSelector((state) => state.acnePredictionDaily.isLoadingGet);
  return (
    <>
      {isLoadingGet ? <LoadingPage/> : null}
      <div className="diagnosis">
        <div className="area__left">
          <NavLeft />
        </div>
        <div className="area__right">
          <RightDiagnosis />
        </div>
      </div>
    </>
  );
}
