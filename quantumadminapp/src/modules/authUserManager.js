// import '@babel/preset-env'
import env from "../../env-config.json";
const remoteURL = env.API_URL;


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
