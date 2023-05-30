import React from "react";
import "./AIFeedback.css";

function AIFeedback({ userAnswer, updateAIFeedback }) {
  return (
    <div className="AIFeedbackContainer">
      <h3>AI의 피드백</h3>
      <p className="AIFeedbackText">{updateAIFeedback}</p>
    </div>
  );
}

export default AIFeedback;