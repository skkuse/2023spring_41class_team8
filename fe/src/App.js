import "./App.css";
import Login from "./pages/login/login";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import Register from "./pages/register/register";
import Selection from "./pages/selection/selection";
import CodingProblem from "./pages/codingProblem/codingProblem";
import EthicsProblem from "./pages/ethicsProblem/ethicsProblem";

function App() {
  return (
    <Router>
      <Link to="/register">Register</Link>
      <Link to="/">Home</Link>

      <Routes>
        <Route path="/codingProblem" element={<CodingProblem />}></Route>
        <Route path="/ethicsProblem" element={<EthicsProblem />}></Route>
        <Route path="/selection" element={<Selection />}></Route>
        <Route path="/register" element={<Register />}></Route>
        <Route path="/" element={<Login />}></Route>
      </Routes>
    </Router>
  );
}

export default App;
