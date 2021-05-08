# KH Insider Bot

## Description

This project is a simple downloader in NodeJS, as a side project for using the [Pupeteer](https://pptr.dev) library and the [node-downloader-helper](https://www.npmjs.com/package/node-downloader-helper) package, respectively for accessing the various link and download each files.

It's very rough on the edges, the pupeteer library could be switched with a simple HTML parser, I however tried to keep the memory usage in its minimum. 

This project isn't to disminished the khinsider project, the amount of work for preserving so much soundtrack is massive. It was a simple project to understand the pupeteer library. Go donate to his [website](https://downloads.khinsider.com/forums/index.php?account/upgrades).


## Dependencies

- npm
- chromium (if you want to use your own version and specify it on the puppeteer.launch() method).


## Installation

```sh
npm install

# If you have some chromium missing issues, try to launch the specific pupeteer script with the command :
node .\node_modules\puppeteer\install.js
```


## Usage 

For using the program you have to specify the album page link on khinsider and specify the format you want to use. This program won't convert the songs for you, you have to specify one format available for this specific album. If the format you use doesn't exist for this album the program will simply not download any files.

```sh
npm start --link="link/the/album/age" --format="mp3 or any other available"
```

The downloaded files will be stored into a specific folder for each album.


## Issues

- This software cannot be bundled with [pkg](https://www.npmjs.com/package/pkg) because of the nature of pupeteer. The use of the page.evaluate function creates problems as seen in this [topic](https://github.com/vercel/pkg/issues/204). The chromium instances was another problem, trying to implements some simple downloader for each OS, I couldn't get it to work. If I find a way I'll try to pass some executables to be easier than using the original source code.
- There isn't any try catch for easier readilibity for the user. However if following the [Usage](#Usage) correctly you won't have any problems.
- The progress bars for each downloads is a simple percentage that can be tedious because of the multithreading download process.
- A GUI could be neat, it could be a cool idea for a future update.