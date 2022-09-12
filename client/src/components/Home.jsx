import { Link } from "react-router-dom";

const Home = () => {
	return (
		<section className="min-h-screen bg-slate-900 text-slate-50 py-5">
			<div className="max-w-7xl flex gap-5 mx-auto">
				<div className="flex-none w-52 ring-1 ring-red-900 shadow-boxy">
					<ul className="p-5">
						<li><Link to="/">Home</Link></li>
						<li><Link to="/">Blog</Link></li>
						<li><Link to="/">Register</Link></li>
						<li><Link to="/login">Article Builder</Link></li>
					</ul>
				</div>
				<div className="shrink w-full ring-1 ring-red-900 shadow-boxy p-5">
					<p>These are the first lines of text of my first ever website</p>
					<p>Here you will find very cool and interesting stuff about technology, philosopy and random thoughts</p>
				</div>
			</div>
		</section>
	);
};

export default Home;
