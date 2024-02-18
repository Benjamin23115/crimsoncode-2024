<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { AppShell } from '@skeletonlabs/skeleton';
	import '../app.postcss';
	import { ERROR_WAIT_TIME, APPLICATION_NAME } from 'constants/constants';
	import Header from 'abstract/Header/Header.svelte';
	import Page from './+page.svelte';

	let invalidFileInput: boolean = false;
	let appTheme: 'light' | 'dark' = 'dark';
	let favicon = writable('favicon-dark.png');

	const changeFavicon = () => {
		if (appTheme === 'light') {
			favicon.set('favicon-light.png');
		} else {
			favicon.set('favicon-dark.png');
		}
	};

	const handleWrongFileInput = () => {
		invalidFileInput = true;
		setTimeout(() => {
			invalidFileInput = false;
		}, ERROR_WAIT_TIME);
	};
	const handleAppThemeChange = () => {
		if (appTheme === 'light') {
			appTheme = 'dark';
		} else {
			appTheme = 'light';
		}
		changeFavicon(); // Call changeFavicon when appTheme changes
	};

	// Watch for changes in the favicon and update the document's favicon
	$: favicon = favicon; // This line triggers reactivity whenever $favicon changes
	favicon.subscribe((newFavicon) => {
		const faviconLink = document.querySelector('link[rel="icon"]');
		if (faviconLink) {
			faviconLink.setAttribute('href', newFavicon);
		}
	});

	onMount(() => {
		document.title = APPLICATION_NAME;
		changeFavicon();
	});
</script>

<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<Header on:appThemeChange={handleAppThemeChange} {appTheme} />
	</svelte:fragment>
	<Page on:wrongFileInput={handleWrongFileInput} {invalidFileInput} />
</AppShell>

<style lang="postcss">
</style>
