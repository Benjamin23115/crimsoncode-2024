<script lang="ts">
	import { fade } from 'svelte/transition';
	export let variant = 'variant-filled-error';
	export let border = 'rounded';
</script>

<aside class={`alert ${variant} ${border}`} transition:fade|local={{ duration: 500 }}>
	<span class="material-symbols-outlined">error</span>
	<div class="alert-message">
		<h3 class="h3">Wrong File Type</h3>
		<span>Please input a proper file type!</span>
	</div>
</aside>

<style lang="postcss">
</style>
