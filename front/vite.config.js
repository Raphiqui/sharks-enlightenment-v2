import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

export default defineConfig({
  plugins: [vue()],
  base: "/static/",
  build: {
    manifest: "manifest.json",
    outDir: resolve(__dirname, '../back/back/static'),
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'src/main.js')
      }
    }
  },
  server: {
    host: '0.0.0.0',  // ← Listen on all interfaces
    port: 5173,
    strictPort: true,

    // HMR configuration for Docker
    hmr: {
      host: 'localhost',  // ← Browser connects via localhost
      clientPort: 8080,   // ← Port exposed in docker-compose
    },

    // Watch configuration for Docker volumes
    watch: {
      usePolling: true,
      interval: 1000,
    }
  },
  // Optional: Silence Sass deprecation warnings. See note below.
  css: {
     preprocessorOptions: {
        scss: {
          silenceDeprecations: [
            "import",
            "mixed-decls",
            "color-functions",
            "global-builtin",
            "if-function",
          ],
        },
     },
  },
})
