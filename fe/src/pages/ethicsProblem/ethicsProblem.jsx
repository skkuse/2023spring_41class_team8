import { useState } from "react";
import { useLocation } from "react-router-dom";
import "./ethicsProblem.css";

function EthicsProblem({ getUserInfo, updateUserInfo }) {
  const location = useLocation();
  const data = location.state.data;

  const [result, setResult] = useState([]);

  const onClickButton = () => {
    let userInfo = getUserInfo();
    updateUserInfo({
      ...userInfo,
      solvedEthicsProblems: [...userInfo.solvedEthicsProblems, data.pid],
    });
    // TODO: 해당 선택지 선택 시 결과 불러오기
    // 같은 선택지 고른 유저들 통계
  };

  return (
    <div className="ethics_problem_container">
      <div className="ethics_problem_title">
        윤리 문제 {data.pid + 1}. {data.title}
      </div>
      <div className="ethics_problem_content">
        <div className="ethics_problem_content_text">{data.content}</div>
      </div>
      <div className="ethics_problem_options">
        <div className="ethics_problem_option">
          <div className="ethics_problem_option_text">A. {data.optionA}</div>
          <button
            className="ethics_problem_option_button"
            onClick={onClickButton}>
            Click
          </button>
        </div>
        <div className="ethics_problem_title">VS</div>
        <div className="ethics_problem_option">
          <div className="ethics_problem_option_text">B. {data.optionB}</div>
          <button
            className="ethics_problem_option_button"
            onClick={onClickButton}>
            Click
          </button>
        </div>
      </div>
      <div className="ethics_problem_options">
        <div className="ethics_result_option">
          <div className="ethics_problem_option_text">A 선택 시 결과</div>
          <div className="ethics_problem_option_button">결과 내용</div>
        </div>
        <div className="ethics_result_option">
          <div className="ethics_problem_option_text">B 선택 시 결과</div>
          <div className="ethics_problem_option_button">결과 내용</div>
        </div>
      </div>
    </div>
  );
}

export default EthicsProblem;
