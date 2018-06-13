import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { authenticate } from '../actions';

const AuthButton = ({ children, onClick }) => (
  <button
    onClick={onClick}
  >
    {children}
  </button>
)

AuthButton.propTypes = {
  children: PropTypes.node.isRequired,
  onClick: PropTypes.func.isRequired
}

const mapDispatchToProps = dispatch => {
  return {
    onClick: () => dispatch(authenticate())
  }
}

export default connect(null, mapDispatchToProps)(AuthButton)