import type {UserConfig} from 'vite'

export default {
    
    server: {
        host: "0.0.0.0",
    },
    build: {
        outDir: "build/dist",
        rollupOptions: {
            input: "build/html/index.html",
        },
    }
}satisfies UserConfig
