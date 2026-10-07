import ReactDOM from 'react-dom/client';

export function useApp() {
  return {
    fetchTool: async (name, params) => {
      const res = await fetch(`/api/v1/tools/${name}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params),
      });
      return res.json();
    },
  };
}

export function hydrate(element, root) {
  ReactDOM.createRoot(root).render(element);
}
