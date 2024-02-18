<script lang="ts">
	import { FileDropzone } from '@skeletonlabs/skeleton';
	import Alert from 'abstract/Alert/Alert.svelte';
	import PdfViewer from 'routes/PdfViewer.svelte';
	import { ALERT_WAIT_TIME, APPLICATION_NAME } from 'constants/constants';
	import { readFileAsUint8Array } from 'models/models';
	import { sendPdf, pingUrl } from 'network/network';

	let invalidFileInput: boolean = false;
	let validFileInput: boolean = false;
	let fileExtensionCheck: boolean = false;
	let pdfHasBeenSent: boolean = false;
	let fileAsUInt8Array: Uint8Array;
	let files: FileList;
	let inputFileAsFile: File;

	const onChangeHandler = async (e: Event) => {
		let file = files[0];
		fileExtensionCheck = file.name.endsWith('.pdf');
		if (fileExtensionCheck) {
			validFileInput = true;
			setTimeout(() => {
				validFileInput = false;
			}, ALERT_WAIT_TIME);
			if (file) {
				fileAsUInt8Array = await readFileAsUint8Array(files[0]);
				const blob = new Blob([fileAsUInt8Array]);
				inputFileAsFile = new File([blob], file.name, { lastModified: file.lastModified });
				console.log('temp', inputFileAsFile);
				sendPdf(inputFileAsFile);
				pdfHasBeenSent = true;
			} else {
				invalidFileInput = true;
				setTimeout(() => {
					invalidFileInput = false;
				}, ALERT_WAIT_TIME);
			}
		}
	};
	$: pingUrl('http://localhost:5000/');
</script>

<div class="container h-full mx-auto flex justify-center items-center flex-col gap-8">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Welcome to {APPLICATION_NAME}</h2>
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
	{#if !validFileInput && pdfHasBeenSent}
		<audio controls>
			<!-- add wav src file here -->
			<source src={audioBlob} type="audio/wav" />
			Your browser does not support the audio element.
		</audio>
	{/if}
</div>

<style lang="postcss">
</style>
