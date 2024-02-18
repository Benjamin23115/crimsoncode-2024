<script lang="ts">
	import { PDFDocument } from 'pdf-lib';
	import { onMount } from 'svelte';

	export let pdf: Uint8Array;
	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D | null = null;
	let cropStartX: number;
	let cropStartY: number;
	let cropEndX: number;
	let cropEndY: number;
	let cropping: boolean = false;

	async function renderPDF() {
		if (!pdf || !canvas) {
			console.error('PDF or canvas not available');
			return;
		}

		try {
			const pdfDoc = await PDFDocument.load(pdf);
			const page = await pdfDoc.getPage(0);
			const { width, height } = page.getSize();

			// Set the canvas dimensions
			canvas.width = width;
			canvas.height = height;

			// Render the PDF page onto the canvas
			const renderContext = {
				canvasContext: ctx!,
				viewport: page.viewport // Use the existing viewport property
			};
			await page.render(renderContext).promise;
		} catch (error) {
			console.error('Error rendering PDF:', error);
		}
	}

	async function cropPage(page) {
		if (!cropping) return;

		// Calculate crop box coordinates
		const minX = Math.min(cropStartX, cropEndX);
		const minY = Math.min(cropStartY, cropEndY);
		const width = Math.abs(cropEndX - cropStartX);
		const height = Math.abs(cropEndY - cropStartY);

		// Set the crop box on the page
		page.setCropBox(minX, minY, width, height);
	}

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

	const handleMouseUp = () => {
		if (cropping) {
			cropping = false;
			crop();
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

	async function crop() {
		if (!pdf || !canvas) {
			console.error('PDF or canvas not available');
			return;
		}

		try {
			const pdfDoc = await PDFDocument.load(pdf);
			const page = await pdfDoc.getPage(0); // Get the first page

			// Crop the page based on the selected area
			await cropPage(page);

			// Render the cropped PDF page onto the canvas
			await renderPDF();
		} catch (error) {
			console.error('Error cropping PDF:', error);
		}
	}

	onMount(async () => {
		if (!canvas) return;
		ctx = canvas.getContext('2d');
		await renderPDF();
	});
</script>

<div>
	<canvas
		bind:this={canvas}
		on:mousedown={handleMouseDown}
		on:mousemove={handleMouseMove}
		on:mouseup={handleMouseUp}
	></canvas>
</div>

<style lang="postcss">
	canvas {
		border: 1px solid #000;
	}
</style>
