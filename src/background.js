import { log, createBookmark, createSubFolderBookMark, createFolderSubFolderBookmark, getFolder, getSubFolder } from "./utils";
const test_addBookmark2 = () => {
  chrome.bookmarks.create({
    parentId: "1",
    title: "테스트2 북마크",
    url: "https://github.com/cs496-week4/d2cr-client",
  });
};

window.test_addBookmark = () => {
  chrome.bookmarks.create(
    {
      parentId: "1",
      title: "테스트 폴더",
    },

    (folder) => {
      chrome.bookmarks.create(
        {
          parentId: folder.id,
          title: "테스트 서브폴더",
        },
        (subfolder) => {
          log("북마크 만드는 중");
          chrome.bookmarks.create({
            parentId: subfolder.id,
            title: "테스트 북마크",
            url: "https://github.com/cs496-week4/d2cr-client",
          });
        }
      );
    }
  );
};

window.hello = (msg) => {
  log(msg);
};

window.addBookmark = (hostName, pageUrl) => {
  chrome.bookmarks.getTree((results) => {
    let folder = getFolder(results);
    let subFolder = getSubFolder(folder, hostName);

    if (folder && subFolder) {
      log("folder && subFolder");
      createBookmark({ subFolder, url: pageUrl });
    } else if (folder) {
      log("folder && !subFolder");
      createSubFolderBookMark({ folder, hostName, url: pageUrl });
    } else {
      log("!folder && !subFolder");
      createFolderSubFolderBookmark({ hostName, url: pageUrl });
    }
  });
};
