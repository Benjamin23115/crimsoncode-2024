import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
const source = path.join('./node_modules/@pdftron/pdfjs-express/public/');
const destination = path.join('./src/pdf-js'); // Adjust if needed

async function copyFiles() {
	try {
		// Check if destination directory exists
		if (!(await fs.existsSync(destination))) {
			await fs.mkdirSync(destination, { recursive: true });
		}

		// Use system-specific command based on platform
		const command = getCommandForPlatform();
		await execSync(command, { stdio: 'inherit' });

		console.log(`Copied files from ${source} to ${destination}`);
	} catch (error) {
		console.error(`Error copying files: ${error.message}`);
	}
}

function getCommandForPlatform() {
    if (process.platform === 'win32') {
        return `xcopy "${source}" "${destination}" /E /Y`;
    } else if (process.platform === 'darwin') {
        return `cp -r "${source}" "${destination}"`;
    } else {
        return `cp -r "${source}" "${destination}"`;
    }
}


copyFiles();
