import type {UserConfig} from 'vite'

export default {
    server: {
        host: "0.0.0.0",
    },
    build: {
        outDir: "build/dist",
        rollupOptions: {
            input: {
                index:"build/html/index.html",
                404: "404.html"
            },
        },
    }
}satisfies UserConfig
