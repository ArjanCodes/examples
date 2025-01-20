import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";


export default function App() {
  const metrics = useQuery(api.metrics.retrieve);


  return (
    <main>
      <header>
        <h1>Real-Time Metrics Dashboard</h1>
      </header>
      <div>
      <ul>
        {metrics?.map((metric) => (
          <li key={metric.name}>
            {metric.name}: {metric.value}
          </li>
        ))}
      </ul>
      </div>
    
    </main>
  );
}

