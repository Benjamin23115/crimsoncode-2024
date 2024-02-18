<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { FileDropzone } from '@skeletonlabs/skeleton';
	import Alert from 'abstract/Alert/Alert.svelte';
	const dispatch = createEventDispatcher();

	export let invalidFileInput: boolean;

	let files: FileList;
	let fileExtensionCheck: boolean;

	const onChangeHandler = (e: Event) => {
		fileExtensionCheck = files[0].name.endsWith('pdf');
		if (fileExtensionCheck) {
			// send pdf file to OCR
		} else {
			dispatch('wrongFileInput');
		}
	};
</script>

<div class="container h-full mx-auto flex justify-center items-center flex-col gap-16">
	{#if invalidFileInput}
		<Alert />
	{/if}
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Welcome to Tuff2DBug</h2>
		<FileDropzone name="files" bind:files on:change={onChangeHandler} rounded="rounded">
			<svelte:fragment slot="lead"
				><span class="material-symbols-outlined"> upload_file </span></svelte:fragment
			>
			<svelte:fragment slot="message"
				><strong>Upload a File</strong> or drag and drop</svelte:fragment
			>
			<svelte:fragment slot="meta">PDF only</svelte:fragment>
		</FileDropzone>
	</div>
</div>

<style lang="postcss">
	@keyframes glow {
		0% {
			@apply bg-primary-400/50;
		}
		33% {
			@apply bg-secondary-400/50;
		}
		66% {
			@apply bg-tertiary-400/50;
		}
		100% {
			@apply bg-primary-400/50;
		}
	}
	@keyframes pulse {
		50% {
			transform: scale(1.5);
		}
	}
</style>
