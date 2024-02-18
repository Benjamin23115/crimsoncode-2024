<script lang="ts">
	import { PDFDocument, PDFPage } from 'pdf-lib';
	import { onMount } from 'svelte';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let pdf: Uint8Array;
	let cropStartX: number;
	let cropStartY: number;
	let cropEndX: number;
	let cropEndY: number;
	let cropping: boolean = false;
	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D | null = null;
	let canvasWidth = 600; // Adjust the width as needed
	let canvasHeight = 800; // Adjust the height as needed

	async function cropPage(page: PDFPage): Promise<Uint8Array> {
		// Calculate crop box coordinates
		const minX = Math.min(cropStartX, cropEndX);
		const minY = Math.min(cropStartY, cropEndY);
		const width = Math.abs(cropEndX - cropStartX);
		const height = Math.abs(cropEndY - cropStartY);

		// Crop the page
		page.setCropBox(minX, minY, width, height);

		// Serialize the modified PDF document
		return page.doc.save();
	}

	const startCrop = () => {
		cropping = true;
	};

	const handleMouseDown = (event: MouseEvent) => {
		if (!cropping) {
			cropping = true;
			cropStartX = event.offsetX;
			cropStartY = event.offsetY;
		}
	};

	const handleMouseMove = (event: MouseEvent) => {
		if (cropping && ctx) {
			cropEndX = event.offsetX;
			cropEndY = event.offsetY;
			drawSelectionRect();
		}
	};

	const handleMouseUp = (event: MouseEvent) => {
		if (!cropping) return;
		cropping = false;
		crop();
	};

	const crop = async () => {
		if (!pdf) {
			console.error('PDF file is not provided');
			return;
		}

		try {
			const pdfDoc = await PDFDocument.load(pdf);
			const page = pdfDoc.getPages()[0]; // Get the first page for demonstration

			// Crop the page based on the selected area
			const modifiedPdfBytes = await cropPage(page);

			// Emit an event with the modified PDF bytes
			dispatch('modifiedPdf', { bytes: modifiedPdfBytes });
		} catch (error) {
			console.error('Error processing PDF:', error);
		}
	};

	const drawSelectionRect = () => {
		if (!ctx) return;

		const width = cropEndX - cropStartX;
		const height = cropEndY - cropStartY;

		ctx.clearRect(0, 0, canvas.width, canvas.height);
		ctx.strokeStyle = 'red';
		ctx.strokeRect(cropStartX, cropStartY, width, height);
	};

	onMount(() => {
		if (canvas) {
			ctx = canvas.getContext('2d')!;
			crop();
		}
	});
</script>

<div class="container h-full mx-auto flex justify-center items-center flex-col">
	<canvas
		bind:this={canvas}
		width={canvasWidth}
		height={canvasHeight}
		on:mousedown={handleMouseDown}
		on:mousemove={handleMouseMove}
		on:mouseup={handleMouseUp}
	/>

	<button on:click={startCrop}>Start Crop</button>
</div>

<style lang="postcss">
	.crop-selection {
		position: absolute;
		border: 2px solid red;
		pointer-events: none;
	}
</style>
