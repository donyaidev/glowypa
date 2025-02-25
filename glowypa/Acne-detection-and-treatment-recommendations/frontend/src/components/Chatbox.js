import React, { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown"; // Import ReactMarkdown
import remarkGfm from "remark-gfm"; // Import remark-gfm
import rehypeHighlight from "rehype-highlight"; // Import rehype-highlight
import "highlight.js/styles/github.css"; // Import theme for code (can change the theme)
import "./css/Chatbox.css";
import { ReactComponent as Send } from "../assets/icons/send.svg";
import LoadingGifIcon from "../assets/loading/loading_plus_icon.gif";
import { ReactComponent as Gpt } from "../assets/icons/gpt.svg";
import { ReactComponent as RDetection } from "../assets/icons/result_detect.svg";
import { ReactComponent as Db } from "../assets/icons/database.svg";
import { useSelector, useDispatch } from "react-redux";
import { ReactComponent as Advice } from "../assets/icons/advice_treatment.svg";
import { ReactComponent as Monitor } from "../assets/icons/monitor.svg";
import { ReactComponent as AcneDiagnosis } from "../assets/icons/acne_diagnosis.svg";
import {
  chatboxRequestion,
  chatboxRag,
  chatboxMedicalDb,
  RecommendProduct,
  postFavourite
} from "../redux/action/actions";
import References from "./References";
import Recommend from "./RecommendProduct";
import FavouritRoutine from "./FavouritRoutine"
const Chatbox = () => {
  const dispatch = useDispatch();
  const predicted_images = useSelector(
    (state) => state.acnePredictionDaily.predicted_images
  );
  const chatMessages = useSelector((state) => state.adviceChatbox.chatMessage);
  const rag = useSelector((state) => state.adviceChatbox.rag);
  const db = useSelector((state) => state.adviceChatbox.medicaldb);
  const user = useSelector((state) => state.user.user);
  const display_status = useSelector(
    (state) => state.adviceChatbox.changeDisplay
  );
  const loadingChat = useSelector((state) => state.adviceChatbox.loading);

  const [message, setMessage] = useState("");
  const [typingMessage, setTypingMessage] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const lastMessageRef = useRef(null);
  const [recommendMessage, setRecommendMessage] = useState("");

  const toggleOnOffRag = () => {
    dispatch(chatboxRag());
  };

  const toggleOnOffMedicalDb = () => {
    dispatch(chatboxMedicalDb());
  };

  const saveFavourit = (chatItem) => {
    console.log('hi')
    dispatch(postFavourite(chatItem));
  };

  const sendChatMessage = (message) => {
    const newMessage = {
      user_id: user.id,
      role: "user",
      message: message,
      rag: rag,
      db: db,
      history_chat: chatMessages,
    };
    dispatch(chatboxRequestion(newMessage));
  };

  const sendRecommend = (messageBot, recommendMessage = "") => {
    const newMessage = {
      user_id: user.id,
      role: "bot",
      type: "chat",
      message: messageBot,
      messageUser: recommendMessage,
      rag: rag,
      db: db,
      history_chat: chatMessages,
    };
    dispatch(RecommendProduct(newMessage));
  };

  const handleSendClick = () => {
    if (message.trim() !== "") {
      sendChatMessage(message);
      setMessage("");
    }
  };

  const handleRecommend = () => {
    const messageBot =
      "Waiting... Glowypa is going to suggest a skincare regimen for you.";
    sendRecommend(messageBot,recommendMessage);
    setRecommendMessage("")
  };

  const handleKeyPress = (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey &&
      !event.ctrlKey &&
      !event.altKey &&
      !event.metaKey &&
      !loadingChat
    ) {
      event.preventDefault();
      handleSendClick();
    }
  };

  const handleKeyPressRCM = (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey &&
      !event.ctrlKey &&
      !event.altKey &&
      !event.metaKey &&
      !loadingChat
    ) {
      event.preventDefault();
      handleRecommend();
    }
  };

  // Typing effect logic
  useEffect(() => {
    if (
      chatMessages.length > 0 &&
      chatMessages[chatMessages.length - 1].role === "bot"
    ) {
      const botMessage = chatMessages[chatMessages.length - 1];
      const botMessageText = botMessage.message || "";
      setTypingMessage(""); // Clear previous message
      setIsTyping(true);

      let index = 0;

      if (botMessageText.length > 0) {
        setTypingMessage(botMessageText[0]);
        index = 1; // Start typing from the second character
      }

      const typingInterval = setInterval(() => {
        if (index < botMessageText.length) {
          setTypingMessage((prev) => prev + botMessageText[index]);
          index++;
        } else {
          clearInterval(typingInterval);
          setIsTyping(false);

          // Update the last message to include references
          const updatedMessages = [...chatMessages];
          updatedMessages[updatedMessages.length - 1] = {
            ...botMessage,
            references: true, // Add references flag to the last message
          };
          dispatch({ type: "UPDATE_CHAT_MESSAGES", payload: updatedMessages }); // Dispatch updated messages
        }
      }, 1); // Adjust typing speed here (30ms per character)

      return () => clearInterval(typingInterval);
    }
  }, [chatMessages]);

  const [favouritDialog, setFavouritDialog]  = useState(false)
  const handleFavouritDialog = () => {
    setFavouritDialog(!favouritDialog)
  }


  const [savedIds, setSavedIds] = useState([]); // Thêm state này
  const chatMessagesFa = useSelector((state) => state.favoriteRoutine.chatMessage);
  
  useEffect(() => {
    let ids = [];
    for (let i = 0; i < chatMessagesFa.length; i++) {
      let chatItem = chatMessagesFa[i];
      ids.push(chatItem.recommend.id);
    }
    setSavedIds(ids); 
  }, [chatMessagesFa]);

  return (
    <>
      {favouritDialog && (<FavouritRoutine handleFavouritDialog={handleFavouritDialog}/>)}
      {chatMessages.length === 0 ? (
        <div className="chatbox__introduction">
          <div className="chatbox__say-hello ban--select">
            <span>
              👋 Hi, {user.first_name} {user.last_name}
            </span>
            <p>How Can I help you today?</p>
          </div>
          <div className="chatbox__introduction-func">
            <div className="chatbox__introduction-func-item">
              <AcneDiagnosis
                className="icon--element"
                style={{ color: "orange" }}
              />
              <span className="ban--select">Acne Diagnosis</span>
            </div>
            <div className="chatbox__introduction-func-item">
              <Advice className="icon--element" />
              <span className="ban--select">Treatment Advice</span>
            </div>
            <div className="chatbox__introduction-func-item">
              <Monitor className="icon--element" style={{ color: "purple" }} />
              <span className="ban--select">Skin Health Monitor</span>
            </div>
          </div>
        </div>
      ) : (
        <div className="chatbox__message">
          {chatMessages.map((chatItem, index) => (
            <div
              key={index}
              className={`chatbox__message--${chatItem.role}`}
              ref={index === chatMessages.length - 1 ? lastMessageRef : null}
            >
              {chatItem.role === "user" ? (
                <div className="message">
                  <p>{chatItem.message || ""}</p>
                </div>
              ) : (
                <div className="chatbox__message--bot">
                  <div className="chatbox__message--bot-info">
                    <div className="chatbox__message--bot-avatar"></div>
                    <div className="chatbox__message--bot-name">
                      <span>Glowypa</span>
                    </div>
                    {chatItem.rag && (
                      <div className="chatbox__message--bot-tag">
                        <span>GPT4o</span>
                      </div>
                    )}
                    {/* {chatItem.db && (
                      <div className="chatbox__message--bot-tag">
                        <span>Medical Record</span>
                      </div>
                    )} */}
                  </div>

                  {chatItem.type == "chat" && (
                    <div className="chatbox__message--mes">
                      {index === chatMessages.length - 1 && isTyping ? (
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          rehypePlugins={[rehypeHighlight]}
                        >
                          {typingMessage}
                        </ReactMarkdown>
                      ) : (
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          rehypePlugins={[rehypeHighlight]}
                        >
                          {chatItem.message || ""}
                        </ReactMarkdown>
                      )}
                    </div>
                  )}
                  {chatItem.type == "recommend" && (
                    <>
                      <Recommend recommend={chatItem.recommend} />
                      <div className="chatbox__message--mes">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          rehypePlugins={[rehypeHighlight]}
                        >
                          {chatItem.message || ""}
                        </ReactMarkdown>
                        <div className="save__treatment-routine">
                          <button 
                            onClick={() => saveFavourit(chatItem)} 
                            disabled={savedIds.includes(chatItem.recommend._id)}
                            className={`save__treatment-btn box--shadow-btn ${savedIds.includes(chatItem.recommend._id) ? 'disabled' : ''}`}
                          >
                            <span className="span-clor">Save</span>
                          </button>
                        </div>
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>
          ))}
          {loadingChat && (
            <div className="chatbox__message--bot">
              <div className="chatbox__message--bot-info">
                <div className="chatbox__message--bot-avatar"></div>
                <div className="chatbox__message--bot-name">
                  <span>Glowypa</span>
                </div>
                {rag && (
                  <div className="chatbox__message--bot-tag">
                    <span>GPT4o</span>
                  </div>
                )}
                {/* {db && (
                  <div className="chatbox__message--bot-tag">
                    <span>Medical Record</span>
                  </div>
                )} */}
              </div>
              <div className="typing-indicator">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
              </div>
            </div>
          )}
        </div>
      )}

      <div className="chatbox__send">
        {!loadingChat ? (
          // <button
          //   className="chatbox__rcm-products box--shadow-btn"
          //   onClick={handleRecommend}
          //   aria-label="Send Recommend"
          // ></button>
          <div
            className="chatbox__rcm-products box--shadow-btn"
            // onClick={handleRecommend}
            aria-label="Send Recommend"
          >
            <button className="rcm-btn box--shadow-btn" onClick={handleRecommend}>Suggest Regimen</button>
            <textarea 
                className="rcm-textarea box--shadow-btn"
                placeholder="Describe your routine daily: work, time, skin..."
                onChange={(e) => setRecommendMessage(e.target.value)}
                onKeyPress={handleKeyPressRCM}
            ></textarea>
        </div>
        ) : (
          ""
        )}
        <div className="chatbox__send--input">
          <textarea
            className="chatbox__send--text-input"
            placeholder="Ask me anything about your skin ..."
            name="text-input"
            id="text-input"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
          ></textarea>
        </div>
        
        <div className="chatbox__send--func">
          
          <div className="chatbox__send--advance">
            
            <div className="chatbox__send--rag chatbox__send--advance-position">
              <div className="chatbox__send--func ">
                <button onClick={handleFavouritDialog} className="favourit__btn box--shadow-btn">Favourit Regimen</button>
              </div>
              <Gpt className="icon-advance" />
              GPT4o
              {loadingChat ? (
                <div id={rag ? "on" : ""} className="button-on-off">
                  <div
                    id={rag ? "on-circle" : ""}
                    className="circle-on-off"
                  ></div>
                </div>
              ) : (
                <div
                  id={rag ? "on" : ""}
                  onClick={toggleOnOffRag}
                  className="button-on-off"
                >
                  <div
                    id={rag ? "on-circle" : ""}
                    className="circle-on-off"
                  ></div>
                </div>
              )}
            </div>
            
            {/* <div className="chatbox__send--db chatbox__send--advance-position">
              <RDetection className="icon-advance" />
              Medical Record
              {loadingChat ? (
                <div id={db ? "on" : ""} className="button-on-off">
                  <div
                    id={db ? "on-circle" : ""}
                    className="circle-on-off"
                  ></div>
                </div>
              ) : (
                <div
                  id={db ? "on" : ""}
                  onClick={toggleOnOffMedicalDb}
                  className="button-on-off"
                >
                  <div
                    id={db ? "on-circle" : ""}
                    className="circle-on-off"
                  ></div>
                </div>
              )}
            </div> */}
          </div>
          <button
            className="chatbox__send--button"
            onClick={handleSendClick}
            aria-label="Send Message"
          >
            {loadingChat ? (
              <img
                src={LoadingGifIcon}
                className="icon-loading"
                alt="Loading"
              />
            ) : (
              <Send className="icon-send" />
            )}
          </button>
        </div>
      </div>
    </>
  );
};

export default Chatbox;
