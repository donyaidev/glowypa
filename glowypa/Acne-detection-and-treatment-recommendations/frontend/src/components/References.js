import React from 'react';
import "./css/Chatbox.css";

const References = ({ chatMessages, index }) => {
  return (
    <>
      {chatMessages[index].question_related_acne_medical == true && (
        <>
          <h3>References:</h3>
          {chatMessages[index].reference_doc.map((item, index) => (
            <p className="references" key={index}>
              [{index + 1}] {item["file_name"]} - page: {item["page"]}
            </p>
          ))}
        </>
      )}
    </>
  );
};

export default References;