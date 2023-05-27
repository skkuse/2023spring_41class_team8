import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./selection.css"; // Import the CSS file

function Selection() {
    const navigate = useNavigate();

    const handleCoding = (e) => {
        navigate("/coding");
    };

    const handleEthics = (e) => {
        navigate("/ethics");
    };

    return (
        <div className="container">
        <h2 className="title">둘 중 하나를 골라주세요.</h2>
        <button className="button" onClick={handleCoding}>
            AI와 코딩대결!
        </button>
        <button className="button" onClick={handleEthics}>
            신나는 윤리 교육!
        </button>
        </div>
    );
}

export default Selection;