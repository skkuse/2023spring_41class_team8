import React, { useEffect, useState } from "react";
import "./AIFeedback.css";

function AIFeedback({ userAnswer, updateAIFeedback , correct}) {
  const [feedback, setFeedback] = useState([""]);

  const parseAIFeedbackByLine = (feedback) => {
    let lines = feedback.split("\n");
    setFeedback(lines);
  };

  useEffect(() => {
    parseAIFeedbackByLine(updateAIFeedback, correct);
  }, [updateAIFeedback]);

  const feedbackColor = correct ? "blue" : "red";
  const feedbackText = correct ? "정답입니다" : "오답입니다";

  return (
    <div className="AIFeedbackContainer">
      <h3>AI의 피드백</h3>
      <p className="AIFeedbackText" style={{ color: feedbackColor }}>
        {feedbackText}
      </p>
      <pre className="AIFeedbackText">{updateAIFeedback}</pre>
    </div>
  );
}

export default AIFeedback;
