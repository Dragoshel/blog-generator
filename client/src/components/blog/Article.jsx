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

			setBody(body);
			setTitle(title);
		};

		setArticle();
	}, [])

	return (
		<section className="p-5">
			<form className="bg-gray-900/80 hover:bg-gray-900 transition duration-75 ring-2 ring-red-900 shadow-boxy text-gray-900 p-5">
				<ReactMarkdown className="text-slate-50">
					{body}
				</ReactMarkdown>
			</form>
		</section>

	);
};

export default Article;
