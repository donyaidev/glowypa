import React, { useEffect, useState } from "react";
import "./css/AcneDetectionFuncRight.css";
import { useSelector } from "react-redux";

const AcneDetectionFuncRight = ({
  sliderConfidence,
  sliderOverlap,
  handleChangeSliderConfidence,
  handleChangeSliderOverlap,
  handleChangeSelecteModeUsed,
  selectedOptionModeUsed,
  handleChangeSelecteModelUsed,
  selectedOptionModelUsed,
  labelColors,
}) => {
  const predicted_images = useSelector(
    (state) => state.acnePredictionDaily.predicted_images
  );
  const image_active = useSelector(
    (state) => state.acnePredictionDaily.image_active
  );

  const images = useSelector((state) => state.acnePredictionDaily.images);
  const [labelList, setLabelList] = useState([]);
  const [totalAcnes, setTotalAcnes] = useState(0);
  const [levelAcnes, setLevelAcnes] = useState(-1);

  useEffect(() => {
    predicted_images.map((item) => {
      if (
        item.image_id === image_active &&
        item.architecture_ai_name === selectedOptionModelUsed
      ) {
        const uniqueClassNames = [
          ...new Set(item.predicted.map((item) => item.class_name)),
        ];
        setLabelList(uniqueClassNames);
        setTotalAcnes(item.total_acnes);
        if (item.total_acnes > 0 && item.total_acnes <= 5) {
          setLevelAcnes(1);
        } else if (item.total_acnes > 5 && item.total_acnes <= 20) {
          setLevelAcnes(2);
        } else if (item.total_acnes > 20 && item.total_acnes <= 50) {
          setLevelAcnes(3);
        } else if (item.total_acnes > 50) {
          setLevelAcnes(4);
        } else if (item.total_acnes === 0) {
          setLevelAcnes(0);
        }
      }
    });
    if (predicted_images.length === 0) {
      setLabelList([]);
      setTotalAcnes(0);
      setLevelAcnes(-1);
    }
  }, [selectedOptionModelUsed, image_active, images, predicted_images]);

  return (
    <div className="acne__detection--tag box--shadow-btn">
      {/* <span className="discribe-about-function">
        <QuestionAskImg className="icon__explain--func" />
      </span> */}
      <div className="acne__detection--result-tag">
        <div className="acne__detection--tool-model-modes">
          <div className="acne__detection--tool-model-used">
            <div className="span__tag ban--select">Model Used</div>
            <select
              id="optionsModelUsed"
              value={selectedOptionModelUsed}
              onChange={handleChangeSelecteModelUsed}
              className="select__option box--shadow-btn"
            >
              <option value="" disabled>
                Select an model option
              </option>
              <option value="YoloV8 with SAHI">YoloV8 with SAHI</option>
              <option value="YoloV8">YoloV8</option>
            </select>
          </div>

          <div className="acne__detection--tool-mode-used">
            <div className="span__tag ban--select">Mode Used</div>
            <select
              id="optionsModelUsed"
              value={selectedOptionModeUsed}
              onChange={handleChangeSelecteModeUsed}
              className="select__option box--shadow-btn"
            >
              <option value="all" disabled>
                Select an mode option
              </option>
              <option value="drawall">Draw all</option>
              <option value="drawlabel">Draw Labels</option>
              <option value="drawconfidence">Draw Confidence</option>
            </select>
          </div>
          <div className="acne__detection--tool-scroll box--shadow-btn">
            <span className="ban--select">
              Confidence Threshold: {sliderConfidence}%
            </span>
            <div className="slider-container">
              <span>0%</span>
              <input
                type="range"
                min="1"
                max="100"
                value={sliderConfidence}
                onChange={handleChangeSliderConfidence}
                className="slider box--shadow-btn"
              />
              <span>100%</span>
            </div>
          </div>

          <div className="acne__detection--tool-scroll box--shadow-btn">
            <span className="ban--select">
              Overlap Threshold: {sliderOverlap}%
            </span>
            <div className="slider-container">
              <span>0%</span>
              <input
                type="range"
                min="1"
                max="100"
                value={sliderOverlap}
                onChange={handleChangeSliderOverlap}
                className="slider box--shadow-btn"
              />
              <span>100%</span>
            </div>
          </div>
        </div>

        <div className="acne__detection--tag-labels box--shadow-btn">
          {labelList &&
            labelList.map((item, index) => (
              <div className="labels" key={index}>
                <div
                  className="color-label box--shadow-btn"
                  style={{ background: labelColors[item] }}
                ></div>
                <div className="name-label">{item}</div>
              </div>
            ))}
        </div>
      </div>

      <div className="acne__detection--summary">
        <div className="acne__detection--summary-level-save-update">
          <div
            className="acne__detection--summary-level box--shadow-btn"
            style={{
              backgroundColor:
                levelAcnes === 1
                  ? "#d0f0c0" // Soft Green
                  : levelAcnes === 2
                  ? "#fffacd" // Soft Yellow
                  : levelAcnes === 3
                  ? "#ffcccb" // Soft Pink
                  : levelAcnes === 4
                  ? "#ffe4e1" // Soft Rose
                  : "", // Soft Blue
              color:
                levelAcnes === 1
                  ? "#2e7d32" // Darker Green
                  : levelAcnes === 2
                  ? "#fbc02d" // Darker Yellow
                  : levelAcnes === 3
                  ? "#d32f2f" // Darker Pink
                  : levelAcnes === 4
                  ? "#c62828" // Darker Rose
                  : "", // Darker Blue
            }}
          >
            <span className="ban--select">
              Skin level:{" "}
              {(() => {
                if (levelAcnes === 1) {
                  return <span>Mild</span>;
                } else if (levelAcnes === 2) {
                  return <span>Moderate</span>;
                } else if (levelAcnes === 3) {
                  return <span>Severe</span>;
                } else if (levelAcnes === 4) {
                  return <span>Very Severe</span>;
                } else if (levelAcnes === 0) {
                  return <span>Good Skin (Glow)</span>;
                } else {
                  return <span>No</span>;
                }
              })()}
            </span>
          </div>
        </div>
        <div className="acne__detection--summary-total box--shadow-btn ban--select">
          <span>Total acnes: {totalAcnes ? totalAcnes : "0"}</span>
        </div>
      </div>
    </div>
  );
};

export default AcneDetectionFuncRight;