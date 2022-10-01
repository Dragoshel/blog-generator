import { useEffect } from "react";
import useAuth from "./useAuth";
import { refresh } from "../api/auth";
import { axiosProtected } from "../api/axios";

const useAxiosProtected = () => {
	const { setAuth } = useAuth();

	useEffect(() => {
		const request = axiosProtected.interceptors.request.use(
			config => {

				const accessToken = localStorage.getItem("access_token");

				config.headers["Authorization"] = `Bearer ${accessToken}`;

				return config;
			},
			error => Promise.reject(error)
		);

		const response = axiosProtected.interceptors.response.use(
			response => { setAuth(true); return response },
			async (error) => {
				const prevRequest = error?.config;

				if (error?.response?.status === 401 && !prevRequest?.sent) {
					prevRequest.sent = true;
					const wwwAuth = error.response.headers["www-authenticate"];
					const wwwAuthData = JSON.parse(wwwAuth.split("=")[1]);

					if (wwwAuthData?.error === "expired_token") {
						try {
							const refreshToken = localStorage.getItem("refresh_token");
							const result = await refresh(refreshToken);
							const newAccessToken = result?.data?.token;

							localStorage.setItem("access_token", newAccessToken);

							return axiosProtected(prevRequest);
						} catch {
						}
					}
				}

				setAuth(false); return Promise.reject(error);
			}
		);

		return () => {
			axiosProtected.interceptors.response.eject(response);
			axiosProtected.interceptors.request.eject(request);
		};
	}, []);

	return axiosProtected;
};

export default useAxiosProtected;
