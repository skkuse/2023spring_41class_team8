import React, { useEffect, useState } from "react";
import "./ProblemInfo.css";
function ProblemInfo({problemData, isTimerRunning}) {
  // 문제 데이터와 타이머 상태 변수를 선언
  const data = problemData;
  const [timer, setTimer] = useState(0);
  
  // 컴포넌트가 마운트될 때 타이머를 시작
  useEffect(() => {
    // 1초마다 타이머 값을 증가시키는 인터벌을 설정
    const interval = setInterval(() => {
      setTimer((prevTimer) => prevTimer + 1);
    }, 1000);

    if (!isTimerRunning) {
      clearInterval(interval); // 타이머 정지
    }
    // 컴포넌트가 언마운트될 때 인터벌을 정리
    return () => {
      clearInterval(interval);
    };
  }, [isTimerRunning]);

  return (
    <div className="coding_problem_container">
      <div className="coding_problem_title">
        문제 {data.pid + 1}. {data.title} (Level: {data.level})
        <div className="coding_problem_timer">{timer}s</div>
      </div>
      <div className="coding_problem_content_info">
        <div className="coding_problem_content_text">{data.content}</div>
      </div>
      <div className="coding_problem_inputoutput">
        <div className="coding_problem_label">Input</div>
        <div className="coding_problem_content_input">{data.input}</div>
        <div className="coding_problem_label">Output</div>
        <div className="coding_problem_content_output">{data.output}</div>
      </div>
    </div>
  );
}

export default ProblemInfo;
