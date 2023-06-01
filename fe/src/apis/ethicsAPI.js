import axios from "axios";

export const ethicsAPI = {
  getProblems: async (email) => {
    try {
      return axios.get(`http://127.0.0.1:8000/ethics?email=${email}`);
    } catch (e) {
      console.log(e);
    }
  },
  submit: async (pid, email) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/ethics/submission",
        {
          pid,
          email,
        }
      );
      console.log(response.data); // 추가된 코드
      return response;
    } catch (e) {
      console.log(e);
    }
  },
};
