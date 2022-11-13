import React, { useState } from "react";
import "./App.css";

import InspectButton from "./InspectButton";
import GitHubButton from "./GitHubButton";
import { statusCode, tooltip } from "../../utils";
import ContributeButton from "./ContributeButton";
import Credit from "./Credit";

function App() {
  const [status, setStatus] = useState(statusCode.OK);
  const [contributeButtonVisible, setVisible] = useState(false);

  const handleStatusChange = (code) => {
    console.log(code);
    setStatus(code);
  };

  const showContributeButton = () => {
    setVisible(true);
  };

  return (
    <div class="container">
      <h1 class="title">리뷰 분석기 </h1>
      <div class="flex-container">
        <div class="flex-item">
          <InspectButton handleStatusChange={handleStatusChange} showContributeButton={showContributeButton} />
        </div>
        <div class="flex-item">
          <GitHubButton />
        </div>
      </div>

      {tooltip[status]}
      {contributeButtonVisible ? (<ContributeButton />) : (
        <Credit/>
      )}
    </div>
  );
}

export default App;
