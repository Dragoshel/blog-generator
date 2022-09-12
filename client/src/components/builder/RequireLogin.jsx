import { Navigate, Outlet } from "react-router-dom";
import useAuth from "../../hooks/UseAuth";


const RequireLogin = () => {
	const { user, isLoading } = useAuth();

	if (isLoading) {
		return <p>Stand by, still loading...</p>
	}

	if (user) {
		return <Outlet />
	} else {
		return <Navigate to="/login" replace />
	}
};

export default RequireLogin;
