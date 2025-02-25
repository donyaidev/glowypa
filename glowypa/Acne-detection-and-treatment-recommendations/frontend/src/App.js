import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Diagnosis from "./pages/Diagnosis.js";
import Test from "./pages/Test.js";
import Demo from "./pages/Demo.js"
import Login from "./pages/Login.js";
import ProtectedRoute from "./components/ProtectedRoute"; 
import "./app.css";
import {useSelector} from "react-redux"; 
import Notication from "./components/Notification"; 
const App = () => {
  const isLoggedIn = useSelector((state) => state.user.isLoggedIn);
  const router = createBrowserRouter([
    { path: "/", element: <Login/> }, 
    {
      path: "/diagnosis",
      element: <ProtectedRoute element={<Diagnosis />} isLoggedIn={isLoggedIn} />,
    },
    // {
    //   path: "/demo",
    //   element: <ProtectedRoute element={<Demo />} isLoggedIn={isLoggedIn} />,
    // },
  ]);

  return (
    <main>
      <Notication />
      <RouterProvider router={router} />
    </main>
  );
};

export default App;
