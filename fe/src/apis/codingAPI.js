import axios from "axios";
import { toast } from "react-toastify";

export const codingAPI = {
  getAnswer: async (pid,email) => {
    try {
      return await axios.get(`http://127.0.0.1:8000/codings/answer?pid=${pid}&email=${email}`);
    } catch (e) {
      console.log(e);
    }
  },
  getProblems: async (email) => {
    try {
      return await axios.get(`http://127.0.0.1:8000/codings?email=${email}`);
    } catch (e) {
      console.log(e);
    }
  },
  submit: async (pid, answer, email, isTimeout) => {
    try {
      return await axios.post("http://127.0.0.1:8000/codings/submission", {
        pid,
        answer,
        email,
        isTimeout,
      });
    } catch (e) {
      toast.error(`${e.message}`);
      console.log(e);
    }
  },
};
