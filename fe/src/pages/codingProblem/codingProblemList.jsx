import "./codingProblemList.css";
import { codingProblems } from "../../codingProblemData";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { defaultUserInfo } from "../../App";
import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

function CodingProblemList({ getUserInfo, updateUserInfo }) {
  const navigate = useNavigate();
  const [data, setData] = useState(codingProblems);
  const [userInfo, setUserInfo] = useState(defaultUserInfo);
  const [score, setScore] = useState(0);
  


  const onClickProblem = (data) => {
    
    navigate(`/coding/${data.pid}`, {
      state: {
        data,
      },
    });
  };
  useEffect(() => {
    const currentUserInfo = getUserInfo();
    setUserInfo(currentUserInfo);
  
    if (currentUserInfo.email !== "test@gmail.com") {
      const solvedProblems = currentUserInfo.solvedCodingProblems.map((index) => data[index]);
      const totalScore = solvedProblems.reduce((sum, problem) => sum + problem.level, 0);
      
      const updatedUserInfo = { ...currentUserInfo, score: totalScore };
      console.log(updatedUserInfo);
      setScore(totalScore)
    }
  }, []);
  
  return (
    <div className="coding_problem_list_container">
      <div className="coding_problem_score">
        <div>
          <div className="coding_problem_score_info">
            {`${userInfo.email}님의 점수: ${score}` }
          </div>
        </div>
      </div>
      <div className="coding_problem_list_title">코딩 문제 리스트</div>
      <div className="coding_problem_list_table">
        <TableContainer
          component={Paper}
          style={{
            display: "flex",
            justifyContent: "center",
            border: `1px solid #3c407f`,
            fontSize: "20px",
            width: "fit-content",
          }}>
          <Table style={{ width: "500px" }}>
            <TableHead>
              <TableRow style={{ backgroundColor: "#cac6ff" }}>
                <TableCell>상태</TableCell>
                <TableCell>레벨</TableCell>
                <TableCell>제한</TableCell>
                <TableCell align="middle">문제 이름</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((row) => (
                <TableRow
                  style={{ cursor: "pointer" }}
                  hover
                  onClick={() => onClickProblem(row)}
                  key={row.title}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}>
                  <TableCell
                    component="th"
                    style={{
                      width: "30px",
                      padding: "10px",
                      color: userInfo.solvedCodingProblems.includes(row.pid) ? "blue" : "red",
                    }}>
                    {userInfo.solvedCodingProblems.includes(row.pid) ? "완료" : "미완"}
                  </TableCell>

                  <TableCell
                    align="middle"
                    style={{ width: "30px", padding: "10px" }}>
                    {row.level}
                  </TableCell>
                  <TableCell
                    component="th"
                    style={{ width: "30px", padding: "10px" }}>
                    {row.level === 1 ? "5분" : row.level === 2 ? "10분" : row.level === 3 ? "15분" : "dummy"}
                  </TableCell>
                  <TableCell
                    align="middle"
                    style={{ width: "200px", padding: "10px" }}>
                    {row.title}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>
    </div>
  );
}

export default CodingProblemList;
