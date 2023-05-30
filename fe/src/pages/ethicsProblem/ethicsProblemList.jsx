import "./ethicsProblemList.css";
import { ethicsProblems } from "../../ethicsProblemData";
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

function EthicsProblemList({ getUserInfo, updateUserInfo }) {
  const navigate = useNavigate();
  const [data, setData] = useState(ethicsProblems);
  const [userInfo, setUserInfo] = useState(defaultUserInfo);

  const onClickProblem = (data) => {
    navigate(`/ethics/${data.pid}`, {
      state: {
        data,
      },
    });
  };

  useEffect(() => {
    setUserInfo(getUserInfo());
  }, []);
  return (
    <div className="ethics_problem_list_container">
      <div className="ethics_problem_percent">
        <div>
          <div className="ethics_problem_percent_info">
            {`${userInfo.username}님의 진행률: ${Math.round(
              (userInfo.solvedEthicsProblems.length / data.length) * 100
            )}%`}
          </div>
          <div className="percent_bar_container">
            <div className="percent_bar" />
            <div
              className="percent_bar_active"
              style={{
                width: `${Math.round(
                  (userInfo.solvedEthicsProblems.length / data.length) * 150
                )}px`,
              }}
            />
          </div>
        </div>
      </div>
      <div className="ethics_problem_list_title">윤리 문제 리스트</div>
      <div className="ethics_problem_list_table">
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
                    style={{ width: "30px", padding: "10px" }}>
                    {userInfo.solvedEthicsProblems.includes(row.pid)
                      ? "완료"
                      : "미완"}
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

export default EthicsProblemList;
