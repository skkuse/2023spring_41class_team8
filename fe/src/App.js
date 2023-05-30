import "./App.css";
import Login from "./pages/login/login";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import Register from "./pages/register/register";
import EthicsProblemList from "./pages/ethicsProblem/ethicsProblemList";
import EthicsProblem from "./pages/ethicsProblem/ethicsProblem";
import { useState } from "react";
import CodingProblem from "./pages/codingProblem/codingProblem";
import CodingProblemList from "./pages/codingProblem/codingProblemList";
import Selection from "./pages/selection/selection";

export const defaultUserInfo = {
  email: "test@gmail.com",
  password: "test",
  solvedCodingProblems: [1, 4, 5],
  solvedEthicsProblems: [0, 4, 9, 11],
  score: 0,
};

function App() {
  const [userInfo, setUserInfo] = useState(defaultUserInfo);

  const getUserInfo = () => {
    return userInfo;
  };

  const updateUserInfo = (newInfo) => {
    setUserInfo(newInfo);
  };

  return (
    <Router>
      <Routes>
        <Route
          path="/ethics/:pid"
          element={
            <EthicsProblem
              getUserInfo={getUserInfo}
              updateUserInfo={updateUserInfo}
            />
          }
        />
        <Route
          path="/ethics"
          element={
            <EthicsProblemList
              getUserInfo={getUserInfo}
              updateUserInfo={updateUserInfo}
            />
          }
        />
        <Route
          path="/coding/:pid"
          element={
            <CodingProblem
              getUserInfo={getUserInfo}
              updateUserInfo={updateUserInfo}
            />
          }
        />
        <Route
          path="/coding"
          element={
            <CodingProblemList
              getUserInfo={getUserInfo}
              updateUserInfo={updateUserInfo}
            />
          }
        />
        <Route path="/register" element={<Register />} />
        <Route
          path="/"
          element={
            <Login getUserInfo={getUserInfo} updateUserInfo={updateUserInfo} />
          }
        />
        <Route path="/selection" element={<Selection />} />
        <Route path="/ethicsProblem" element={<EthicsProblem />} />
      </Routes>
    </Router>
  );
}

export default App;
