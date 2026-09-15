import { Routes, Route } from "react-router-dom";
import GamePage from "./pages/GamePage";
import RulesPage from "./pages/RulesPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<GamePage />} />
      <Route path="/rules" element={<RulesPage />} />
    </Routes>
  );
}
