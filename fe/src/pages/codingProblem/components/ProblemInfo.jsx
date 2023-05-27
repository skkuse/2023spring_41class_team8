import { useState } from "react";
import { useLocation } from "react-router-dom";
//import "./ethicsProblem.css";


function ProblemInfo({ getUserInfo, updateUserInfo }) {
  const location = useLocation();
  console.log(location)
  const data = location.state.data;

  return (
    <div className="coding_problem_container">
      <div className="coding_problem_title">
        윤리 문제 {data.pid + 1}. {data.title}
      </div>
      <div className="coding_problem_content">
        <div className="coding_problem_content_text">{data.content}</div>
      </div>
      <div className="coding_problem_options">
        <div className="coding_problem_option">
          <div className="coding_problem_option_text">A. {data.optionA}</div>
          <button
            className="coding_problem_option_button"
            onClick={onClickButton}>
            Click
          </button>
        </div>
        <div className="coding_problem_title">VS</div>
        <div className="coding_problem_option">
          <div className="coding_problem_option_text">B. {data.optionB}</div>
          <button
            className="coding_problem_option_button"
            onClick={onClickButton}>
            Click
          </button>
        </div>
      </div>
      <div className="coding_problem_options">
        <div className="coding_result_option">
          <div className="coding_problem_option_text">A 선택 시 결과</div>
          <div className="coding_problem_option_button">결과 내용</div>
        </div>
        <div className="coding_result_option">
          <div className="coding_problem_option_text">B 선택 시 결과</div>
          <div className="coding_problem_option_button">결과 내용</div>
        </div>
      </div>
    </div>
  );
}

export default ProblemInfo;
