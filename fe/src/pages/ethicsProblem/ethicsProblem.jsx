import { useState } from "react";
import { useLocation } from "react-router-dom";
import "./ethicsProblem.css";
import { ethicsAPI } from "../../apis/ethicsAPI";

function EthicsProblem({ getUserInfo, updateUserInfo }) {
  const location = useLocation();
  const data = location.state.data;

  const [result, setResult] = useState([]);
  const [selectedOption, setSelectedOption] = useState("");

  const onClickButton = (clicked) => {
    if (selectedOption.length === 0) {
      setSelectedOption(clicked);
      let userInfo = getUserInfo();
      updateUserInfo({
        ...userInfo,
        solvedEthicsProblems: [...userInfo.solvedEthicsProblems, data.pid],
      });
      ethicsAPI.submit(data.pid.toString(), userInfo.email).then((res) => {
        console.log("submit", res.data.results);
        setResult(res.data.results);
      });
    }

    // TODO: 해당 선택지 선택 시 결과 불러오기
    // 같은 선택지 고른 유저들 통계
    // 풀었던 문제면 정보 가져와서 해당 답 미리 선택되어있도록 하기
  };

  return (
    <div className="ethics_problem_container">
      <div className="ethics_problem_area">
        <div className="ethics_problem_title">
          윤리 문제 {data.pid + 1}. {data.title}
        </div>
        <div className="ethics_problem_content">
          <div className="ethics_problem_content_text">{data.content}</div>
        </div>
        <div className="ethics_problem_options">
          <div
            className={`ethics_problem_option ethics_problem_option_${
              selectedOption.length === 0
                ? "active"
                : selectedOption === "a"
                ? "selected"
                : ""
            }`}
            onClick={() => onClickButton("a")}>
            <div className="ethics_problem_option_text">A. {data.optionA}</div>
          </div>
          <div className="ethics_problem_title">VS</div>
          <div
            className={`ethics_problem_option ethics_problem_option_${
              selectedOption.length === 0 ? "active" : ""
            }`}
            onClick={() => onClickButton("b")}>
            <div className="ethics_problem_option_text">B. {data.optionB}</div>
          </div>
        </div>
      </div>

      {selectedOption.length !== 0 && (
        <div className="ethics_result_options">
          <div
            className={`ethics_result_option ${
              selectedOption === "a" ? "ethics_result_option_selected" : ""
            }`}>
            <h3 className="ethics_result_title">A 선택 시 결과</h3>
            <div className="ethics_result_content">{result[0]}</div>
          </div>
          <div
            className={`ethics_result_option ${
              selectedOption === "b" ? "ethics_result_option_selected" : ""
            }`}>
            <h3 className="ethics_result_title">B 선택 시 결과</h3>
            <div className="ethics_result_content">{result[1]}</div>
          </div>
        </div>
      )}
    </div>
  );
}

export default EthicsProblem;
