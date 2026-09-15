import { Routes, Route } from "react-router-dom";
import GamePage from "./pages/GamePage.jsx";
import RulesPage from "./pages/RulesPage.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<GamePage />} />
      <Route path="/rules" element={<RulesPage />} />
    </Routes>
  );
}
