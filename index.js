const { DownloaderHelper } = require("node-downloader-helper");
const fs = require("fs");
const puppeteer = require("puppeteer");

let completeLinkArray = [];

( async () => {
	let link = process.argv[2];
	const browser = await puppeteer.launch();
	const page = await browser.newPage();
	// Try catch for argument
	await page.goto(link);
	await page.waitForSelector("title");
	const folderName = await page.title();
	console.log(`The page ${folderName} was loaded!`);
	
	if (!fs.existsSync(folderName)) {
		fs.mkdirSync(folderName);
	}

	let format = process.argv[3];
	const tableSongList = await page.evaluate( () => {
		const table = document.querySelector("#songlist");
		let trackArray = [];
		// to avoid the header and - to avoid the footer
		for (let i=1; i<table.rows.length-1; i++) {
			// Need to use the last element because multi cds album can move the first usable link
			let link = "https://downloads.khinsider.com" + table.rows[i].cells[table.rows[i].cells.length-1].childNodes[0].getAttribute("href");
			trackArray.push(link);
		}
		return trackArray;
	});
	
	await page.close();
	
	await console.log("Fetching all links for the download");

	for await (element of tableSongList) {
		const tab = await browser.newPage();
		await tab.goto(element);
		const linkArray = await tab.evaluate( (format) => {
			let linkArray = [];
			let linkArrayTemp = document.querySelectorAll(".songDownloadLink");
			for (linkElement of linkArrayTemp) {
				link = linkElement.parentElement.href;
				if (format != undefined && link.split(".")[link.split(".").length-1] == format)
					linkArray.push(decodeURI(link));
			}
			return linkArray;
		}, format);
		
		await tab.close();

		for (element of linkArray)
			completeLinkArray.push(element);
	}
	await browser.close();


	for await (element of completeLinkArray)
	downloadFile(element, folderName);
})();


function downloadFile(link, folderName) {
	// Last part of the URI to get the proper name without some encoding artefacts.
	let properName = link.split("/")[link.split("/").length-1];
	const dl = new DownloaderHelper(link, folderName, {fileName: properName});

	dl.on("download", () => {
		console.log("Downloading file", properName);
	});

	dl.on("progress", () => {
		process.stdout.write("Progress : " + Math.floor(dl.getStats().progress) + "%");
		process.stdout.cursorTo(0);
	});
	
	dl.on("end", () => console.log("Download Completed"));
	
	dl.start();
}