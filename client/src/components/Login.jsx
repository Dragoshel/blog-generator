import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Home from "./Home";

const Login = () => {

	const [email, setEmail] = useState("");
	const [pwd, setPwd] = useState("");

	const [err, setErr] = useState("");

	const navigate = useNavigate();

	const handleSubmit = async (e) => {
	
		e.preventDefault();

		const URL = "http://localhost:5000/login";

		const payload = new FormData();
		payload.append("email", email);
		payload.append("password", pwd);

		const options = {
			method: "POST",
			body: payload
		};

		const response = await fetch(URL, options);
		const data = await response.json();

		if (response.status !== 200) {

			setErr(data.error);

		} else {

			localStorage.setItem("access_token", data.data.access_token);
			localStorage.setItem("refresh_token", data.data.refresh_token);

			navigate("/");
		}	
	};


	return (

		<section className="bg-slate-900 text-slate-50">
			<div className="min-h-screen max-w-md grid grid-cols-1 place-content-center mx-auto">
				<form className="flex flex-col ring-1 ring-red-900 shadow-boxy p-5" onSubmit={handleSubmit}>
				<h1 className="text-xl">Log In</h1>
					<label htmlFor="email">Email</label>
					<input className="bg-slate-50 text-zinc-900"
						type="text"
						id="email"
						required
						value={email}
						onChange={(e) => setEmail(e.target.value)}
					/>
					<label className="mt-5" htmlFor="pwd">Password</label>
					<input className="bg-slate-50 text-zinc-900"
						type="password"
						id="pwd"
						required
						value={pwd}
						onChange={(e) => setPwd(e.target.value)}
					/>
					<p>{err}</p>
					<button className="bg-red-400 text-slate-900 mt-5">Log In</button>
				</form>
				
			</div>
		</section>
	);
};

export default Login;
