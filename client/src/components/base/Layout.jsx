import { Outlet } from "react-router-dom";

const Layout = () => {
	return (
		<main className="font-mono">
			<Outlet />
		</main>
	);
};

export default Layout;
