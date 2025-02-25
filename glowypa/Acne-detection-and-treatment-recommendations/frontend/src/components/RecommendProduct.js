import React, { useState, useEffect, useCallback } from "react";
import "./css/RecommendProduct.css";
import ruamat from "../assets/images/celtafill.png";
import favourit from "../assets/icons/favourite-stroke-rounded.svg";
import {
  updateLike
} from "../redux/action/actions";
import { useSelector, useDispatch } from "react-redux";

const convertDropboxUrl = (url) => {
  if (!url) return '';
  if (!url.includes('dropbox.com')) return url;
  let newUrl = url.replace('www.dropbox.com', 'dl.dropboxusercontent.com');
  if (!newUrl.includes('dl=1')) {
    newUrl = newUrl.includes('?') ? 
      `${newUrl}&dl=1` : 
      `${newUrl}?dl=1`;
  }
  return newUrl;
};

const ProductImage = ({ src }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [imgSrc, setImgSrc] = useState('');
  const [error, setError] = useState(false);


 
  useEffect(() => {
    setIsLoading(true);
    setError(false);
    const convertedSrc = convertDropboxUrl(src);
    setImgSrc(convertedSrc);
    const img = new Image();
    img.src = convertedSrc;
    img.onload = () => {
      console.log("Image loaded successfully");
      setIsLoading(false);
    };

    img.onerror = () => {
      console.error("Image failed to load:", convertedSrc);
      setError(true);
      setIsLoading(false);
    };
    return () => {
      img.onload = null;
      img.onerror = null;
    };
  }, [src]);

  if (error) {
    return (
      <div className="rcm__product--img error">
        <div className="error-message">
          Image failed to load
        </div>
      </div>
    );
  }

  return (
    <div className="rcm__product--img">
      {isLoading && (
        <div className="loading-spinner"></div>
      )}
      {!isLoading && (
        <img
          src={imgSrc}
          alt="product"
          onError={(e) => {
            console.error("Image error:", e);
            setError(true);
          }}
        />
      )}
    </div>
  );
};

const Recommend = React.memo(({recommend}) => {
  const dispatch = useDispatch();
  
  const [rcm, setRcm] = useState(recommend); // Changed to use setRcm
  const [likedProducts, setLikedProducts] = useState([]);

  const handleLike = useCallback((name, timeOfDay, index) => {
    if (!likedProducts.includes(name)) {
      dispatch(updateLike(recommend._id, name))
      setLikedProducts(prev => [...prev, name]);
        setRcm(prevRcm => {
        const newRcm = {...prevRcm};
        const routineArray = newRcm.daily_routine[timeOfDay];
        routineArray[index] = {
          ...routineArray[index],
          like: (parseInt(routineArray[index].like) + 1).toString()
        };
        return newRcm;
      });
    }
  }, [likedProducts]);

  if (!rcm?.daily_routine) {
    return <div>No recommendation data available</div>;
  }

  return (
    <div className="rcm__bg letter-border">
      <div>Skincare Regimen:</div>
      <div className="tag__rcm--morning box--shadow-btn">Morning</div>
      <div className="rcm__product">
        {rcm.daily_routine.morning.map((item, index) => (
          <div className="rcm__product--item box--shadow-btn" key={index}>
            <ProductImage src={item.image} />
            <div className="rcm__product--details">
              <div className="rcm__product--details-name">{item.product}</div>
              <div className="rcm__product--details-tag">{item.step}</div>
              <div className="rcm__product--details-usage">{item.usage}</div>
              <div className="rcm__product--details-func">
                <div className="like">{item.like}</div>
                <button 
                  className={`rcm_like box--shadow-btn ${likedProducts.includes(item.product) ? 'liked' : ''}`}
                  onClick={() => !likedProducts.includes(item.product) && handleLike(item.product, 'morning', index)}
                  disabled={likedProducts.includes(item.product)}
                >
                  <img src={favourit} alt="favourite" />
                </button>
                <a 
                  href={item.link} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="buy-link"
                >
                  <button className="rcm_buy box--shadow-btn">Buy</button>
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="tag__rcm--evening box--shadow-btn">Evening</div>
      <div className="rcm__product">
        {rcm.daily_routine.evening.map((item, index) => (
          <div className="rcm__product--item box--shadow-btn" key={index}>
            <ProductImage src={item.image} />
            <div className="rcm__product--details">
              <div className="rcm__product--details-name">{item.product}</div>
              <div className="rcm__product--details-tag">{item.step}</div>
              <div className="rcm__product--details-usage">{item.usage}</div>
              <div className="rcm__product--details-func">
                <div className="like">{item.like}</div>
                <button 
                  className={`rcm_like box--shadow-btn ${likedProducts.includes(item.product) ? 'liked' : ''}`}
                  onClick={() => !likedProducts.includes(item.product) && handleLike(item.product, 'evening', index)}
                  disabled={likedProducts.includes(item.product)}
                >
                  <img src={favourit} alt="favourite" />
                </button>
                <a 
                  href={item.link} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="buy-link"
                >
                  <button className="rcm_buy box--shadow-btn">Buy</button>
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="tag__rcm--end box--shadow-btn"></div>
    </div>
  );
});

export default Recommend;
