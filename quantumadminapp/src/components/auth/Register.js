import React, { useState } from "react";
import LoginNav from "../nav/LoginNav";
import authUserManager from "../../modules/authUserManager";
import { useAuthUser } from "../../contexts/AuthUserContext";
import RegisterForm from "./forms/RegisterForm";
import "./styles/Register.css";

const Register = (props) => {
  const [credentials, setCredentials] = useState({});
  const { setDjangoToken, setAuthToken } = useAuthUser();
  const [error, setError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isValidating, setIsValidating] = useState(false);
  const [success, setSuccess] = useState(false);
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
      username: credentials.username,
      oldPassword: credentials.oldPassword,
      newPassword: credentials.newPassword,
      newPassword2: credentials.newPassword2,
    };
    if (credentials.newPassword !== credentials.newPassword2) {
      showError("Passwords did not match.");
    }

    try {
      var registeredAdminUser = authUserManager.registerAdminUser(registerFormData);
      if (registeredAdminUser.valid === true) {
        setIsValidating(false);
        setSuccess(true);
        setAuthToken(response.token);
        setDjangoToken(response);
        sessionStorage.setItem("email", response.email);
        props.history.push("/quantumadmin/home");
      }
    } catch (error) {
      console.log(error);
      showError("There was a problem. Please try again.");
    }
  };

  return (
    <>
      <LoginNav {...props} />
      <div
        className="back_to_previous"
        onClick={() => props.history.push("/quantumadmin/login")}
      >
        {" "}
        &lt; Back To Previous
      </div>
      <div id="register_form_master_container">
        <RegisterForm
          handleInput={handleInput}
          credentials={credentials}
          handleSubmit={handleSubmit}
          {...props}
        />
      </div>
    </>
  );
};

export default Register;
