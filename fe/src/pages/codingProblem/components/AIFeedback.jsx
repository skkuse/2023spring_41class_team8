import React, { useEffect, useState } from "react";
import "./AIFeedback.css";

function AIFeedback({ userAnswer, updateAIFeedback , correct}) {
  const [feedback, setFeedback] = useState([""]);
  const [feedbackText, setFeedbackText] = useState("확인 중입니다.");
  const parseAIFeedbackByLine = (feedback) => {
    let lines = feedback.split("\n");
    setFeedback(lines);
  };

  useEffect(() => {
    parseAIFeedbackByLine(updateAIFeedback, correct);
    if (updateAIFeedback!="잠시만 기다려 주세요"){
      if (correct){
        setFeedbackText("정답입니다.")
      }
      else{
        setFeedbackText("오답입니다.")
      }
    }
   
  }, [updateAIFeedback, correct]);

  const feedbackColor = correct ? "blue" : "red";

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
