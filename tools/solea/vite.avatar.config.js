import { defineConfig } from 'vite';

export default defineConfig({
  base: './',
  publicDir: false,
  build: {
    target: 'es2022',
    outDir: 'dist-component',
    emptyOutDir: true,
    lib: {
      entry: 'src/sol-avatar.js',
      formats: ['es'],
      fileName: () => 'sol-avatar.js'
    },
    rollupOptions: {
      output: { inlineDynamicImports: true }
    }
  }
});
