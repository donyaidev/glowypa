import React, { useState, useEffect, useRef } from "react";
import { useSelector, useDispatch } from "react-redux";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import "./css/FavouritRoutine.css";
import Recommend from "./RecommendProduct";
import {
  deleteFavourite
} from "../redux/action/actions";
const FavouriteRoutine = ({handleFavouritDialog}) => {
  const dispatch = useDispatch();
  const [isTyping, setIsTyping] = useState(false);
  const [typingMessage, setTypingMessage] = useState("");
  const lastMessageRef = useRef(null);

  const predicted_images = useSelector(
    (state) => state.acnePredictionDaily.predicted_images
  );
  const chatMessages = useSelector((state) => state.favoriteRoutine.chatMessage);
  // Scroll to bottom when new messages arrive
  useEffect(() => {
    if (lastMessageRef.current) {
      lastMessageRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [chatMessages]);
  const deleteFavourit = (chatItem) => {
    dispatch(deleteFavourite(chatItem));
  };
  
  return (
    <div className="favourit__routine--bg">
      
      <div className="favourit__child-bg">
      <div className="favourit-header  box--shadow-btn">Favorite Routine</div>
        <button onClick={handleFavouritDialog} className="fvrcls__btn box--shadow-btn">X</button>
        {chatMessages.length === 0 ? (
          <div className="chatbox__introduction">
            <div className="chatbox__say-hello ban--select">
              <span>👋 Hi</span>
              <p>How Can I help you today?</p>
            </div>
          </div>
        ) : (
          <div className="chatbox__message-fvr">
            {chatMessages.map((chatItem, index) => (
              <div
                key={index}
                className={`chatbox__message-fvr--bot`}
                ref={index === chatMessages.length - 1 ? lastMessageRef : null}
              >
                {chatItem.role === "user" ? (
                  <div className="message">
                    <p>{chatItem.message || ""}</p>
                  </div>
                ) : (
                  <div className="chatbox__message-fvr--bot">
                    <div className="chatbox__message-fvr--bot-info">
                      <div className="chatbox__message-fvr--bot-avatar"></div>
                      <div className="chatbox__message-fvr--bot-name">
                        <span>Glowypa</span>
                      </div>
                      {chatItem.rag && (
                        <div className="chatbox__message-fvr--bot-tag">
                          <span>GPT4o</span>
                        </div>
                      )}
                    </div>

                    {chatItem.type === "chat" && (
                      <div className="chatbox__message-fvr--mes">
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            rehypePlugins={[rehypeHighlight]}
                          >
                            {chatItem.message || ""}
                          </ReactMarkdown>
                      </div>
                    )}

                    {chatItem.type === "recommend" && (
                      <>
                        <Recommend recommend={chatItem.recommend} />
                        <div className="chatbox__message-fvr--mes">
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            rehypePlugins={[rehypeHighlight]}
                          >
                            {chatItem.message || ""}
                          </ReactMarkdown>
                          <div className="save__treatment-routine">
                            <button onClick={() => deleteFavourit(chatItem)}  className="save__treatment-btn box--shadow-btn">Delete</button>
                          </div>
                        </div>
                      </>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default FavouriteRoutine;
