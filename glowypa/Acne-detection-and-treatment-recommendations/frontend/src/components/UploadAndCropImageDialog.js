import React, { useState, useRef } from "react";
import Cropper from "react-cropper";
import Webcam from "react-webcam";
import "cropperjs/dist/cropper.css";
import "./css/UploadAndCropImageDialog.css";
import { ReactComponent as MultipleImg } from "../assets/icons/multiple.svg";
import { ReactComponent as CropImg } from "../assets/icons/crop.svg";
import { ReactComponent as UploadImg } from "../assets/icons/upload-img.svg";
import { ReactComponent as LockedImg } from "../assets/icons/locked.svg";
import { ReactComponent as MedicalImg } from "../assets/icons/medical.svg";
import { ReactComponent as CameraImg } from "../assets/icons/camera.svg";
import { ReactComponent as CaptureImg } from "../assets/icons/capture.svg";

import ZoomAcneImg from "../assets/icons/zoom_images.png";
import LimitedImg from "../assets/icons/limited_images.png";
import HighQualityImg from "../assets/icons/high_quality.png";

import ImgDiagnoisis from "./ImgDiagnoisis";
import LoadingTask from "./LoadingTask";
import { useSelector, useDispatch } from "react-redux";
import {
  detectionAcneDailyPut,
  detectionAcneDaily,
  closeDialogUploadImg,
} from "../redux/action/actions";

