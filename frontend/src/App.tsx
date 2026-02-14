import { useState } from "react";
import "./App.css";
import PageOne from "./pages/PageOne";

export default function App() {
  const [currentPage, setCurrentPage] = useState<"home" | "page-one">("home");

  const handleButtonClick = () => {
    setCurrentPage("page-one");
  };

  const handleBackHome = () => {
    setCurrentPage("home");
  };

  return (
    <>
      {currentPage === "home" ? (
        <div className="App">
          <h1>Welcome to the App</h1>
          <p>Coming soon...</p>
          <button onClick={handleButtonClick}>Sample Test API</button>
        </div>
      ) : (
        <div>
          <PageOne onBack={handleBackHome} />
        </div>
      )}
    </>
  );
}
