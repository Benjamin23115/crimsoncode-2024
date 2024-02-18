<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { AppShell } from '@skeletonlabs/skeleton';
	import '../app.postcss';
	import Header from 'abstract/Header/Header.svelte';
	import Page from './+page.svelte';

	let appTheme: 'light' | 'dark' = 'dark';
	let favicon = writable('favicon-dark.png');
	let hasComponentMounted: boolean = false;
	let appName = import.meta.env.VITE_APPLICATION_NAME;


	const changeFavicon = () => {
		if (appTheme === 'light') {
			favicon.set('favicon-light.png');
		} else {
			favicon.set('favicon-dark.png');
		}
	};

	const handleAppThemeChange = () => {
		if (appTheme === 'light') {
			appTheme = 'dark';
		} else {
			appTheme = 'light';
		}
		changeFavicon(); // Call changeFavicon when appTheme changes
	};

	$: favicon = favicon; // This line triggers reactivity whenever favicon changes
	$: if (hasComponentMounted) {
		favicon.subscribe((newFavicon) => {
			const faviconLink = document?.querySelector('link[rel="icon"]');
			if (faviconLink) {
				faviconLink.setAttribute('href', newFavicon);
			}
		});
	}

	onMount(() => {
		document.title = appName;
		changeFavicon();
		hasComponentMounted = true;
	});
</script>

<AppShell>
	<svelte:fragment slot="header">
		<Header on:appThemeChange={handleAppThemeChange} {appTheme} {appName}/>
	</svelte:fragment>
	<svelte:fragment>
		<Page {appName}/>
	</svelte:fragment>
</AppShell>

<style lang="postcss">
</style>
