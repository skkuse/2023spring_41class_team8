import React, { useEffect, useState } from "react";
import "./AIFeedback.css";

function AIFeedback({ userAnswer, updateAIFeedback , correct, late}) {
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
        if (late){
          setFeedbackText("정답입니다.\n 다음번에는 더 자신있게 제출 버튼을 눌러주세요!")
        }
        else{
          setFeedbackText("정답입니다.\n 당신이 GPT를 이겼습니다!")
        }
      }
      else{
        if (late){
          setFeedbackText("오답입니다.\n 피드백을 보고 다음번에 다시 도전해 보세요!")
        }
        else{
          setFeedbackText("오답입니다.\n 너무 성급했던 것 아닐까요? 피드백을 보고 다음번엔 꼭 풀어보아요.")
        }
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
