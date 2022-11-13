import React from "react";
import { log, createTabWithUrl } from "../../utils";
import "./App.css";

function ContributeButton() {
  const handlePress = (e) => {
    const contributeUrl = process.env.REACT_APP_WEB_URL + "contribute"
    createTabWithUrl(contributeUrl);
  };

  return (
    <div class="flex-container" onClick={handlePress}>
      <h3 style={{ textDecoration: "underline", color: "#bbb" }}>
        API 등록하러 가기
      </h3>
    </div>
  );
}

export default ContributeButton;
