import { useApp, hydrate } from "@modelcontextprotocol/ext-apps-react";
import { useEffect, useState } from "react";

export function App() {
  const { fetchTool } = useApp();
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetchTool("list_dir", { path: "." })
      .then((r) => r.json())
      .then((json) => setItems(json.items))
      .catch(console.error);
  }, [fetchTool]);

  return (
    <div>
      <h1>File Directory</h1>
      <ul>
        {items.map((it) => (
          <li key={it.name}>
            {it.name} ({it.type})
          </li>
        ))}
      </ul>
    </div>
  );
}

hydrate(<App />, document.getElementById("app-root"));
