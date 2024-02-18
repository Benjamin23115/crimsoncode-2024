<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { AppBar, LightSwitch } from '@skeletonlabs/skeleton';
	import { APPLICATION_NAME } from 'constants/constants';

	export let appTheme: 'light' | 'dark' = 'dark';
	const dispatch = createEventDispatcher();

	const appThemeChange = () => {
		dispatch('appThemeChange');
	};
	const handleAppReload = () => {
		window.location.reload();
	};
</script>

<AppBar>
	<svelte:fragment slot="lead">
		<button on:click={handleAppReload}>
			<img
				alt="app-logo"
				src={appTheme === 'dark' ? './favicon-dark.png' : './favicon-light.png'}
			/>
		</button>

		<div class="divider" />
		<strong class="text-xl uppercase">{APPLICATION_NAME}</strong>
	</svelte:fragment>
	<svelte:fragment slot="trail">
		<LightSwitch rounded="rounded-2xl" height="h-8" width="w-16" on:click={appThemeChange} />
	</svelte:fragment>
</AppBar>

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
