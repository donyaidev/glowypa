import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ element, isLoggedIn }) => {
  return isLoggedIn ? element : <Navigate to="/" />;
};

export default ProtectedRoute;
