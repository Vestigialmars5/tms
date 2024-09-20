import { Route } from "react-router-dom";
import AdminDashboard from "../pages-new/admin/AdminDashboard";
import { Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthProvider";
import { Navigate } from "react-router-dom";
import { useSelector } from "react-redux";

const AdminRoute = () => {
  const required = 1;
  const authState = useSelector((state) => state.auth);

  if (!authState.isAuthenticated) {
    console.log("Not Authenticated, Redirecting To Login");
    return <Navigate to="/login" />;
  }

  if (authState.user.roleId !== required) {
    console.log("User not authorized, redirecting to home");
    return <Navigate to="/home" />;
  }

  return <Outlet />;
};

export default AdminRoute;