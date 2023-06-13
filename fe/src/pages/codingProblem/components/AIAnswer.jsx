import React, { useState, useEffect } from "react";
import Editor from "@monaco-editor/react";
import "./AIAnswer.css";

const AIAnswer = ({ onChange, language, code, timerEndCondition, isBlurred }) => {
  const [value, setValue] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    // 코드 출력을 위한 인터벌 설정
    if(timerEndCondition){
      setValue(code)
      setCurrentIndex(code.length)
    }
    
    const interval = setInterval(() => {
      if (currentIndex < code.length) {
        // 현재 인덱스가 코드 길이보다 작은 경우에만 실행
        setValue((prevValue) => prevValue + code[currentIndex]); // 현재 인덱스의 문자를 현재 값에 추가
        setCurrentIndex((prevIndex) => prevIndex + 1); // 인덱스 증가
      }
    }, 500);

    return () => {
      clearInterval(interval); // 컴포넌트가 언마운트될 때 인터벌 제거
    };
  }, [code, currentIndex]);

  const handleEditorChange = (value) => {
    setValue(value); // 상태 변수에 값 설정
  };

  const blurClass = isBlurred ? "blur" : ""; // blurClass 변수에 blur 클래스 할당 여부 설정

  return (
    <div className={`overlay rounded-md overflow-hidden w-full h-full shadow-4xl ${blurClass}`}>
      <Editor
        height="60vh"
        width={`100%`}
        language={language || "python"} // 언어 설정
        value={value} // 현재 코드 값 설정
        theme="oceanic-next" // 테마 설정
        defaultValue="// some comment"
        onChange={handleEditorChange} // 에디터 값 변경 이벤트 핸들러
        options={{
          readOnly: true, // 읽기 전용 모드 설정
        }}
      />
    </div>
  );
};

export default AIAnswer;