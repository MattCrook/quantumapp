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
        hasLoginCredential,
        setHasCredential,
      }}
    >
      {children}
    </AuthUserContext.Provider>
  );
};
