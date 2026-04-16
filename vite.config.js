import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite"; // <--- Đổi từ 'tailwindcss' thành '@tailwindcss/vite'

const host = process.env.TAURI_DEV_HOST;

export default defineConfig(async () => ({
  // Ở v4, tailwindcss() đóng vai trò là một Vite plugin chính hiệu
  base: process.env.NODE_ENV === 'production' ? "" : "/",
  plugins: [vue(), tailwindcss()],
  build: {
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            return id.toString().split('node_modules/')[1].split('/')[0].toString();
          }
        }
      }
    }
  },

  assetsInclude: ["**/*.avi"],
  clearScreen: false,
  server: {
    port: 1420,
    strictPort: true,
    host: host || false,
    hmr: host
      ? {
        protocol: "ws",
        host,
        port: 1421,
      }
      : undefined,
    watch: {
      ignored: ["**/src-tauri/**", '**/sql.poseApp.db', '**/sql.poseApp.db-journal'],
    },
  },
}));