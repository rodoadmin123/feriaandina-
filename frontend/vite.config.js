import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// El "proxy" reenvia /api y /media al servidor Django (puerto 8000).
// Asi React y Django "conversan" sin problemas de CORS en desarrollo.
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // permite abrirlo desde el celular en la misma red WiFi
    port: 5173,
    proxy: {
      "/api": "http://127.0.0.1:8000",
      "/media": "http://127.0.0.1:8000",
    },
  },
});
