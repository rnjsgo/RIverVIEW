import React, { useState } from "react";
import { log, createTabWithUrl, statusCode, getCurrentTabUrl, mountRequestListener, getHostName } from "../../utils";
import { getReviewInspectPage, checkInspectable, hello, headers } from "../../api";
import AwesomeButtonProgress from "react-awesome-button/src/components/AwesomeButtonProgress";
import styles from "react-awesome-button/src/styles/themes/theme-rickiest";
import axios from "axios";

function InspectButton({ handleStatusChange, showContributeButton }) {
  const registerBookmark = (reviewInspectPageUrl, productUrl) => {
    const hostName = getHostName(productUrl);
    const bg = chrome.extension.getBackgroundPage();
    bg.addBookmark(hostName, reviewInspectPageUrl);
  };

  const handlePress = async (element, next) => {
    handleStatusChange(statusCode.LOADING);
    const apiUrl = process.env.REACT_APP_API_URL + "/inspect";

    try {
      getCurrentTabUrl((productUrl) => {
        try {
          checkInspectable(productUrl).then((res) => {
            if (res.data === "valid") {
              mountRequestListener((urlList) => {
                try {
                  axios.post(apiUrl, { productUrl, urlList: urlList }, { headers }).then((res) => {
                    const reviewInspectPageUrl = process.env.REACT_APP_WEB_URL + "page/" + res.data;
                    createTabWithUrl(reviewInspectPageUrl);
                    log(`reviewInspectPageUrl: ${reviewInspectPageUrl}`);
                    registerBookmark(reviewInspectPageUrl, productUrl);
                    next();
                  });
                } catch (e) {
                  handleStatusChange(statusCode.SERVER_ERROR);
                  next();
                }
              });
            } else {
              log("invalid page: register page to contribute");
              handleStatusChange(statusCode.INVALID_PAGE);
              showContributeButton()
              next();
            }
          });
        } catch (e) {
          handleStatusChange(statusCode.SERVER_ERROR);
          next();
        }
      });
    } catch (e) {
      log("no active tab (refresh required)");
      handleStatusChange(statusCode.NO_ACTIVE_TAB);
      next();
    }
  };

  const handleHello = () => {
    hello();
  };

  return (
    <AwesomeButtonProgress loadingLabel="기다려주세요" resultLabel="다 됐어요!" size="medium" type="primary" onPress={handlePress}>
      리뷰 분석
    </AwesomeButtonProgress>
  );
}

export default InspectButton;
