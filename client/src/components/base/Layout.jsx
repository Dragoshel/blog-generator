import { Outlet } from "react-router-dom";
import bench from "../../assets/img/bench.png";
import jungle from "../../assets/img/jungle.png";
import mud from "../../assets/img/mud.png";
import river from "../../assets/img/river.png";
import ponton1 from "../../assets/img/ponton1.png";
import ponton2 from "../../assets/img/ponton2.png";

const Layout = () => {

	const body = document.getElementsByTagName("body")[0];

	const backgroundImages = [bench, jungle, mud, ponton1, ponton2, river];
	const randomImage = backgroundImages[Math.floor(Math.random() * backgroundImages.length)];

	body.style.backgroundImage = `linear-gradient(#1118279e 100%, #1118279e), url('${randomImage}')`;

	return (
		<main className="max-w-7xl font-mono text-slate-50 mx-auto">
			<Outlet />
		</main>
	);
};

export default Layout;
