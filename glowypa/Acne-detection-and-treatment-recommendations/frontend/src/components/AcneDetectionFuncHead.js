import { ReactComponent as UploadImg } from "../assets/icons/upload-img.svg";
import "./css/AcneDetectionFuncHead.css";
import ImgDiagnoisis from "./ImgDiagnoisis";
import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";
import { activeDialogUploadImg } from "../redux/action/actions";
const AcneDetectionFuncHead = ({
  handleChangeSelectedImage,
}) => {
  const dispatch = useDispatch();
  const images = useSelector((state) => state.acnePredictionDaily.images);
  const handleOpenUploadImgDialog = () => {
    dispatch(activeDialogUploadImg());
  };

  return (
    <>
      <div
        className="acne__detection--tool-input-image box--shadow-btn"
        onClick={() => handleOpenUploadImgDialog()}
        style={{ cursor: "pointer" }}
      >
        <UploadImg className="icon--element-arrow" />
        <p>Click upload image</p>
      </div>
      <div className="acne__detection--tool-image-tool-scroll">
        <div className="acne__detection--tool-images">
          {images.map((object, index) => (
            <ImgDiagnoisis
              key = {index}
              tag="1"
              image_id = {object.image_id}
              base64Image= {object.image_base64}
              handleChangeSelectedImage ={handleChangeSelectedImage}
           />
          ))}
          {Array.from({ length: 4 - images.length }, (_, index) => (
            <ImgDiagnoisis
              key={`empty-${index}`}
              tag="1" 
              id_img={null}
              base64Image= {null}
              onDelete={() => {}}
            />
          ))}
        </div>
      </div>
      <div className="acne__detection--tool-model-logo-mode">
        <div className="acne__detection--tool-model-logo"></div>
      </div>
    </>
  );
};

export default AcneDetectionFuncHead;
