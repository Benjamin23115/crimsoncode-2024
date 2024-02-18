import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import path from 'path';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	extensions: ['.svelte'],
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: [vitePreprocess()],

	kit: {
		// Pass the adapter configuration directly to the adapter property
		adapter: adapter({
			out: 'build'
		}),
		files: {
			assets: path.resolve('./public')
		},
		alias: {
			constants: 'src/constants',
			routes: 'src/routes',
			abstract: 'src/abstract',
			models: 'src/models',
			network: 'src/network'
		}
	}
};
export default config;
