import React, { useState } from "react";
import LoginNav from "../nav/LoginNav";
import AuthForm from "./forms/LoginForm";
import authUserManager from "../../modules/authUserManager";
import { useAuthUser } from "../../contexts/AuthUserContext";
import "./styles/Login.css";

const Login = (props) => {
  const { setDjangoToken, setAuthToken } = useAuthUser();
  const [error, setError] = useState(false);
  const [errorMessage, setErrorMessage] = useState(""); // error message
  const [isValidating, setIsValidating] = useState(false); // progress loading circle
  const [success, setSuccess] = useState(false); // success login check
  const [email, setEmail] = useState({});
  const [password, setPassword] = useState({});

  const showError = (message) => {
    setIsValidating(false);
    setError(true);
    setErrorMessage(message);
  };



  const handleEmail = (e) => {
    const formState = { ...email };
    formState[e.target.id] = e.target.value;
    setEmail(formState);
  };

  const handlePassword = (e) => {
    const formState = { ...password };
    formState[e.target.id] = e.target.value;
    setPassword(formState);
  };



  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsValidating(true);

    const loginCredentials = {
      email: email,
      password: password,
    };
    console.log({loginCredentials})

    try {
      const response = await authUserManager.adminLogin(loginCredentials);
      if (response.valid === true) {
        setIsValidating(false);
        setSuccess(true);
        setDjangoToken(response);
        setAuthToken(response.token);
        sessionStorage.setItem("email", response.email);
        // Todo: set logged in to true (user profile table)
        props.history.push("/quantumadmin/");
      } else {
        showError("Credentials you entered are incorrect.");
      }
    } catch (error) {
      showError("Error logging in. Please try again.");
    }
  };

  return (
    <>
      <LoginNav {...props} />
      <div id="login_master_container">
        <AuthForm
          email={email}
          password={password}
          handleSubmit={handleSubmit}
          handleEmail={handleEmail}
          handlePassword={handlePassword}
          {...props}
        />
        {isValidating ? (
          <div className="validating_email_container">
            <div id="auth_spinner"></div>
          </div>
        ) : null}
        {error ? (
          <div className="error_message_container">
            <i id="fa_triangle" className="fas fa-exclamation-triangle"></i>
            <div className="error_message">{errorMessage}</div>
          </div>
        ) : null}
        {success ? (
          <div className="success_check_wrapper">
            <i id="auth_check" className="fas fa-check-circle"></i>
          </div>
        ) : null}
      </div>
    </>
  );
};

export default Login;
