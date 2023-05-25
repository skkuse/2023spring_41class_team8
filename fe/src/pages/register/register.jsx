import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const navigate = useNavigate()
  const [duplicatePopup, setDuplicatePopup] = useState(false);
  const [successPopup, setSuccessPopup] = useState(false);
  const [failurePopup, setFailurePopup] = useState(false);
  const [failure2Popup, setFailure2Popup] = useState(false);

  
  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    //console.log("Password:", password);
    setPassword(e.target.value);
  };

  const handlePassword2Change = (e) => {
    //console.log("Password2:", password2);
    setPassword2(e.target.value);
  };

  const duplicateHandler = (e) => {
    //중복 확인 성공하면 성공팝업, 아니면 실패 팝업
    //const isDuplicate = checkDuplicate(); // 중복 확인 로직을 구현한 함수
    /* if (isDuplicate) {
      setDuplicateError(true); // 중복된 이메일이 있다면 에러 설정
    } else {
      setDuplicateError(false); // 중복된 이메일이 없다면 에러 해제
      setSuccessPopup(true); // 중복 확인 성공 팝업 설정
    } */
    setDuplicatePopup(false); // 중복된 이메일이 없다면 에러 해제
    setSuccessPopup(true); // 중복 확인 성공 팝업 설정
  };

  


  const handleSubmit = (e) => {
    e.preventDefault();
    // Perform register logic here, e.g., send email and password to an API for authentication
    // password = password2 이면 로그인 아니면 팝업
    console.log("Password:", password);
    console.log("Password2:", password2);

    if (password === password2 && successPopup === true){
      console.log("Email:", email);
      console.log("Password:", password);
      setPassword(password);

      setSuccessPopup(true);
      navigate("/");
    } else if(password !== password2 && successPopup === true){
      setFailurePopup(true);
      setFailure2Popup(false);
    } else if(password === password2 && successPopup !== true){
      setFailurePopup(false);
      setFailure2Popup(true);
    } else{
      setFailurePopup(true);
      setFailure2Popup(true);
    }

  };

  return (
    <div className="register">
      <div>회원 가입</div>
      <div>
        <label>이메일:</label>
        <input type="email" value={email} onChange={handleEmailChange} />
        <button type="submit" onClick={duplicateHandler}>중복 검사</button>
        {duplicatePopup && <div>중복된 이메일입니다.</div>} {/* 중복 에러 표시 */}
        {successPopup && <div>성공했습니다.</div>} {/* 성공 팝업 표시 */}
      </div>
      <div>
        <label>비밀번호:</label>
        <input type="password" value={password} onChange={handlePasswordChange} />
      </div>
      <div>
        <label>비밀번호 확인:</label>
        <input type="password" value={password2} onChange={handlePassword2Change} />
      </div>
      {failure2Popup && <div>이메일 중복 확인을 한 후 제출 버튼을 눌러주세요.</div>} {/* 실패 팝업 표시 */}
      {failurePopup && <div>비밀번호와 비밀번호 확인이 일치하지 않습니다.</div>} {/* 실패 팝업 표시 */}
      <button onClick={handleSubmit}>제출</button>
      
    </div>
  );
}

export default Register;
