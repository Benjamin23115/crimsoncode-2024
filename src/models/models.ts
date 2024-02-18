export const readFileAsArrayBuffer = (file: File): Promise<ArrayBuffer> => {
	return new Promise((resolve, reject) => {
		const reader = new FileReader();
		reader.onload = () => {
			if (reader.result instanceof ArrayBuffer) {
				resolve(reader.result);
			} else {
				reject(new Error('Failed to read file as ArrayBuffer'));
			}
		};
		reader.onerror = reject;
		reader.readAsArrayBuffer(file);
	});
};

export const readFileAsUint8Array = (file: File): Promise<Uint8Array> => {
	return new Promise((resolve, reject) => {
		const reader = new FileReader();
		reader.onload = () => {
			if (reader.result instanceof ArrayBuffer) {
				const uint8Array = new Uint8Array(reader.result);
				resolve(uint8Array);
			} else {
				reject(new Error('Failed to read file as ArrayBuffer'));
			}
		};
		reader.onerror = reject;
		reader.readAsArrayBuffer(file);
	});
};
