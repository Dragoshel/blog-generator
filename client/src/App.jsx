import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/base/Layout"; 
import Home from "./components/Home";
import Login from "./components/Login";
import Article from "./components/blog/Article";



const App = () => {
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Layout />}>
					<Route path="/" element={<Home />} />
					<Route path="/login" element={<Login />} />
					<Route path="/blog/article/:id" element={<Article />} />
				</Route>
			</Routes>
		</BrowserRouter>
	);
};

export default App;
