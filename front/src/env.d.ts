/// <reference types="vite/client" />

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

interface ImportMetaEnv {
  readonly VITE_BASE_URL: string;
  // добавьте другие переменные, которые используете
}
