import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import { Input } from "@material-ui/core";
import HelpIcon from "@material-ui/icons/Help";
import "../styles/Register.css";

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
    },
  },
}));

const RegisterForm = (props) => {
  const classes = useStyles();

  return (
    <>
      <div className="form_container" onSubmit={props.handleSubmit}>
        <form
          id="auth_form"
          className={classes.root}
          noValidate
          autoComplete="off"
        >
          <TextField label="Username" color="secondary">
            <Input
              id="username"
              type="text"
              value={props.username}
              onChange={props.handleEmail}
            />
          </TextField>
          <TextField label="Old Password" color="secondary">
            <Input
              id="old_password"
              type="password"
              value={props.old_password}
              onChange={props.handleEmail}
            />
          </TextField>
          <TextField label="New Password" color="secondary">
            <Input
              id="new_password"
              type="password"
              value={props.password1}
              onChange={props.handleEmail}
            />
          </TextField>
          <TextField label="Confirm New Password" color="secondary">
            <Input
              id="new_password2"
              type="password"
              value={props.password2}
              onChange={props.handleEmail}
            />
          </TextField>
          <div className="register_btn_wrapper">
            <button className="admin_login_submit_button" type="submit">
              Register
            </button>
          </div>
        </form>
      </div>
    </>
  );
};

export default RegisterForm;
