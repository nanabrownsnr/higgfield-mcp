import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "../../dist/ui_file_dir",
    assetsInlineLimit: 0,
    manifest: true,
    rollupOptions: {
      external: ["@modelcontextprotocol/ext-apps-react"],
    },
  },
});