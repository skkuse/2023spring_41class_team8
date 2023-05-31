import axios from "axios";

export const ethicsAPI = {
  getProblems: (email) => {},
  submit: async (pid, email) => {
    try {
      return await axios.post("http://127.0.0.1:8000/ethics/submission", {
        pid,
        email,
      });
    } catch (e) {
      console.log(e);
    }
  },
};
