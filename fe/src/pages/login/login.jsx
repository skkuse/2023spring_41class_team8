import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";
import "./login.css";
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
} from "@mui/material/";
import { createTheme, ThemeProvider } from "@mui/material/styles";

function Login({ getUserInfo, updateUserInfo }) {
  const theme = createTheme();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const location = useLocation();
  const [failurePopup, setFailurePopup] = useState(false);

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = async (e) => {
    try {
      const response = await fetch(
        `http://localhost:8000/user?email=${email}&password=${password}`
      );

      if (response.ok) {
        const data = await response.json();
        if (email === data.email) {
          updateUserInfo({
            email: email,
            password: password,
            score: data.score,
            solvedCodingProblems: data.solvedCodingProblems,
            solvedEthicsProblems: data.solvedEthicsProblems,
          });
          navigate("/selection");
        } else {
          setFailurePopup(true);
        }
      } else {
        setFailurePopup(true);
      }
    } catch (error) {
      // Handle any network or server errors
      console.error("Error:", error);
    } // 중복 확인 성공 팝업 설정
  };

  return (
    <div className="login_container">
      <Container component="main" maxWidth="xs" className="login_container">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}>
          <img src="img/logo.jpg" style={{ width: '250px', height: '100px' }}></img>
          <h2 className="title">로그인</h2>
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
              </Grid>
            </FormControl>
          </Box>
        </Box>
        <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
          <Button variant="contained" onClick={handleSubmit} style={{ backgroundColor: "#3c407f", color: "#ffffff" }}>
            제출
          </Button>
        </Box>
        {failurePopup && (
          <div style={{ color: "red" }}>해당 회원 정보가 없습니다.</div>
        )}{" "}
        {/* 실패 팝업 표시 */}
        <Link to="register" className="register-link">회원가입</Link>
      </Container>
    </div>
  );
}

export default Login;
