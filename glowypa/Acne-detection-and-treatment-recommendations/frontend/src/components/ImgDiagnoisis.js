// import React from "react";
// import "./ImgDiagnoisis.css";
// import { ReactComponent as MultipleImg } from "../assets/icons/multiple.svg";

// const ImgDiagnoisis = ({
//   base64,
//   id_img,
//   onDelete,
//   tag,
//   handleChangeSelectedImage,
//   base64Image,
// }) => {
//     let active_img_chosend = 0;
//     console.log(base64Image)
//     if(base64Image && base64Image != 0){
//         active_img_chosend = base64Image.id_image;
//     } else {
//         active_img_chosend = 0;
//     }
//   return (
//     <div
//       className="acne__detection--tool-image box--shadow-btn"
//       onClick={base64 != null && tag == 1 ? () => handleChangeSelectedImage(base64) : undefined}
//     >
//       {" "}
//       {tag != 1 ? (
//         <button
//           className="delete-btn box--shadow-btn"
//           onClick={() => onDelete(base64.id_img)}
//         >
//           <MultipleImg className="icon--element-mul" />
//         </button>
//       ) : null}
//       <div className={active_img_chosend == id_img ? "acne-image active-image" : "acne-image"}>
//         {base64 ? (
//           <img className="responsive-image" src={base64.image_base64} alt="Diagnosis" />
//         ) : null}
//       </div>
//     </div>
//   );
// };

// export default ImgDiagnoisis;

import React from "react";
import "./css/ImgDiagnoisis.css";
import { ReactComponent as MultipleImg } from "../assets/icons/multiple.svg";
import { useSelector, useDispatch } from "react-redux";
import { detectionAcneDailyActiveShow } from "../redux/action/actions";
const ImgDiagnoisis = ({
  onDelete,
  tag,
  handleChangeSelectedImage,
  image_id,
  base64Image,
}) => {
  const dispatch = useDispatch();
  const image_active = useSelector((state) => state.acnePredictionDaily.image_active);
  const handleChangeActiveImage = (image_id) => {
    dispatch(detectionAcneDailyActiveShow(image_id));
  }
  return (
    <div className="acne__detection--tool-image box--shadow-btn" onClick={base64Image && tag == 1 ? () => handleChangeActiveImage(image_id) : null}>
      {tag != 1 ? (
        <button
          className="delete-btn box--shadow-btn"
          onClick={() => onDelete(image_id)}
        >
          <MultipleImg className="icon--element-mul" />
        </button>
      ) : null}
      {base64Image ? (
        <div className={image_active == image_id && tag == 1 ? "acne-image active-image box--shadow-btn" : "acne-image"} >
          <img className="responsive-image" src={base64Image} alt="Diagnosis" />
        </div>
      ) : (
        <div className="acne-image"></div>
      )}
    </div>
  );
};

export default ImgDiagnoisis;
