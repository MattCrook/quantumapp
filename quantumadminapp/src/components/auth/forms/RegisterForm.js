import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import { Input } from "@material-ui/core";
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
          <TextField
            id="email"
            label="Email"
            color="secondary"
            type="email"
            onChange={props.handleInput}
          >
            <Input value={props.credentials.email} />
          </TextField>
          <TextField
            id="username"
            type="text"
            label="Username"
            color="secondary"
            onChange={props.handleInput}
          >
            <Input value={props.credentials.username} />
          </TextField>
          <TextField
            id="oldPassword"
            type="password"
            label="Old Password"
            color="secondary"
            onChange={props.handleInput}
          >
            <Input value={props.credentials.oldPassword} />
          </TextField>
          <TextField
            id="newPassword"
            type="password"
            label="New Password"
            color="secondary"
            onChange={props.handleInput}
          >
            <Input value={props.credentials.newPassword} />
          </TextField>
          <TextField
            id="newPassword2"
            label="Confirm New Password"
            type="password"
            color="secondary"
            onChange={props.handleInput}
          >
            <Input value={props.credentials.newPassword2} />
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
