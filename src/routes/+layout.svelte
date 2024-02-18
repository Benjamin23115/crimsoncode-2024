<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { AppShell } from '@skeletonlabs/skeleton';
	import '../app.postcss';
	import { APPLICATION_NAME } from 'constants/constants';
	import Header from 'abstract/Header/Header.svelte';
	import Page from './+page.svelte';

	let appTheme: 'light' | 'dark' = 'dark';
	let favicon = writable('favicon-dark.png');
	let hasComponentMounted: boolean = false;

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
		document.title = APPLICATION_NAME;
		changeFavicon();
		hasComponentMounted = true;
	});
</script>

<AppShell>
	<svelte:fragment slot="header">
		<Header on:appThemeChange={handleAppThemeChange} {appTheme} />
	</svelte:fragment>
	<svelte:fragment>
		<Page />
	</svelte:fragment>
</AppShell>

<style lang="postcss">
</style>
