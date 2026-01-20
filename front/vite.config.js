import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";
import tailwindcss from "@tailwindcss/vite"

export default defineConfig({
  plugins: [vue(), tailwindcss()],
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
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,

    // HMR configuration for Docker
    hmr: {
      host: 'localhost',  // ← Browser connects via localhost
      clientPort: 8080,   // ← Port exposed in docker-compose
    },

    watch: {
      usePolling: true,
      interval: 1000,
    }
  },
  
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
