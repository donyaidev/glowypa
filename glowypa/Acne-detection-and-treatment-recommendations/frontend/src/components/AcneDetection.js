// Diagnosis.js
import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import "./css/Acnedetection.css";
import AcneDetectionFuncRight from "./AcneDetectionFuncRight";
import AcneDetectionResultImg from "./AcneDetectionResultImg";
import AcneDetectionFuncHead from "./AcneDetectionFuncHead";
import UploadAndCropImageDialog from "./UploadAndCropImageDialog";

import {activeDialogUploadImg,closeDialogUploadImg } from "../redux/action/actions";


const labelColors = {
  acne_scars: "#FF5733", // Bright Orange
  comedone: "#2980B9", // Bright Blue
  conglobata: "#27AE60", // Bright Green
  crystanlline: "#F39C12", // Bright Yellow
  cystic: "#8E44AD", // Bright Purple
  flat_wart: "#E74C3C", // Bright Red
  folliculitis: "#2ECC71", // Bright Lime
  keloid: "#3498DB", // Bright Sky Blue
  milium: "#E67E22", // Bright Orange
  papule: "#1ABC9C", // Bright Turquoise
  pustule: "#D35400", // Bright Dark Orange
  "sebo-crystan-conglo": "#9B59B6", // Bright Lavender
  syringoma: "#C0392B", // Bright Crimson
  birthmarks: "#F1C40F", // Bright Yellow
};


export default function RightDiagnosis() {
  const dispatch = useDispatch();
  const openUploadImg = useSelector((state) => state.activeDialog.isActiveDialogUploadImg);
  // mode, model, confidence, overlap using for props
  const [sliderConfidence, setSliderConfidence] = useState(1);
  const [sliderOverlap, setSliderOverlap] = useState(1);
  const [selectedOptionModeUsed, setSelectedOptionModeUsed] = useState("all");
  const [selectedOptionModelUsed, setSelectedOptionModelUsed] = useState("YoloV8 with SAHI");

  const handleChangeSelecteModelUsed = (event) => {
    setSelectedOptionModelUsed(event.target.value);
  };
  const handleChangeSelecteModeUsed = (event) => {
    setSelectedOptionModeUsed(event.target.value);
  };
  const handleChangeSliderConfidence = (event) => {
    console.log(event.target.value);
    setSliderConfidence(event.target.value);
  };
  const handleChangeSliderOverlap = (event) => {
    console.log(event.target.value);
    setSliderOverlap(event.target.value);
  };


  return (
    <>
      {openUploadImg && (
        <UploadAndCropImageDialog/>
      )}
      <div className="acne__detection--split">
        <div className="acne__detection--tool">
          <AcneDetectionFuncHead/>
        </div>
        <div className="acne__detection--result">

          <AcneDetectionResultImg
            selectedOptionModeUsed={selectedOptionModeUsed}
            selectedOptionModelUsed = {selectedOptionModelUsed}
            sliderConfidence={sliderConfidence}
            sliderOverlap={sliderOverlap}
            labelColors = {labelColors}
          />
          <AcneDetectionFuncRight
            sliderConfidence={sliderConfidence}
            sliderOverlap={sliderOverlap}
            selectedOptionModeUsed = {selectedOptionModeUsed}
            handleChangeSliderConfidence={handleChangeSliderConfidence}
            handleChangeSliderOverlap={handleChangeSliderOverlap}
            handleChangeSelecteModeUsed = {handleChangeSelecteModeUsed}
            handleChangeSelecteModelUsed = {handleChangeSelecteModelUsed}
            selectedOptionModelUsed = {selectedOptionModelUsed}
            labelColors = {labelColors}
          />
        </div>
      </div>
    </>
  );
}
