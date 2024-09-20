// Make sure user is logged out to access pages protected by this route

import React from "react";
import { Navigate } from "react-router-dom";
import { Outlet } from "react-router-dom";
import { useSelector } from "react-redux";

const PublicRoute = () => {
  const authState = useSelector((state) => state.auth);

  if (authState.isAuthenticated) {
    return <Navigate to="/home" />;
  }

  return <Outlet />;
};

export default PublicRoute;