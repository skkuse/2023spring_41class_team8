import React, { useState } from "react";

import Editor from "@monaco-editor/react";

const CodeEditorWindow = ({ onChange, language, code}) => {
  const [value, setValue] = useState(code || "");

  // 코드 변경 핸들러 함수
  const handleEditorChange = (value) => {
    setValue(value);
    onChange("code", value);
  };

  return (
    <div className="overlay rounded-md overflow-hidden w-full h-full shadow-4xl">
      <Editor
        height="60vh"
        width={`100%`}
        language={language || "python"}
        value={value}
        theme="oceanic-next"
        defaultValue="// some comment"
        onChange={handleEditorChange}
      />
    </div>
  );
};

export default CodeEditorWindow;