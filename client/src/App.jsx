import { BrowserRouter, Routes, Route } from "react-router-dom";
// Layout
import Layout from "./components/base/Layout"; 

// Auth
import Register from "./components/auth/Register";
import Login from "./components/auth/Login";
import RequireAuth from "./components/auth/RequireAuth";

// Blog
import Article from "./components/blog/Article";

// Builder
import BuilderHome from "./components/builder/Home";

// Index
import Home from "./components/Home";
import PersistLogin from "./components/auth/PersistLogin";

const App = () => {
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Layout />} >
					<Route path="" element={<Home />} />
					<Route path="login" element={<Login />} />
					<Route path="register" element={<Register />} />
					<Route path="builder" element={<PersistLogin />} >
						<Route path="" element={<RequireAuth />} >
							<Route path="" element={<BuilderHome />} />
						</Route>
					</Route>
					<Route path="/blog/article/:id" element={<Article />} />
				</Route>
			</Routes>
		</BrowserRouter>
	);
};

export default App;
