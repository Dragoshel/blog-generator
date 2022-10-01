import { useEffect, useState } from "react";
import useAxiosProtected from "../../hooks/useAxiosProtected";
import { Outlet } from "react-router-dom";


const PersistLogin = () => {
	const [loaded, setLoaded] = useState(false);
	const axiosProtected = useAxiosProtected();

	useEffect(() => {
		const checkPersistLogin = async () => {
			try {
				await axiosProtected.get("/authorized");
			} catch {

			} finally {
				setLoaded(true);
			}
		};

		checkPersistLogin();
	}, []);


	return (
		loaded 
			? <Outlet />
			: <></>
	);
};

export default PersistLogin;