const UploadAndCropImage = () => {
  const dispatch = useDispatch();
  const user_id = useSelector((state) => state.user.user.id);
  const id_daily_acne_detection = useSelector(
    (state) => state.acnePredictionDaily.id_daily_acne_detection
  );
  const images = useSelector((state) => state.acnePredictionDaily.images);
  const isLoading = useSelector((state) => state.acnePredictionDaily.isLoading);

  const [imageBase64Array, setImageBase64Array] = useState(images);
  const [imagePredict, setImagePredict] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [uploadError, setUploadError] = useState("");
  const [idImgDelete, setIdImgDelete] = useState([]);
  const [notificationEmpty, setNotificationEmpty] = useState(false);
  const [isWebcamOpen, setIsWebcamOpen] = useState(false);

  const cropperRef = useRef(null);
  const webcamRef = useRef(null);

  const generateDateTimeId = () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const seconds = String(now.getSeconds()).padStart(2, "0");
    const milliseconds = String(now.getMilliseconds()).padStart(3, "0");
    return `${year}${month}${day}${hours}${minutes}${seconds}${milliseconds}`;
  };

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const img = new Image();
      img.onload = () => {
        if (img.width < 640 || img.height < 640) {
          setUploadError("Image must be at least 640x640 pixels.");
          setSelectedImage(null);
        } else {
          const reader = new FileReader();
          reader.onloadend = () => {
            setSelectedImage(reader.result);
            setUploadError("");
          };
          reader.readAsDataURL(file);
        }
      };
      img.src = URL.createObjectURL(file);
      event.target.value = null;
    }
  };

  const handleCrop = () => {
    const cropper = cropperRef.current.cropper;
    const croppedImage = cropper
      .getCroppedCanvas({
        width: 640,
        height: 640,
      })
      .toDataURL();
    let imgUpObject = {
      image_id: generateDateTimeId(),
      image_base64: croppedImage,
    };
    setImageBase64Array((prevArray) => [...prevArray, imgUpObject]);
    setImagePredict((prevArray) => [...prevArray, imgUpObject]);
    setSelectedImage(null);
  };

  const handleCancel = () => {
    setSelectedImage(null);
  }

  const handleDeleteImage = (id_img) => {
    setIdImgDelete((prevArray) => [...prevArray, id_img]);

    setImagePredict((prevArray) => {
      const newArray = prevArray.filter((imgObj) => imgObj.image_id !== id_img);
      return newArray;
    });

    setImageBase64Array((prevArray) => {
      const newArray = prevArray.filter((imgObj) => imgObj.image_id !== id_img);
      return newArray;
    });
    console.log("Delete image with id:", idImgDelete);
  };

  const isUploadDisabled = imageBase64Array.length >= 4;

  const handleDispatchImage = () => {
    if (id_daily_acne_detection == "") {
      if (imagePredict.length === 0) {
        setNotificationEmpty(true);
        setTimeout(() => {
          setNotificationEmpty(false);
        }, 3000);
        return;
      }
      dispatch(detectionAcneDaily(imagePredict, user_id));
    } else {
      if (
        (imagePredict.length === 0 && idImgDelete.length === 0) ||
        (images.length === 0 && imagePredict.length === 0)
      ) {
        setNotificationEmpty(true);
        setTimeout(() => {
          setNotificationEmpty(false);
        }, 3000);
        return;
      }
      let data = {
        image_base64_list: imagePredict,
        img_id_remove_list: idImgDelete,
      };
      console.log("data", data);
      dispatch(detectionAcneDailyPut(data, user_id));
      setImagePredict([]);
    }
  };

  const captureWebcamImage = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    if (imageSrc) {
      const img = new Image();
      img.src = imageSrc;

      img.onload = () => {
        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");

        canvas.width = img.width;
        canvas.height = img.height;

        // Lật ảnh theo chiều ngang
        context.translate(canvas.width, 0);
        context.scale(-1, 1);

        context.drawImage(img, 0, 0, img.width, img.height);

        // Lấy dữ liệu hình ảnh từ canvas
        const flippedImageSrc = canvas.toDataURL("image/jpeg");

        setSelectedImage(flippedImageSrc);
        setIsWebcamOpen(false);
      };
    }
  };

  const captureWebcamImageClose = () => {
    setIsWebcamOpen(false);
  }

  const handleCloseUploadImgDialog = () => {
    dispatch(closeDialogUploadImg());
  };

  return (
    <div className="background__dialog ban--select">
      <div className="background__dialog--main box--shadow-btn">
        {isLoading && <LoadingTask />}
        <div className="dialog__header">
          <div className="dialog__header--area dialog__header--title">
            Choose Image Diagnosis
          </div>
          <button
            className="cls__btn box--shadow-btn"
            onClick={() => handleCloseUploadImgDialog()}
          >
            <MultipleImg className="icon--element-mul" />
          </button>
        </div>
        <div className="dialog__body">
          <div className="dialog__body-func">
            <div
              className={`dialog__body--upload-img-btn ${
                isUploadDisabled ? "disabled" : ""
              }`}
              onClick={() =>
                !isUploadDisabled &&
                document.getElementById("upload-input").click()
              }
              style={{
                cursor:
                  isUploadDisabled || isWebcamOpen || selectedImage
                    ? "not-allowed"
                    : "pointer",
              }}
            >
              {isUploadDisabled ? (
                <LockedImg className="icon--element-locked" />
              ) : (
                <UploadImg className="icon--element-unlocked" />
              )}

              <p>
                {isUploadDisabled
                  ? "Image limit reached"
                  : "Click upload image"}
              </p>
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                style={{ display: "none", width: "100%", height: "100%" }}
                id="upload-input"
                disabled={isUploadDisabled || selectedImage || isWebcamOpen}
              />
            </div>
            <div
              className={`dialog__body--upload-img-btn webcam ${
                isUploadDisabled ? "disabled" : ""
              }`}
              onClick={() => {
                if (!isWebcamOpen && !selectedImage && !isUploadDisabled) {
                  setIsWebcamOpen(true);
                }
              }}
              style={{
                cursor:
                  isUploadDisabled || isWebcamOpen || selectedImage
                    ? "not-allowed"
                    : "pointer",
              }}
            >
              {isUploadDisabled ? (
                <CameraImg className="icon--element-locked" />
              ) : (
                <CameraImg className="icon--element-unlocked" />
              )}
              <p>Webcam</p>
            </div>
            {notificationEmpty && (
              <div className="notification__empty">
                <p>Hãy thêm dữ liệu!</p>
              </div>
            )}
          </div>

          {uploadError && <p className="error-message">{uploadError}</p>}

          {selectedImage && (
            <>
              <div className="cropper-container">
                <Cropper
                  src={selectedImage}
                  style={{ height: 400, width: "100%" }}
                  aspectRatio={1}
                  guides={false}
                  ref={cropperRef}
                  viewMode={1}
                  dragMode="move"
                  cropBoxMovable={false}
                  cropBoxResizable={false}
                  toggleDragModeOnDblclick={false}
                  minCropBoxWidth={640}
                  minCropBoxHeight={640}
                  background={false}
                  responsive={true}
                  autoCropArea={1}
                  checkOrientation={false}
                />
              </div>
              <div className="btn__func--crop">
               
                <button
                  onClick={handleCancel}
                  className="cancel-btn box--shadow-btn"
                >
                  <span>Cancel</span>
                </button>
                <button
                  onClick={handleCrop}
                  className="crop-btn box--shadow-btn"
                >
                  <CropImg className="icon--element-crop" />
                  <span>Crop Image</span>
                </button>
              </div>
            </>
          )}

          {isWebcamOpen && (
            <div className="webcam-container">
              <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                width="100%"
                videoConstraints={{
                  width: 2560,
                  height: 1440,
                  facingMode: "user",
                }}
                className="webcam-flip"
              />
              <div className="bouding__capture--btn">
                <button onClick={captureWebcamImage} className="capture-btn box--shadow-btn">
                  <span>Capture</span>
                </button>
                <button
                  onClick={captureWebcamImageClose}
                  className="cancel-btn box--shadow-btn"
                >
                  <span>Cancel</span>
                </button>
              </div>
            </div>
          )}
          <div className="list__img--diagnoises">
            <div className="list__diagnoises--img">
              {imageBase64Array.map((object, index) => (
                <ImgDiagnoisis
                  key={index}
                  image_id={object.image_id}
                  base64Image={object.image_base64}
                  onDelete={handleDeleteImage}
                />
              ))}
            </div>
          </div>

          <div className="save__img">
            <button
              className="dialog__img-save box--shadow-btn"
              onClick={() => {
                handleDispatchImage();
                setIdImgDelete([]);
              }}
            >
              <MedicalImg className="icon--element-med" />
              <span>Carry out diagnosis</span>
            </button>
          </div>

          <div className="img__diagnoises--recommend">
            <div className="img__diagnoises--rule--title">
              How to take a good image?
            </div>
            <div className="img__diagnoises--rules--list">
              <div className="img__diagnoises--rule">
                <div className="img__diagnoises--guild">
                  <img
                    className="img__diagnoises--icon"
                    src={HighQualityImg}
                    alt="limited_images"
                  />
                </div>
                <div className="img_diagnoises--text">
                  {/* Đảm bảo rằng các ảnh tải lên có độ phân giải cao để tránh bị
                  vỡ khi cắt ảnh và hỗ trợ quá trình chuẩn đoán chính xác hơn. */}
                  Ensure that the uploaded images are of high resolution to
                  avoid breaking when cropping and to support a more accurate
                  diagnostic process.
                </div>
              </div>
              <div className="img__diagnoises--rule">
                <div className="img__diagnoises--guild">
                  <img
                    className="img__diagnoises--icon"
                    src={ZoomAcneImg}
                    alt="zoom_acne"
                  />
                </div>
                <div className="img_diagnoises--text">
                  {/* Sử dụng chức năng phóng to ảnh để tránh việc vật thể mụn quá
                  nhỏ. Điều này sẽ cải thiện độ chính xác của quá trình chuẩn
                  đoán. */}
                  Use the zoom function on images to avoid acne objects being
                  too small. This will improve the accuracy of the diagnostic
                  process.
                </div>
              </div>

              <div className="img__diagnoises--rule">
                <div className="img__diagnoises--guild">
                  <img
                    className="img__diagnoises--icon"
                    src={LimitedImg}
                    alt="high_quality"
                  />
                </div>
                <div className="img_diagnoises--text">
                  {/* Hạn chế tải lên nhiều ảnh cùng lúc để tối ưu hóa tốc độ xử lý
                  và kết quả chuẩn đoán. */}
                  Limit uploading multiple images at once to optimize processing
                  speed and diagnostic results.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadAndCropImage;
