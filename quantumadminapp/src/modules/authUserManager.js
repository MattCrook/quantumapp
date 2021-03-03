// import '@babel/preset-env'
import env from "../../env-config.json";
const remoteURL = env.API_URL;
console.log(remoteURL)

const authUserManager = {
  async getCurrentUserFromToken(token) {
    const data = await fetch(`${remoteURL}/api/get_user_from_token/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + token,
      },
      Accept: "application/json",
    });
    return await data.json();
  },
  async getUserProfileFromAuthUser(uid) {
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
