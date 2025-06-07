import { createBrowserRouter } from "react-router-dom";
import MainPage from "../pages/main";
import Greeting from "../pages/greetings";
import Auth from "../pages/auth";
const Router = createBrowserRouter([
    {
        path: "/",
        element: <MainPage />,
    },
    {
        path: '/register',
        element: <Greeting />
    },
    {
        path: '/auth',
        element: <Auth />
    }
]);

export default Router;
