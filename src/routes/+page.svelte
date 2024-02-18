<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { FileDropzone } from '@skeletonlabs/skeleton';
	import Alert from 'abstract/Alert/Alert.svelte';
	import PdfViewer from "routes/PdfViewer/PdfViewer.svelte"
	import { ALERT_WAIT_TIME } from 'constants/constants';

	let invalidFileInput: boolean = false;
	let validFileInput: boolean = false;

	let files: FileList;
	let fileExtensionCheck: boolean;

	const onChangeHandler = (e: Event) => {
		fileExtensionCheck = files[0].name.endsWith('.pdf');
		if (fileExtensionCheck) {
			validFileInput = true;
			setTimeout(() => {
				validFileInput = false;
			}, ALERT_WAIT_TIME);
			// send pdf file to OCR
		} else {
			invalidFileInput = true;
			setTimeout(() => {
				invalidFileInput = false;
			}, ALERT_WAIT_TIME);
		}
	};
</script>

<div class="container h-full mx-auto flex justify-center items-center flex-col gap-8">
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
	{#if invalidFileInput}
		<Alert />
	{/if}
	{#if validFileInput}
		<Alert
			title={'Success'}
			description={'The uploaded file is now being processed'}
			variant={'variant-filled-success'}
			icon={'done'}
		/>
	{/if}
</div>

<style lang="postcss">
</style>
