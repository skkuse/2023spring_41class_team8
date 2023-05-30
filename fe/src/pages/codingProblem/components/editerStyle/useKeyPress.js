import React, { useState } from "react";

// 특정 키를 눌렀는지 여부를 감지하는 커스텀 훅
const useKeyPress = function (targetKey) {
  const [keyPressed, setKeyPressed] = useState(false);

  // 키 다운 이벤트 핸들러
  function downHandler({ key }) {
    // targetKey와 일치하는 키를 눌렀을 때 keyPressed 상태를 true로 설정
    if (key === targetKey) {
      setKeyPressed(true);
    }
  }
  // 키 업 이벤트 핸들러
  const upHandler = ({ key }) => {
    // targetKey와 일치하는 키를 떼었을 때 keyPressed 상태를 false로 설정
    if (key === targetKey) {
      setKeyPressed(false);
    }
  };

  React.useEffect(() => {
    // 키 다운 이벤트와 키 업 이벤트에 대한 이벤트 리스너 등록
    document.addEventListener("keydown", downHandler);
    document.addEventListener("keyup", upHandler);

    // 컴포넌트가 언마운트될 때 이벤트 리스너 제거
    return () => {
      document.removeEventListener("keydown", downHandler);
      document.removeEventListener("keyup", upHandler);
    };
  });

  return keyPressed; // targetKey를 누르고 있는지 여부를 반환하는 상태 값
};

export default useKeyPress;