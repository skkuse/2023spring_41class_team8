import React, { useEffect, useState } from "react";
import ProblemInfo from "./components/ProblemInfo";
import Editer from "./components/Editer";
import AIAnswer from "./components/AIAnswer";
import { codingProblems } from "../../codingProblemData";
import { correctAnswer } from "../../correctAnswer";
import AIFeedback from "./components/AIFeedback";
import { languageOptions } from "../../languageOption";
import { useLocation } from "react-router-dom";
import { defineTheme } from "./components/editerStyle/defineTheme";
import useKeyPress from "./components/editerStyle/useKeyPress";
import "./codingProblem.css";

const pythonDefault = `여기에 입력하세요`;

function CodingProblem({ getUserInfo, updateUserInfo }) {
  // 필요한 상태 변수들을 선언
  const location = useLocation();
  const data = location.state.data;
  const [userAnswer, setUserAnswer] = useState("");
  const [Feedback, setAIFeedBack] = useState("잘했어요");
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [timer, setTimer] = useState(0);

  const [code, setCode] = useState(pythonDefault);
  const [AIcode, setAICode] = useState(correctAnswer[0].answer);
  const [theme, setTheme] = useState("oceanic-next");
  const [language, setLanguage] = useState(languageOptions[0]);

  const [isBlurred, setIsBlurred] = useState(true);

  const enterPress = useKeyPress("Enter");
  const ctrlPress = useKeyPress("Control");

  // Enter, Ctrl 키를 눌렀을 때의 동작을 처리
  useEffect(() => {
    if (enterPress && ctrlPress) {
      console.log("enterPress", enterPress);
      console.log("ctrlPress", ctrlPress);
    }
  }, [ctrlPress, enterPress]);

  // 초기 테마 설정을 수행
  useEffect(() => {
    defineTheme("oceanic-next").then((_) =>
      setTheme({ value: "oceanic-next", label: "Oceanic Next" })
    );
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setTimer((prevTimer) => prevTimer + 1);
    }, 1000);

    // 도달하면 handleSaveAnswer 실행 및 타이머 정리
    if (timer === data.level*20) {
      handleSaveAnswer();
      clearInterval(interval);
    }

    return () => {
      clearInterval(interval);
    };
  }, [timer]);

  // 코드 변경 시 호출되는 함수
  const onChange = (action, value) => {
    switch (action) {
      case "code": {
        setCode(value);
        break;
      }
      default: {
        console.warn("case not handled!", action, value);
      }
    }
  };

  // 사용자 답안 저장을 처리하는 함수
  const handleSaveAnswer = () => {
    setIsSubmitted(true);
    updateUserAnswer(code);
  };
  // 코드 숨기기/보이기 기능을 처리하는 함수
  const handleBlur = () => {
    setIsBlurred(!isBlurred);
  };
  // 사용자 답안 업데이트를 수행하는 함수
  const updateUserAnswer = (newAnswer) => {
    setUserAnswer(newAnswer);
    // 제한시간이 끝나거나 제출한 경우
  };
  // AI 피드백 업데이트를 수행하는 함수
  const updateAIFeedback = (newFeedback) => {
    // 피드백 불러오기
    setAIFeedBack(newFeedback);
  };

  return (
    <div className="coding_problem_container">
      <ProblemInfo problemData={data} />
      <div className="coding_problem_content">
        <div className="coding_problem_editor">
          <Editer
            code={code}
            onChange={onChange}
            language={language?.value}
            theme={theme.value}
          />
          <button onClick={handleSaveAnswer}>제출</button>
        </div>

        <div className="coding_problem_aianswer">
          <AIAnswer
            code={AIcode}
            onChange={onChange}
            language={language?.value}
            theme={theme.value}
            isBlurred={isBlurred}
          />
          <button onClick={handleBlur}>코드 숨기기</button>
        </div>
      </div>
      <div className="coding_problem_feedback">
        {isSubmitted && (
          <AIFeedback userAnswer={userAnswer} updateAIFeedback={Feedback} />
        )}
      </div>
    </div>
  );
}

export default CodingProblem;
