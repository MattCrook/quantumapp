// import '@babel/preset-env'
import env from "../../env-config.json";
const remoteURL = env.API_URL;

function getCookie(cookieName) {
  let name = cookieName + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let cookieArray = decodedCookie.split(";");
  for (let i = 0; i < cookieArray.length; i++) {
    let cookie = cookieArray[i];
    while (cookie.charAt(0) === " ") {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(name) === 0) {
      return cookie.substring(name.length, cookie.length);
    }
  }
  return "";
}

const authUserManager = {
  async adminLogin(payload) {
    const result = await fetch(`${remoteURL}/quantumadmin/login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      Accept: "application/json",
      body: JSON.stringify(payload),
    });
    return await result.json();
  },
  async registerAdminUser(payload) {
    try {
      const result = await fetch(`${remoteURL}/quantumadmin/register/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        Accept: "application/json",
        body: JSON.stringify(payload),
      });
      return await result.json();
    } catch (error) {
      console.log(error)
    }
  },

  async getCurrentUserFromToken(token) {
    try {
      let cookie = getCookie("csrftoken");
      const data = await fetch(`${remoteURL}/api/get_user_from_token/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": cookie,
          Authorization: "Token " + token,
        },
        Accept: "application/json",
        body: JSON.stringify({"Token": token}),
      });
      return await data.json();
    } catch (error) {
      console.log(error)
    }
  },
  async getUserProfileFromAuthUser(uid, token) {
    const data = await fetch(`${remoteURL}/api/userprofiles?user_id=${uid}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + token,
      },
    });
    return await data.json();
  },
};


export default authUserManager;
