import ProblemInfo from "./components/ProblemInfo";
import Editer from "./components/Editer";
import AIAnswer from "./components/AIAnswer";
import AIFeedback from "./components/AIFeedback";
import { useLocation } from "react-router-dom";
import { useState } from "react";
import "./codingProblem.css";

function CodingProblem({ getUserInfo, updateUserInfo }) {
  const location = useLocation();
  console.log(location)
  const data = location.state.data;
  const [userAnswer, setUserAnswer] = useState("");
  const [AIFeedback, setAIFeedBack] = useState("");

  const updateUserAnswer = (newAnswer) => {
    setUserAnswer(newAnswer);
  };
  // 제한시간이 끝나거나 제출한 경우
  const updateAIFeedback = (newFeedback) => {
    // 피드백 불러오기
    setAIFeedBack(newFeedback);
  };

  return (
    <div>
      <ProblemInfo
        getUserInfo={getUserInfo}
        updateUserInfo={updateUserInfo}
      />
      <div>
        <Editer />
        <AIAnswer />
      </div>
      <div>
        <AIFeedback
          userAnswer={userAnswer}
          updateAIFeedback={updateAIFeedback}
        />
      </div>
    </div>
  );
}

export default CodingProblem;
