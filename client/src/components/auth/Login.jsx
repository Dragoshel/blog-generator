import { useEffect, useRef, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "../../api/auth";

const Login = () => {
	const [email, setEmail] = useState("");
	const emailRef = useRef();

	const [password, setPassword] = useState("");

	const [error, setError] = useState("");

	const navigate = useNavigate();

	const handleSubmit = async (e) => {
		e.preventDefault();

		if (!email || !password) {
			setError("Email or password empty"); return;			
		}

		try {
			const result = await login(email, password);
			const data = result?.data;

			localStorage.setItem("access_token", data.access_token);
			localStorage.setItem("refresh_token", data.refresh_token);

			navigate("/builder");
		} catch (error) {
			setError(error?.response?.data?.error);
		}
	};

	useEffect(() => {
		emailRef.current.focus();
		setError("");
	}, []);

	useEffect(() => {
		setError("");
	}, [email, password]);

	return (
		<section className="min-h-screen grid place-items-center p-5">
			<form className="flex flex-col bg-gray-900/80 hover:bg-gray-900 transition duration-75 ring-2 ring-red-900 shadow-boxy text-gray-900 p-5"
				onSubmit={handleSubmit}>
				<h1 className="text-center text-xl text-slate-50">LogIn</h1>
				{
					error ? (<p className="text-center text-red-400">{error}</p>) : <></>
				}
				<label className="text-slate-50 font-bold mb-2" htmlFor="email-input">Email</label>
				<input className="px-3"
					id="email-input"
					type="text"
					value={email}
					ref={emailRef}
					onChange={(e) => setEmail(e.target.value)}
				/>

				<label className="text-slate-50 font-bold mb-2 mt-3" htmlFor="password-input">Password</label>
				<input className="px-3"
					id="password-input"
					type="password"
					value={password}
					onChange={(e) => setPassword(e.target.value)}
				/>
				<button className="bg-red-700 hover:bg-red-800 shadow font-bold text-slate-50 mt-5">Login</button>
				<Link className="" to="/register">
					<span className="float-right underline hover:text-sky-500 text-slate-50 mt-3">
					Register
					</span>
				</Link>
			</form>
		</section>
	);
};

export default Login;
