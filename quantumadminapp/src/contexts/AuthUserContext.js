import React, { useState, useEffect, useContext } from "react";
import authUserManager from "../modules/authUserManager";

export const AuthUserContext = React.createContext();
export const useAuthUser = () => useContext(AuthUserContext);

export const AuthUserProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [authUser, setAuthUser] = useState([]);
  const [userProfile, setUserProfile] = useState([]);
  const [authToken, setAuthToken] = useState([]);
  const [authUserData, setAuthUserData] = useState([]);
  const [idToken, setIdToken] = useState([]);
  const [openIDUser, setOpenIDUser] = useState([]);

  // Todo: change to "token" instead of "QuantumToken"
  const hasLoggedIn = () => sessionStorage.getItem("QuantumToken") !== null;
  const [isLoggedIn, setIsLoggedIn] = useState(hasLoggedIn());
  const hasLoginCredential = () => sessionStorage.getItem("email") !== null;
  const [hasCredential, setHasCredential] = useState(hasLoginCredential());


  const setDjangoToken = (resp) => {
    // Todo: change to "token" instead of "QuantumToken"
    sessionStorage.setItem("QuantumToken", resp.token);
    setIsLoggedIn(hasLoggedIn());
  };

  useEffect(() => {
    const initAuthUser = async () => {
      if (hasCredential && isLoggedIn) {
        // Todo: change to "token" instead of "QuantumToken"
        const token = sessionStorage.getItem("QuantumToken");
        setAuthToken(token);
        const currentUser = await authUserManager.getCurrentUserFromToken(token);
        console.log(currentUser)
        setAuthUser(currentUser);
        const currentUserProfile = await authUserManager.getUserProfileFromAuthUser(currentUser.id, token);
        setUserProfile(currentUserProfile);
        // sessionStorage.removeItem("QuantumToken");

        const credential = sessionStorage.getItem("email");
        if (credential === currentUser.email) {
          setIsAuthenticated(true);
        }
        setIsLoading(false);
      } else {
        console.log("AuthUserContext: NOTLOGGEDIN");
        setIsLoading(false);
      }
    };
    initAuthUser();
  }, []);

  const adminLogout = async () => {
    setIsLoading(true);
    sessionStorage.removeItem("QuantumToken");
    sessionStorage.removeItem("email");
    var adminLogoutUrl = window._env_.ADMIN_LOGOUT
    try {
      const csrf = getCookie('csrftoken');
      const response = await fetch(`${adminLogoutUrl}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrf,
        },
      });
      if (response.ok) {
        setIsLoading(false);
        const origin = window.location.origin;
        window.location.href = origin + '/quantumadmin/'
      }
    } catch (err) {
      setIsLoading(false);
      console.log(err);
    }
  };

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



  return (
    <AuthUserContext.Provider
      value={{
        isAuthenticated,
        setIsAuthenticated,
        isLoading,
        setIsLoading,
        userProfile,
        authUser,
        authToken,
        setUserProfile,
        setAuthUser,
        setAuthToken,
        setAuthUserData,
        authUserData,
        isLoggedIn,
        setDjangoToken,
        hasCredential,
        hasLoginCredential,
        setHasCredential,
        adminLogout,
      }}
    >
      {children}
    </AuthUserContext.Provider>
  );
};
