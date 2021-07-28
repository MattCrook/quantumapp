import React, { useState } from "react";
import LoginNav from "../nav/LoginNav";
import authUserManager from "../../modules/authUserManager";
import { useAuthUser } from "../../contexts/AuthUserContext";
import RegisterForm from "./forms/RegisterForm";
import "./styles/Register.css";

const Register = (props) => {
  const [credentials, setCredentials] = useState({
    email: "",
    username: "",
    oldPassword: "",
    newPassword: "",
    newPassword2: "",
  });
  const { setDjangoToken, setAuthToken, setIsAuthenticated, setAuthUserData } = useAuthUser();
  const [error, setError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isValidating, setIsValidating] = useState(false);
  const [success, setSuccess] = useState(false);
  // ToDo: set warning/ spinner alerts
  const showError = (message) => {
    setIsValidating(false);
    setError(true);
    setErrorMessage(message);
  };

  const handleInput = (e) => {
    const inputState = { ...credentials };
    inputState[e.target.id] = e.target.value;
    setCredentials(inputState);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    var registerFormData = {
      email: credentials.email,
      username: credentials.username,
      oldPassword: credentials.oldPassword,
      newPassword: credentials.newPassword,
      newPassword2: credentials.newPassword2,
    };
    if (credentials.newPassword !== credentials.newPassword2) {
      showError("Passwords did not match.");
    }

    try {
      var registeredAdminUser = await authUserManager.registerAdminUser(registerFormData);
      if (registeredAdminUser.valid === true) {
        setIsValidating(false);
        setSuccess(true);
        setDjangoToken(registeredAdminUser);
        setAuthToken(registeredAdminUser.token);
        sessionStorage.setItem("email", registeredAdminUser.email);
        setIsAuthenticated(true);
        setAuthUserData(registeredAdminUser);

        // ToDo: set is logged in to true (user profile table)
        // props.history.push("/quantumadmin/");
        const origin = window.location.origin;
        window.location.href = origin + "/quantumadmin/";
      } else {
        showError("Credentials you entered are incorrect.");
      }
    } catch (error) {
      console.log(error);
      showError("There was a problem. Please try again.");
    }
  };

  return (
    <>
      <LoginNav {...props} />
      <div className="back_to_previous" onClick={() => props.history.push("/quantumadmin/login")}>
        {" "}
        &lt; Back To Login
      </div>
      <div id="register_form_master_container">
        <RegisterForm
          handleInput={handleInput}
          credentials={credentials}
          handleSubmit={handleSubmit}
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

export default Register;
