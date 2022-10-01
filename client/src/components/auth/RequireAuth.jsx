import useAuth from "../../hooks/useAuth";
import { Outlet, Navigate, useLocation } from "react-router-dom";

const RequireAuth = () => {
	const { auth } = useAuth();
	const location = useLocation();

	return (
		auth
			? <Outlet />
			: <Navigate to="/login" state={{ from: location }} replace />
	);
};

export default RequireAuth;
