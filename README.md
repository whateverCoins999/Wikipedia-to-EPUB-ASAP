# Wikipedia-to-EPUB-ASAP
Converts a long list of Wikipedia pages into properly formatted EPUBs.


# Introduction
A few days ago, I was looking for a fast, simple, and efficient way to convert Wikipedia pages into EPUB files. The problem was that other solutions I found were either too slow or produced malformed EPUBs (checked with [EPUB Validator](https://draft2digital.com/book/epubcheck/upload)). A malformed EPUB can still be read, but Google Play Books is very picky about this. In fact, even a single imperfection in the EPUB causes a "processing..." failure in Google Play Books. So, I decided to create my own solution.

The EPUBs created by the app have a white cover with the page title written in black. The author is automatically set to "Wikipedia," making it easy to distinguish regular books from Wikipedia pages. Additionally, it automatically detects the chapters of the page, so they are displayed correctly on Google Play Books or any other reader.

# Installation
## Windows
Just download the `.exe` file and run it. no Python or installation required.

## Other Platforms
Install Python and the dependencies
`pip install pip install pillow wikipedia-api ebooklib` 

then run the script.

# Usage
It's simple: just load a bunch of Wikipedia links into the `wiki.txt` file and run the program. The `.exe` file and `wiki.txt` must be in the same directory. Wait until the process is finished. 

The `wiki.txt` file in the repo contains some example links. Once the EPUBs are downloaded, the chapters are already automatically defined.

If you have any questions, feel free to contact me on Discord @rrospega

Have fun and enjoy your reading!
