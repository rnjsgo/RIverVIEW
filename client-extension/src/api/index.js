import axios from "axios";

export const headers = {
  "Content-Type": "application/json",
};

export const mockCheckUrl = (url) => {
  const apiUrl = process.env.REACT_APP_API_URL + "/check";
  axios
    .get(apiUrl)
    .then((res) => {
      if (res.status === 200) return true;
      else return false;
    })
    .catch((e) => console.error(e));
};

export const getReviewInspectPage = (urlList, productUrl) => {
  const apiUrl = process.env.REACT_APP_API_URL + "/inspect";
  console.log(`getReviewInspectPage: ${urlList}`);
  return axios.post(apiUrl, { urlList, productUrl }, { headers })
}

export const checkInspectable = (productUrl) => {
  const apiUrl = process.env.REACT_APP_API_URL + "/check";
  return axios.post(apiUrl, { productUrl }, { headers });
};

export const hello = () => {
  axios
    .get(process.env.REACT_APP_API_URL + "/hello")
    .then((res) => {
      console.warn(res.data);
    })
    .catch((e) => console.error(e));
};

export default {
  getReviewInspectPage,
  hello,
  checkInspectable,
};
