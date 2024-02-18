import fetch from 'node-fetch';

export async function GET(request: any) {
	try {
		// Extract query parameters from the request
		const queryParams = new URLSearchParams(request.query).toString();

		// Make a GET request to backend server with query parameters
		const response = await fetch(`http://localhost:5000/status?${queryParams}`);

		if (!response.ok) {
			throw new Error('Failed to fetch data from backend');
		}

		const data = await response.json();

		return {
			status: 200,
			body: {
				data
			}
		};
	} catch (error) {
		console.error('Error:', error);
		return {
			status: 500,
			body: {
				error: 'Internal Server Error'
			}
		};
	}
}

export async function POST(request: any) {
	try {
		// Extract request body
		const formData = new FormData();

		formData.append('file', request.files.file[0].buffer);

		// Make a POST request to backend server
		const response = await fetch('http://localhost:5000/submit', {
			method: 'POST',
			body: formData
		});

		if (!response.ok) {
			throw new Error('Failed to fetch data from backend');
		}

		return response;
	} catch (error) {
		console.error('Error:', error);
		throw new Error('Failed to fetch data from backend');
	}
}
