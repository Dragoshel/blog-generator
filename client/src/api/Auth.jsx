import axios from "./Axios";

export const verifyAccess = async (access_token) => {
	try {
		const result = await axios.get("/authenticate", {
			headers: {
				Authorization: `Bearer ${access_token}`
			}
		});

		return {
			ok: result.data.data.email,
			err: null
		};

	} catch (err) {

		console.log(err);

		if (err.response.data.error === "Token has expired.") {
			return {
				ok: null,
				err: err.response.data.error
			};
		}

		return { ok: null, err: err }
	}
};

export const renewAccess = async (refresh_token) => {
	try {
		const payload = new FormData();
		payload.append("token", refresh_token);


		const result = await axios.post("/token", payload)

		console.log(`Here ${result}`);

		return {
			ok: result.data.data.token,
			err: null
		};

	} catch (err) {
		if (err.response.data.error === "Token has expired.") {
			return {
				ok: null,
				err: err.response.data.error
			};
		}

		return { ok: null, err: err }
	}
}
