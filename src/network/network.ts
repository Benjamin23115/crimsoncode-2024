export const sendPdf = async (pdfFile: File): Promise<void> => {
	let formData = new FormData();
	formData.append('file', pdfFile);
	console.log('temp', formData);

	// const url = import.meta.env.VITE_URL; // Replace with your server endpoint
	const url = 'http://localhost:5001/submit'; // Replace with your server endpoint

	try {
		const response = await fetch(url, {
			method: 'POST',
			body: formData
		});
		console.log(response);
	} catch (error) {
		console.error('Error with sending Pdf: ', error);
	}
};

export async function pingUrl(url: string): Promise<void> {
	const startTime = performance.now();
	try {
		const response = await fetch(url);
		if (response.ok) {
			const endTime = performance.now();
			const pingTime = endTime - startTime;
			console.log(`Ping to ${url} successful. Time: ${pingTime.toFixed(2)} ms`);
		} else {
			console.error(`Failed to ping ${url}. Status: ${response.status} ${response.statusText}`);
		}
	} catch (error) {
		console.error(`Error pinging ${url}:`, error);
	}
}
