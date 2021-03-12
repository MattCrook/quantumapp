import React, { useRef, useState } from "react";
import LoginNav from "../nav/LoginNav";
import AuthForm from "./LoginForm";
import authUserManager from "../../modules/authUserManager";
import { useAuthUser } from "../../contexts/AuthUserContext";
import "./styles/Login.css";

const Login = (props) => {
  const { setDjangoToken, setAuthToken } = useAuthUser();
  const [error, setError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isValidating, setIsValidating] = useState(false);
  const [success, setSuccess] = useState(false);
  const email = useRef();
  const password = useRef();
  const showError = (message) => {
    setIsValidating(false);
    setError(true);
    setErrorMessage(message);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsValidating(true);
    const loginCredentials = {
      email: email.current.value,
      password: password.current.value,
    };

    try {
      const response = await authUserManager.adminLogin(loginCredentials);
      if (response.valid === true) {
        setIsValidating(false);
        setSuccess(true);
        setDjangoToken(response);
        setAuthToken(response.token);
        sessionStorage.setItem("email", response.email);
        props.history.push("quantumadmin/home");
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
          handleSubmit={handleSubmit}
          email={email}
          password={password}
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
