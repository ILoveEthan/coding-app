import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import axios from 'axios';
import { registerFormRules, loginFormRules } from './form-rules.js';
import FormErrors from './FormErrors';

class Form extends Component {
  constructor(props) {
    super(props);
    this.state = {
      formData: {
        username: '',
        email: '',
        password: ''
      },
      valid: false,
      registerFormRules: registerFormRules,
      loginFormRules: loginFormRules,
    };
    this.handleFormChange = this.handleFormChange.bind(this);
    this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
  };
  componentDidMount() {
    this.clearForm();
  };
  componentWillReceiveProps(nextProps) {
    if (this.props.formType !== nextProps.formType) {
      this.clearForm();
      this.resetRules();
    };
  };
  clearForm() {
    this.setState({
      formData: {username: '', email: '', password: ''}
    });
  };
  handleFormChange(event) {
    const obj = this.state.formData;
    obj[event.target.name] = event.target.value;
    this.setState(obj);
    this.validateForm();
  };
  handleUserFormSubmit(event) {
    event.preventDefault();
    const formType = window.location.href.split('/').reverse()[0];
    let data = {
      email: this.state.formData.email,
      password: this.state.formData.password,
    }
    if (formType === 'register') {
      data.username = this.state.formData.username;
    }
    const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${formType}`;
    axios.post(url, data)
    .then((res) => {
      this.clearForm();
      console.log(res.data);
      this.props.loginUser(res.data.auth_token);
    })
    .catch((err) => {
      console.log(err);
    })
  };
  allTrue() {
    let formRules = this.state.registerFormRules;
    if ( this.props.formType === 'Login') {
      formRules = this.state.loginFormRules;
    }
    for (const rule of formRules) {
      if (!rule.valid) return false;
    }
    return true;
  };
  resetRules() {
    if (this.props.formType === 'Login') {
      const formRules = this.state.loginFormRules.slice();
      for (const rule of formRules) {
        rule.valid = false;
      }
      this.setState({loginFormRules: formRules})
    }
    if (this.props.formType === 'Register') {
      const formRules = this.state.registerFormRules.slice();
      for (const rule of formRules) {
        rule.valid = false;
      }
      this.setState({registerFormRules: formRules})
    }
    this.setState({valid: false});
  };
  validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
  }
  validateForm() {
    const self = this;
    const formData = self.state.formData;
    self.resetRules();
    if (self.props.formType === 'Register') {
      const formRules = self.state.registerFormRules.slice();
      if (formData.username.length > 5) formRules[0].valid = true;
      if (formData.email.length > 5) formRules[1].valid = true;
      if (self.validateEmail(formData.email)) formRules[2].valid = true;
      if (formData.password.length > 10) formRules[3].valid = true;
      self.setState({registerFormRules: formRules});
      if (self.allTrue()) self.setState({valid: true});
    }
    if (self.props.formType === 'Login') {
      const formRules = self.state.loginFormRules.slice();
      if (formData.email.length > 0) formRules[0].valid = true;
      if (formData.password.length > 0) formRules[1].valid = true;
      self.setState({loginFormRules: formRules});
      if (self.allTrue()) self.setState({valid: true});
    }
  };
  render() {
    if (this.props.isAuthenticated) {
      return <Redirect to='/' />;
    };
    let formRules = this.state.registerFormRules;
    if ( this.props.formType === 'Login') {
      formRules = this.state.loginFormRules;
    }
    return (
      <div>
        <h1>{this.props.formType}</h1>
        <hr/><br/>
        <FormErrors
          formType={this.props.formType}
          formRules={formRules}
        />
        <form onSubmit={(event) => this.handleUserFormSubmit(event)}>
          {this.props.formType === 'Register' &&
            <div className="form-group">
              <input
                name="username"
                className="form-control input-lg"
                type="text"
                placeholder="Enter a username"
                required
                value={this.state.formData.username}
                onChange={this.handleFormChange}
              />
            </div>
          }
          <div className="form-group">
            <input
              name="email"
              className="form-control input-lg"
              type="email"
              placeholder="Enter an email address"
              required
              value={this.state.formData.email}
              onChange={this.handleFormChange}
            />
          </div>
          <div className="form-group">
            <input
              name="password"
              className="form-control input-lg"
              type="password"
              placeholder="Enter a password"
              required
              value={this.state.formData.password}
              onChange={this.handleFormChange}
            />
          </div>
          <input
            type="submit"
            className="btn btn-primary btn-lg btn-block"
            value="Submit"
            disabled={!this.state.valid}
          />
        </form>
      </div>
    )
  };
}

export default Form;