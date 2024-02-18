<script lang="ts">
	import { onMount } from 'svelte';
	import { AppShell } from '@skeletonlabs/skeleton';
	import '../app.postcss';
	import { ERROR_WAIT_TIME, APPLICATION_NAME } from 'constants/constants';
	import Header from 'abstract/Header/Header.svelte';
	import Page from './+page.svelte';

	let invalidFileInput: boolean = false;
	let appTheme: 'light' | 'dark' = 'dark';

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
	};

	onMount(() => {
		document.title = APPLICATION_NAME;
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
