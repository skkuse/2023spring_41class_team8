import React, { useEffect, useState } from "react";
import "./AIFeedback.css";

function AIFeedback({ userAnswer, updateAIFeedback }) {
  const [feedback, setFeedback] = useState([""]);

  const parseAIFeedbackByLine = (feedback) => {
    let lines = feedback.split("\n");
    setFeedback(lines);
  };

  useEffect(() => {
    parseAIFeedbackByLine(updateAIFeedback);
  }, [updateAIFeedback]);

  return (
    <div className="AIFeedbackContainer">
      <h3>AI의 피드백</h3>
      <pre className="AIFeedbackText">{updateAIFeedback}</pre>
    </div>
  );
}

export default AIFeedback;
