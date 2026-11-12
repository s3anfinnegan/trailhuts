/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_PROTOMAPS_API_KEY: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
