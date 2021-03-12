import React from "react";
import LoginNav from "../nav/LoginNav";
import AuthForm from "./LoginForm";
import "./styles/Login.css";

const Login = (props) => {
  return (
    <>
      <LoginNav {...props} />
          <div id="login_master_container">
              <AuthForm {...props}/>
              
      </div>
    </>
  );
};

export default Login;
