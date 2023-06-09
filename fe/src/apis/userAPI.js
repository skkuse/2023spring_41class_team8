import axios from "axios";

export const userInfo = {
  id: 0,
  email: "test@gmail.com",
  password: "test",
  username: "test",
  solvedCodingProblems: [1, 4, 5],
  solvedEthicsProblems: [0, 4, 9, 11],
};
export const userAPI = {
  getUserInfo: async (email, password) => {
    try {
      return axios.get(
        `http://127.0.0.1:8000/user?email=${email}&password=${password}`
      );
    } catch (e) {
      console.log(e);
    }
  },
  updateUserInfo: (newInfo) => {
    // 업데이트하고
    // 상태 업데이트해주기
  },
  createUserInfo: () => {},
};
