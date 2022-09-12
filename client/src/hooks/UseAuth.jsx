import { useState, useEffect } from "react";
import { verifyAccess, renewAccess } from "../api/Auth";

const useAuth = () => {
	const [user, setUser] = useState({});
	const [isLoading, setLoading] = useState(true);

	const setRenewAccess = async () => {
		const refresh_token = localStorage.getItem("refresh_token");

		if (!refresh_token) {
			console.log("Refresh token is missing.");
		}

		const result = await renewAccess(refresh_token);

		if (result.err === "Token has expired.") {
			console.log("Refresh token has expired.")
			return undefined;
		}

		return result.ok;
	};

	const setVerifyAccess = async () => {
		var accessToken = localStorage.getItem("access_token");

		if (!accessToken) {
			console.log("Access token is missing");
			setLoading(false);
		}

		const result = await verifyAccess(accessToken);

		if (result.err === "Token has expired.") {
			accessToken = await setRenewAccess();

			if (accessToken) {
				localStorage.setItem("access_token", accessToken);
			}
		}

		setUser(result.ok);
		setLoading(false);
	};

	useEffect(() => {
		setVerifyAccess();
	}, []);

	return { user, isLoading };
};

export default useAuth;
