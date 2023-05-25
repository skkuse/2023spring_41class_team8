import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate()

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Perform login logic here, e.g., send email and password to an API for authentication
    console.log("Email:", email);
    console.log("Password:", password);
    navigate("/selection");
  };

  return (
    <div className="login">
      <div>로그인</div>
      <form onSubmit={handleSubmit}>
        <div>
          <label>이메일:</label>
          <input type="email" value={email} onChange={handleEmailChange} />
        </div>
        <div>
          <label>비밀번호:</label>
          <input type="password" value={password} onChange={handlePasswordChange} />
        </div>
        <button type="submit">로그인</button>
      </form>
      <Link to="register">`Go to Register</Link>
    </div>
  );
}

export default Login;
