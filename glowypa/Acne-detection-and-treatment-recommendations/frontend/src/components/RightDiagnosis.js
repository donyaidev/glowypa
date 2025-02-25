// Diagnosis.js
import React, { useState } from "react";
import "./css/RightDiagnosis.css";
import { ReactComponent as ArrowLeft } from '../assets/icons/arrow-left.svg';
import { ReactComponent as ArrowRight } from '../assets/icons/arrow-right.svg';
import AcneDetection from "../components/AcneDetection";
import Chatbox from "./Chatbox";

export default function RightDiagnosis() {
    const [onOffChat, setOnOffChat] = useState(false);

    const toggleOnOffChat = () => {
        setOnOffChat(prevState => !prevState);
    };

    return (
        <div className="right-diagnosis">
            <div className={onOffChat ? "chatbox display-hidden box--shadow-btn" : "chatbox box--shadow-btn"} >
                <Chatbox />
            </div>
            {
                onOffChat ? (
                    <div className="button-close-open-chat button-close-open-chat__close">
                        <button className="chat-open__btn" onClick={() => toggleOnOffChat()}>
                            <ArrowRight className="icon--element-arrow" />
                        </button>
                    </div>
                ) : (
                    <div className="button-close-open-chat">
                        <button className="chat-close__btn" onClick={() => toggleOnOffChat()}>
                            <ArrowLeft className="icon--element-arrow" />
                        </button>
                    </div>
                )
            }
            <div className="acne-detection">
                <AcneDetection />
            </div>
        </div>
    );
};
