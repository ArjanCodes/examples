import { ConvexProvider, ConvexReactClient } from "convex/react";
import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
// import "./index.css";

console.log(import.meta.env);
const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ConvexProvider client={convex}>
      <App />
    </ConvexProvider>
  </StrictMode>,
);
