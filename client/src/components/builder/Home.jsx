import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./index.css";

const Home = () => {

	const [content, setContent] = useState("");



	return (
		<section className="p-5">
			<form className="bg-gray-900/80 hover:bg-gray-900 transition duration-75 ring-2 ring-red-900 shadow-boxy text-gray-900 p-5">
				<textarea className="w-full p-5"
					placeholder="Begin typing here..."
					value={content}
					onChange={(e) => setContent(e.target.value)}
				>
				</textarea>
				<ReactMarkdown className="text-slate-50">
					{content}
				</ReactMarkdown>
				<button className="bg-red-700 hover:bg-red-800 shadow font-bold text-slate-50 mt-5 p-1">Create article</button>
			</form>
		</section>
	);
};

export default Home;
