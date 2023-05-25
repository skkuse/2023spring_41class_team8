import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Selection() {
    const navigate = useNavigate()
    const handleCoding = (e) => {
        navigate("/codingProblem");
    };

    const handleEthics = (e) => {
        navigate("/ethicsProblem");
    };


    return (
    <div>둘 중 하나를 골라주세요.
        <button onClick={handleCoding}>AI와 코딩대결!</button>
        <button onClick={handleEthics}>신나는 윤리 교육!</button>
    </div>
    )
}

export default Selection;