import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vite.dev/config/
export default defineConfig({
    server: {
        watch: {
            usePolling: true,
        },
        host: "0.0.0.0",
        port: 5173,
    },
    plugins: [vue()],
    build: {
        outDir: "dist",
    },
});
