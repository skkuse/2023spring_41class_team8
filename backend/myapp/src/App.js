import "./App.css";
import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [responseText, setResponseText] = useState("");

  useEffect(() => {
    fetchCSRFToken();
  }, []);

  
  const fetchCSRFToken = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/csrf-token/");
      const csrftoken = response.data.csrftoken;
      axios.defaults.headers.common["X-CSRFToken"] = csrftoken;
    } catch (error) {
      console.error("CSRF 토큰을 가져오는 동안 오류가 발생했습니다.", error);
    }
  };
  

  const handleButtonClick1 = async () => {
    const data = {
      params:{
        id: "아이디",
        pw: "패스워드",
      }
    };

    try {
      const response = await axios.get("http://127.0.0.1:8000/register/", data);
      setResponseText(response.data.message);
      console.log(response.data.id);
      console.log(response.data.cookie);
      console.log(response.data.pw);
    } catch (error) {
      console.error("요청을 보내는 동안 오류가 발생했습니다.", error);
    }
  };

  const handleButtonClick2 = async () => {
    const data = {
      id: "아이디",
      email: "sample@gmail.com",
      pw: "패스워드",
    };

    try {
      const response = await axios.post("http://127.0.0.1:8000/register/", data);
      setResponseText(response.data.message);
      console.log(response.data.id);
      console.log(response.data.email);
      console.log(response.data.pw);
    } catch (error) {
      console.error("요청을 보내는 동안 오류가 발생했습니다.", error);
    }
  };

  return (
    <div>
      <h1>{responseText}</h1>
      <button onClick={handleButtonClick1}>로그인</button>
      <button onClick={handleButtonClick2}>회원가입</button>
    </div>
    
  );
}

export default App;


