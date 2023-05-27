import React, { useState } from 'react';
import { Link, useNavigate } from "react-router-dom";
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
      ///api 보내기
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
    <ThemeProvider theme={theme}>
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
          <Avatar sx={{ m: 1, bgcolor: '#3c407f' }} />
          <Typography component="h1" variant="h5">
            회원가입
          </Typography>
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
                  />
                  <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                    <Button variant="contained" onClick={duplicateHandler}>
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
          <Button variant="contained" onClick={handleSubmit}>
            제출
          </Button>
        </Box>
        {failure3Popup && <div style={{ color: 'red' }}>* 조건에 맞는 비밀번호를 입력해주세요.</div>} {/* 실패 팝업 표시 */}
        {failure2Popup && <div style={{ color: 'red' }}>* 이메일 중복 확인을 한 후 제출 버튼을 눌러주세요.</div>} {/* 실패 팝업 표시 */}
        {failurePopup && <div style={{ color: 'red' }}>* 비밀번호와 비밀번호 확인이 일치하지 않습니다.</div>} {/* 실패 팝업 표시 */}
        
      </Container>
    </ThemeProvider>
  );
};
export default Register;