<script lang="ts">
	import { fade } from 'svelte/transition';
	export let variant = 'variant-filled-error';
	export let border = 'rounded';
	export let title = 'Wrong File Type';
	export let description = 'Please input a proper file type!';
	export let icon = 'error';
</script>

<aside class={`alert ${variant} ${border} w-4/12`} transition:fade|local={{ duration: 500 }}>
	<span class="material-symbols-outlined">{icon}</span>
	<div class="alert-message">
		<h3 class="h3">{title}</h3>
		<span>{description}</span>
	</div>
</aside>

<style lang="postcss">
</style>
