import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getAllArticlesFiltered } from "../api/core";

const Home = () => {
	const [articles, setArticles] = useState([]);
	const [loaded, setLoaded] = useState(false);

	useEffect(() => {
		const articles = async () => {
			try {
				const result = await getAllArticlesFiltered(10);

				setArticles(result);
			} catch {

			} finally {
				setLoaded(true);
			}
		}

		articles();
	}, [])

	const aritcleList = () => {
		if (articles?.length < 1) {
			return (<p className="font-bold text-amber-500">No articles at the moment</p>);
		}

		return (
			<ul>
				{articles.map((a) => (
					<li key={a.id}>
						<Link to={`/blog/article/${a.id}`}>
							<span className="underline hover:text-sky-500">
								{a.title}
							</span>
						</Link>
					</li>
				))}
			</ul>
		);
	};

	return (
		<section className="md:flex gap-10 p-5"> 
			<div className="self-start max-w-[16rem] md:w-64 shrink-0
								bg-gray-900/80 hover:bg-gray-900 transition duration-75 ring-2 ring-red-900 shadow-boxy">
				<ul className="p-5">
					<li>
						<Link to="/">
							<span className="underline hover:text-sky-500">
								Home
							</span>
						</Link>
					</li>
					<li>
						<Link to="/register">
							<span className="underline hover:text-sky-500">
								Register
							</span>						
						</Link>
					</li>
					<li>
						<Link to="/builder">
							<span className="underline hover:text-sky-500">
								Create an article
							</span>
						</Link>
					</li>
				</ul>
			</div>
			<div className="self-start w-full
								bg-gray-900/80 hover:bg-gray-900 transition duration-75 ring-2 ring-red-900 shadow-boxy mt-5 md:mt-0 p-5">
				<p className="font-extrabold">These are the first lines of text of my first ever website.</p>
				<p>Here you will find very cool and interesting stuff about technology, philosopy and random thoughts.</p>
				<br />
				<p>Available articles:</p>
				{
					loaded
						? aritcleList()
						: <p className="font-bold text-amber-500">Loading...</p>
				}
			</div>
		</section>
	);
};

export default Home;
