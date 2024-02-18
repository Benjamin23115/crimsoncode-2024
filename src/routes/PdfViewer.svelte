<script lang="ts">
	import * as pdfjsLib from 'pdfjs-dist';
	import { onMount } from 'svelte';
	import { PDF_JS_WORKER } from 'constants/constants';

	pdfjsLib.GlobalWorkerOptions.workerSrc = PDF_JS_WORKER;

	export let pdf: Uint8Array;
	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D | null = null;
	let cropping: boolean = false;
	let startX: number;
	let startY: number;
	let endX: number;
	let endY: number;

	async function renderPDF() {
		if (!pdf || !canvas || !ctx) {
			console.error('PDF, canvas, or context not available');
			return;
		}

		try {
			const loadingTask = pdfjsLib.getDocument({ data: pdf });
			const pdfDoc = await loadingTask.promise;

			for (let i = 1; i <= pdfDoc.numPages; i++) {
				const page = await pdfDoc.getPage(i);
				const { width, height } = page.getViewport({ scale: 1 });

				canvas.width = width;
				canvas.height = height;

				await page.render({
					canvasContext: ctx,
					viewport: page.getViewport({ scale: 1 })
				}).promise;
			}
		} catch (error) {
			console.error('Error rendering PDF:', error);
		}
	}

	function handleMouseDown(event: MouseEvent) {
		startX = event.offsetX;
		startY = event.offsetY;
		cropping = true;
	}

	function handleMouseMove(event: MouseEvent) {
		if (!cropping || !ctx) return;

		endX = event.offsetX;
		endY = event.offsetY;

		drawSelectionRect();
	}

	function handleMouseUp() {
		if (cropping) {
			cropping = false;
			crop();
		}
	}

	function drawSelectionRect() {
		if (!ctx) return;

		const width = endX - startX;
		const height = endY - startY;

		ctx.clearRect(0, 0, canvas.width, canvas.height);
		ctx.strokeStyle = 'red';
		ctx.strokeRect(startX, startY, width, height);
	}

	async function crop() {
		if (!pdf || !canvas || !ctx) {
			console.error('PDF, canvas, or context not available');
			return;
		}

		try {
			const loadingTask = pdfjsLib.getDocument({ data: pdf });
			const pdfDoc = await loadingTask.promise;

			for (let i = 1; i <= pdfDoc.numPages; i++) {
				const page = await pdfDoc.getPage(i);

				// Crop the page
				const minX = Math.min(startX, endX);
				const minY = Math.min(startY, endY);
				const width = Math.abs(endX - startX);
				const height = Math.abs(endY - startY);
				page.setCropBox(minX, minY, width, height);

				// Clear canvas and re-render cropped page
				ctx.clearRect(0, 0, canvas.width, canvas.height);
				await renderPDF();
			}
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
