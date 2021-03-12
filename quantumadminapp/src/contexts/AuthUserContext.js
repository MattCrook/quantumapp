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
  const hasLoggedIn = () => sessionStorage.getItem("token") !== null;
  const [isLoggedIn, setIsLoggedIn] = useState(hasLoggedIn());
  const hasLoginCredential = () => sessionStorage.getItem("email") !== null;
  const [hasCredential, setHasCredential] = useState(hasLoginCredential());

  const setDjangoToken = (resp) => {
    sessionStorage.setItem("QuantumToken", resp.token);
    setIsLoggedIn(hasLoggedIn());
  };

  useEffect(() => {
    const initAuthUser = async () => {
      if (hasCredential && isLoggedIn) {
        const token = sessionStorage.getItem("token");
        setAuthToken(token);
        const currentUser = await authUserManager.getCurrentUserFromToken(token);
        setAuthUser(currentUser);
        const currentUserProfile = await authUserManager.getUserProfileFromAuthUser(currentUser.id);
        setUserProfile(currentUserProfile);
        sessionStorage.removeItem("token");

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

  return (
    <AuthUserContext.Provider
      value={{
        isAuthenticated,
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
      }}
    >
      {children}
    </AuthUserContext.Provider>
  );
};
