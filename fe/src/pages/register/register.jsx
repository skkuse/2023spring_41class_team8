import React, { useState } from 'react';
import { Link, useNavigate } from "react-router-dom";
import axios from 'axios';
import "./register.css";
import {
  Avatar,
  Button,
  CssBaseline,
  TextField,
  FormControl,
  FormControlLabel,
  Checkbox,
  FormHelperText,
  Grid,
  Box,
  Typography,
  Container,
} from '@mui/material/';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const Register = () => {
  const theme = createTheme();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const navigate = useNavigate()
  const [duplicatePopup, setDuplicatePopup] = useState(false);
  const [successPopup, setSuccessPopup] = useState(false);
  const [failurePopup, setFailurePopup] = useState(false);
  const [failure2Popup, setFailure2Popup] = useState(false);
  const [failure3Popup, setFailure3Popup] = useState(false);
  const [failure4Popup, setFailure4Popup] = useState(false);


  
  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };
  const handlePasswordChange = (e) => {
    //console.log("Password:", password);
    setPassword(e.target.value);
    if(password.length>16 || password.length<8){
      setFailure3Popup(true)
    }else{
      setFailure3Popup(false)
    }
  };

  const handlePassword2Change = (e) => {
    //console.log("Password2:", password2);
    setPassword2(e.target.value);
  };

  const duplicateHandler = async (e) => {
    try {
      const response = await fetch(`http://localhost:8000/user/idcheck?email=${email}`);
      
      if (response.ok) {
        // Login successful, update user info and navigate to the desired page
        const data = await response.json();
        setDuplicatePopup(true);
        // status 값 200이면 가능 501이면 중복 
        if (data.status === 200){
          setDuplicatePopup(false);
          setSuccessPopup(true);
        }
        else if(data.status===501){
          setDuplicatePopup(true); 
          setSuccessPopup(false); 
        }
      } else {
        // Login failed, display failure message
        setFailurePopup(true);
      }
    } catch (error) {
      // Handle any network or server errors
      console.error('Error:', error);
    } // 중복 확인 성공 팝업 설정
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Perform register logic here, e.g., send email and password to an API for authentication
    // password = password2 이면 로그인 아니면 팝업
    console.log("Password:", password);
    console.log("Password2:", password2);


    if (password === password2 && successPopup === true){
      console.log("Email:", email);
      console.log("Password:", password);
      //setEmail(email);
      setPassword(password);
      if (failure3Popup){
          
      }
      else{
        try {
        
          const user = {
            email: email,
            password: password
          }
          const response = await fetch('http://127.0.0.1:8000/register', {
            method:'POST',
            body: JSON.stringify(user)
          });
          const data = await response.json()
          console.log(data.status)
          if (data.status === 200) {
            // setSuccessPopup(true);
            navigate("/");
          } else {
            //setFailurePopup(true);
            setFailure4Popup(true);
          }
        } catch (error) {
          console.log(error);
          // setFailurePopup(true);
          setFailure4Popup(true);
        }
      }
      //api 보내기

      
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
    <div className="register_container">
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <img src="img/logo.jpg" style={{ width: '250px', height: '100px' }}></img>
          <h2 className="title">회원가입</h2>
          
          <Box noValidate sx={{ mt: 3 }}>
            <FormControl component="fieldset" variant="standard">
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    required
                    autoFocus
                    fullWidth
                    type="email"
                    id="email"
                    name="email"
                    label="이메일 주소"
                    onChange={handleEmailChange}
                  />
                  <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                    <Button variant="contained" onClick={duplicateHandler} style={{ backgroundColor: "#3c407f", color: "#ffffff" }}>
                      중복 검사
                    </Button>
                  </Box>
                  {duplicatePopup && <div style={{ color: 'red' }}>* 중복된 이메일입니다.</div>} {/* 중복 에러 표시 */}
                  {successPopup && <div style={{ color: 'red' }}>* 성공했습니다.</div>} {/* 성공 팝업 표시 */}
                </Grid>
    
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    type="password"
                    id="password"
                    name="password"
                    label="비밀번호 (8자리 이상 16자리 이하)"
                    onChange={handlePasswordChange}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    type="password"
                    id="password2"
                    name="password2"
                    label="비밀번호 재입력"
                    onChange={handlePassword2Change}
                  />
                </Grid>
                
              </Grid>
            </FormControl>
          </Box>
        </Box>
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2, }}>
          <Button variant="contained" onClick={handleSubmit} style={{ backgroundColor: "#3c407f", color: "#ffffff" }}>
            제출
          </Button>
        </Box>
        {failure4Popup && <div style={{ color: 'red' }}>* 내부적인 문제로 회원 정보 등록에 실패했습니다.</div>} {/* 실패 팝업 표시 */}
        {failure3Popup && <div style={{ color: 'red' }}>* 조건에 맞는 비밀번호를 입력해주세요.</div>} {/* 실패 팝업 표시 */}
        {failure2Popup && <div style={{ color: 'red' }}>* 이메일 중복 확인을 한 후 제출 버튼을 눌러주세요.</div>} {/* 실패 팝업 표시 */}
        {failurePopup && <div style={{ color: 'red' }}>* 비밀번호와 비밀번호 확인이 일치하지 않습니다.</div>} {/* 실패 팝업 표시 */}
        
      </Container>
    </div>
  );
};
export default Register;