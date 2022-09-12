import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/base/Layout"; 
import Home from "./components/Home";
import Login from "./components/Login";

import RequireLogin from "./components/builder/RequireLogin";


const App = () => {
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Layout />}>
					<Route path="/" element={<Home />} />
					<Route path="/login" element={<Login />} />
				</Route>
			</Routes>
		</BrowserRouter>
	);
};

export default App;
