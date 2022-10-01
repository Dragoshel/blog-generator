import axios from "./axios";

export const refresh = async (refreshToken) => {
	const config = {
		headers: {
			Authorization: `Bearer ${refreshToken}`
		}
	};

	const result = await axios.post("/token", {}, config);

	return result?.data;
}

export const login = async (email, password) => {
	const payload = new FormData();
	payload.append("email", email);
	payload.append("password", password);

	const result = await axios.post("/login", payload);

	return result?.data;
};

export const register = async (email, password) => {
	const payload = new FormData();
	payload.append("email", email);
	payload.append("password", password);

	const result = await axios.post("/register", payload);

	return result?.data;	
};
