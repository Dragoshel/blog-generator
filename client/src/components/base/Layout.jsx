import { Outlet } from "react-router-dom";

const Layout = () => {
	return (
		<main className="min-h-screen font-mono font-bold">
			<Outlet />
		</main>
	);
};

export default Layout;
