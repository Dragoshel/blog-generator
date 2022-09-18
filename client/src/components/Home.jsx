import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import nature from "../nature.png";

const Home = () => {
	const [articles, setArticles] = useState([]);

	const getAllArticles = async () => {
		const URL = "http://localhost:5000/blog/articles";

		const options = {
			method: "GET"
		};

		const response = await fetch(URL, options);
		const data = await response.json();

		if (response.status === 200) {
			return data.data;
		}

		return undefined;
	};

	useEffect(() => {
		const setAllArticles = async () => {
			const result = await getAllArticles();

			setArticles(result);
		};

		setAllArticles();
	}, [])

	return (
		<section className="min-h-screen bg-image text-slate-50">
			<div className="min-h-screen max-w-7xl md:flex gap-10 mx-auto p-5">
				<div className="self-start max-w-[16rem] md:w-64 shrink-0
								bg-gray-900/80 ring-2 ring-red-900 shadow-boxy">
					<ul className="p-5">
						<li><Link to="/">Home</Link></li>
						<li><Link to="/register">Register</Link></li>
						<li><Link to="/login">Article Builder</Link></li>
					</ul>
				</div>
				<div className="self-start w-full
								bg-gray-900/80 ring-2 ring-red-900 shadow-boxy mt-5 md:mt-0 p-5">
					<p className="font-extrabold">These are the first lines of text of my first ever website.</p>
					<p>Here you will find very cool and interesting stuff about technology, philosopy and random thoughts.</p>
					<br />
					<p>Available articles:</p>					
					{
						articles !== undefined || articles.length > 0 ? 
							(
								<ul>
									{articles.map((article) => (
										<li key={article.id} className="hover:text-sky-500">
											<Link to={`/blog/article/${article.id}`}>
												{article.title}
											</Link>
										</li>
									))}
								</ul>
							) : (<p>No articles at the moment.</p>)
					}
				</div>
			</div>
		</section>
	);
};

export default Home;
