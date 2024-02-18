<script lang="ts">
	import { onMount } from 'svelte';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
	import { LightSwitch } from '@skeletonlabs/skeleton';
	import '../app.postcss';
	import { ERROR_WAIT_TIME } from 'constants/constants';
	import Page from './+page.svelte';

	let applicationName = import.meta.env.VITE_APPLICATION_NAME;
	let invalidFileInput: boolean = false;
	const handleWrongFileInput = () => {
		invalidFileInput = true;
		setTimeout(() => {
			invalidFileInput = false;
		}, ERROR_WAIT_TIME);
	};

	onMount(() => {
		document.title = applicationName;
	});
</script>

<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar>
			<svelte:fragment slot="lead">
				<img alt="app-logo" src="./favicon.png" />
				<div class="divider" />
				<strong class="text-xl uppercase">{applicationName}</strong>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<LightSwitch />
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<Page on:wrongFileInput={handleWrongFileInput} {invalidFileInput} />
</AppShell>

<style lang="postcss">
	img {
		max-height: 50px;
		max-width: 50px;
	}
	.divider {
		width: 100%;
		height: 1px;
		margin: 20px 5px;
	}
</style>
