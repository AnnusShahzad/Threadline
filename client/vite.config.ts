import { defineConfig } from "vite";

export default defineConfig({
  server: {
    // The canvas calls the backend same-origin in production; the dev server mimics that,
    // so no CORS middleware is needed on the backend.
    proxy: { "/api": "http://127.0.0.1:8000" },
  },
  build: { outDir: "dist" },
});
