import React from "react";
import { log, createTabWithUrl } from "../../utils";
import "./App.css";

function Credit() {
  const handlePress = (e) => {
    const creditUrl = "https://github.com/cs496-week4/d2cr-server";
    createTabWithUrl(creditUrl);
  };

  return (
    <div class="flex-container" onClick={handlePress}>
      <h3 style={{ textDecoration: "underline", color: "#bbb" }}>Made by 조재구, 최상아 @ CS496 </h3>
    </div>
  );
}

export default Credit;
