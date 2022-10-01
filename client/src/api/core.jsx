import axios from "./axios";

export const getAllArticlesFiltered = async (filter=10) => {
	const result = await axios.get(`/blog/articles/${filter}`);

	return result.data.data;
};
