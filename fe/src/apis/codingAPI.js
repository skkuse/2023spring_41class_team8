import axios from "axios";

export const codingAPI = {
  getProblems: (email) => {},
  submit: async (pid, answer, email, isTimeout) => {
    /*
    { 
        result:string (pass, fail), 
        feedback:string
    } 
    */
    try {
      return await axios.post("http://127.0.0.1:8000/codings/submission", {
        pid,
        answer,
        email,
        isTimeout,
      });
    } catch (e) {
      console.log(e);
    }
  },
};
