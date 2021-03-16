import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import { Input } from "@material-ui/core";
import HelpIcon from '@material-ui/icons/Help';
import "../styles/Login.css"

const useStyles = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(1),
      width: "35ch",
      display: "flex",
      flexDirection: "column",
      color: "white",
    },
    text: {
      color: "white",
    }
  },
}));

const AuthForm = (props) => {
  const classes = useStyles();


  return (
    <>
      <div className="form_container" onSubmit={props.handleSubmit}>
        <form id="auth_form" className={classes.root} noValidate autoComplete="off">
          <TextField id="email"  label="Email" type="email" color="secondary" onChange={props.handleEmail}>
            <Input type="email" color="secondary" value={props.email} />
          </TextField>
          <TextField id="password"  label="Password" type="password" color="secondary" onChange={props.handlePassword}>
            <Input type="password" color="secondary" value={props.password}/>
          </TextField>
          <div className="login_btn_wrapper">
          <button className="admin_login_submit_button" type="submit">Login</button>
          </div>
          <div id="register_link_wrapper">
          <div className="register_admin_link" onClick={() => props.history.push("/quantumadmin/register/")}>Register Your Admin Account </div>
          <HelpIcon />
          </div>
        </form>
      </div>
    </>
  );
}

export default AuthForm;
