export const hello = () => console.log("hello modules!");
export const getCurrentTabUrl = (callback) => {
  chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
    if (!tabs || tabs.length < 1) throw new Error("[getCurrentTabUrl] No active tab in this window");
    else callback(tabs[0].url);
  });
};

export const getCurrentTabId = (callback) => {
  chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
    if (!tabs || tabs.length < 1) throw new Error("[getCurrentTabId] No active tab in this window");
    else callback(tabs[0].id);
  });
};

export const reloadTabWithId = (id) => {
  chrome.tabs.reload(id);
};

export const createTabWithUrl = (destination, callback = () => null) => {
  chrome.tabs.create({ url: destination }, callback());
};

export const isRequestAboutReview = (details) => {
  return details.url.includes("reviews") && details.type !== "image";
};

export const statusCode = {
  OK: "ok",
  SERVER_ERROR: "error",
  SUCCEESS: "success",
  LOADING: "loading",
  INVALID_PAGE: "invalid page",
  NO_ACTIVE_TAB: "no active tab",
};

export const tooltip = {
  [statusCode.OK]: (
    <div class="flex-container">
      <h2> {"😉  "}</h2>
      <h3 style={{ color: "#bbb" }}> 리뷰 분석 버튼을 눌러보세요! </h3>
    </div>
  ),

  [statusCode.INVALID_PAGE]: (
    <div class="flex-container">
      <h2> {"😅  "} </h2>
      <h3 style={{ color: "#bbb" }}> 분석기를 사용할 수 없는 페이지입니다 </h3>
    </div>
  ),

  [statusCode.SERVER_ERROR]: (
    <div class="flex-container">
      <h2> {"😱  "} </h2>
      <h3 style={{ color: "#bbb" }}> 에러가 발생했습니다 </h3>
    </div>
  ),

  [statusCode.NO_ACTIVE_TAB]: (
    <div class="flex-container">
      <h2> {"🤔  "} </h2>
      <h3 style={{ color: "#bbb" }}> 새로운 창을 띄워 접속해주시겠어요? </h3>
    </div>
  ),

  [statusCode.SUCCEESS]: (
    <div class="flex-container">
      <h2> 🤩 </h2>
      <h3 style={{ color: "#bbb" }}> 분석이 완료되었습니다! </h3>
    </div>
  ),

  [statusCode.LOADING]: (
    <div class="flex-container">
      <h2> 🙄 </h2>
      <h3 style={{ color: "#bbb" }}> 분석 중이에요 </h3>
    </div>
  ),
};

export const mountRequestListener = (callback) => {
  let urlList = [];

  chrome.webRequest.onBeforeRequest.addListener(
    (details) => {
      if (isRequestAboutReview(details)) {
        log("add url");
        urlList.push(details.url);
      }
    },
    { urls: ["<all_urls>"] },
    ["requestBody"]
  );

  chrome.tabs.reload();

  setTimeout(() => {
    log(urlList);
    callback(urlList);
  }, 10000);
};

export const log = (str) => chrome.extension.getBackgroundPage().console.log(str);
export const error = (str) => chrome.extension.getBackgroundPage().console.error(str);


const findBookmark = (bookmarks, title) => {
  for (let i = 0; i < bookmarks.length; i++) {
    const bookmark = bookmarks[i];
    if (bookmark.title === title) return bookmark;
    if (bookmark.children) {
      let childPossiblyCorrect = findBookmark(bookmark.children, title);
      if (childPossiblyCorrect) return childPossiblyCorrect;
    }
  }
  return null;
};

export const getFolder = (results) => {
  return findBookmark(results, "리뷰 분석");
};

export const getSubFolder = (folder, hostName) => {
  if (!folder) return null;
  return findBookmark(folder.children, hostName);
};

export const createFolder = (callback, params) => {
  log("createFolder");
  chrome.bookmarks.create(
    {
      parentId: "1",
      title: "리뷰 분석",
    },

    (folder) => {
      callback({ ...params, folder });
    }
  );
};

export const createFolderSubFolderBookmark = ({ hostName, url }) => {
  createFolder(createSubFolderBookMark, { hostName, url });
};

export const createSubFolderBookMark = ({ folder, hostName, url }) => {
  createSubFolder(folder, hostName, createBookmark, { url });
};

export const createSubFolder = (folder, hostName, callback, params) => {
  log(`createSubFolder: ${folder.id}  ${folder.title} ${hostName}`);

  chrome.bookmarks.create(
    {
      parentId: folder.id,
      title: hostName,
    },
    (subFolder) => {
      log("created subfolder: " + subFolder.id);
      callback({ ...params, subFolder });
    }
  );
};

export const createBookmark = ({ subFolder, url }) => {
  log(`createBookmark: ${subFolder.id} ${subFolder.title} ${url}`);

  chrome.bookmarks.create(
    {
      parentId: subFolder.id,
      title: url,
      url: url,
    },
    (bookmark) => {
      log(`created bookmark: ${bookmark.id} `);
    }
  );
};

export const getHostName = (productUrl) => {
  const url = new URL(productUrl);
  return url.hostname;
};
