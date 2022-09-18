import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { useParams } from "react-router-dom";

const Article = () => {

	const [body, setBody] = useState();
	const [title, setTitle] = useState();

	const params = useParams();

	const getArticle = async (id) => {
		const URL = `http://localhost:5000/blog/article/${id}`;

		const options = {
			method: "GET"
		}

		const response = await fetch(URL, options);
		const data = await response.json();

		if (response.status === 200) {
			return data.data;
		}

		return undefined;
	};

	useEffect(() => {	
		const setArticle = async () => {
			const result = await getArticle(params.id);
			const title = result.title;
			const body = result.body;

			console.log(title);
			console.log(body);

			setBody(body);
			setTitle(title);
		};

		setArticle();
	}, [])

	return (
		<section className="min-h-screen bg-image text-slate-50">
			<div className="max-w-7xl mx-auto p-5">
				<ReactMarkdown className="w-full bg-gray-900/80 ring-2 ring-red-900 shadow-boxy p-5">
					{body}
				</ReactMarkdown>
			</div>
		</section>

	);
};

export default Article;
