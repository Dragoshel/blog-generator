import { useRef, useState, useEffect } from "react";
import { register } from "../../api/auth";

const EMAIL_REGEX = /^(?:(?:[\w`~!#$%^&*\-=+;:{}'|,?\/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?\/\.()<>\[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}'|,?\/]+))*\.[\w`~!#$%^&*\-=+;:{}'|,?\/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?\/\.()<>\[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d\-]+(?:\.[a-zA-Z\d\-]+)*|\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\])$/;
const PASSWORD_REGEX = /^.{8,}$/;

const Register = () => {

	const [email, setEmail] = useState("");
	const emailRef = useRef();

	const [password, setPassword] = useState("");
	const [confirmPassword, setConfirmPassword] = useState("");

	const [error, setError] = useState("");
	const [success, setSuccess] = useState("");

	const handleSubmit = async (e) => {
		e.preventDefault();

		const v1 = EMAIL_REGEX.test(email);
		const v2 = PASSWORD_REGEX.test(password);

		if (!v1) {
			setError("Invalid email");
			return;
		}

		if (!v2) {
			setError("Invalid password");
			return;
		}

		if (password !== confirmPassword) {
			setError("Passwords don't match");
			return;
		}

		try {
			await register(email, password);

			setSuccess(`Created account with ${email}`);
		} catch (error) {
			setError(error?.response?.data?.error);
			setSuccess("");
		}
	};

	useEffect(() => {
		emailRef.current.focus();
		setError("");
		setSuccess("");
	}, []);

	useEffect(() => {
		setError("");
		setSuccess("");
	}, [email, password, confirmPassword]);

	return (
		<section className="min-h-screen grid place-items-center p-5">
			<form className="flex flex-col bg-gray-900/80 hover:bg-gray-900 transition duration-75 ring-2 ring-red-900 shadow-boxy text-gray-900 p-5"
				onSubmit={handleSubmit}>
				<h1 className="text-center text-xl text-slate-50">Register</h1>
				{
					error ? (<p className="text-center text-red-400">{error}</p>) : <></>
				}
				{
					success ? (<p className="font-bold text-center text-green-400">{success}</p>) : <></>
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

				<label className="text-slate-50 font-bold mb-2 mt-3" htmlFor="password-input">Confirm Password</label>
				<input className="px-3"
					id="confirm-password-input"
					type="password"
					value={confirmPassword}
					onChange={(e) => setConfirmPassword(e.target.value)}
				/>

				<button className="bg-red-700 hover:bg-red-800 shadow font-bold text-slate-50 mb-2 mt-5">Register</button>
			</form>
		</section>
	);
};

export default Register;
