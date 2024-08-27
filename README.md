# Static Site Generator (SSG)

## Overview

This project is a simple Static Site Generator (SSG) that converts Markdown files into HTML pages. It reads Markdown files from the `/content` directory, processes them using a template, and outputs the HTML files to the `/public` directory. The generated site can be viewed locally via a built-in Python HTTP server.

## Features

- **Markdown Support**: Converts Markdown syntax to HTML.
  - Headings (`#`, `##`, `###`, etc.)
  - Paragraphs
  - Bold (`**bold**`)
  - Italics (`*italic*`)
  - Links
  - Images
  - Lists (ordered and unordered)
  - Quotes
  - Code blocks
- **Template Integration**: Inserts converted Markdown content into a pre-defined HTML template.
- **Automatic File Handling**: Processes all Markdown files in the `/content` directory and outputs them to `/public`.

## Supported Markdown to HTML Conversion

| **Markdown**               | **HTML**                            |
|----------------------------|-------------------------------------|
| `# Heading 1`              | `<h1>Heading 1</h1>`                |
| `This is a paragraph.`     | `<p>This is a paragraph.</p>`       |
| `**bold**`                 | `<b>bold</b>`                       |
| `*italic*`                 | `<i>italic</i>`                     |
| `[link](https://example)`  | `<a href="https://example">link</a>`|
| `![alt text](image.jpg)`   | `<img src="image.jpg" alt="alt text">`|
| `* Item`                   | `<ul><li>Item</li></ul>`            |
| `1. Item`                  | `<ol><li>Item</li></ol>`            |
| `> Quote`                  | `<blockquote>Quote</blockquote>`    |
| `` `Code` ``               | `<code>Code</code>`                 |

## Data Flow Through the System

1. **Content Directory**: Markdown files are stored in the `/content` directory.
2. **Template File**: An `template.html` file is located in the root of the project.
3. **Static Site Generator**:
    - The generator (Python code in `src/`) reads the Markdown files and the template file.
    - Converts Markdown files into final HTML pages.
    - Writes the HTML files to the `/public` directory.
4. **Serving the Site**:
    - Start the built-in Python HTTP server (separate from the generator) to serve the contents of the `/public` directory.
    - Access the site via `http://localhost:8888` in a web browser.

## How the SSG Works

Most of the work happens in the `src/` directory. Here's an outline of the program's process:

1. **Cleanup**: Delete everything in the `/public` directory.
2. **Copy Assets**: Move static assets (HTML template, images, CSS, etc.) to the `/public` directory.
3. **Generate HTML**: For each Markdown file in the `/content` directory:
    - Open and read the file's contents.
    - Split the content into blocks (e.g., paragraphs, headings, lists).
    - Convert each block into a tree of `HTMLNode` objects. Inline elements like bold text or links are converted as follows:
        - Raw markdown → `TextNode` → `HTMLNode`
    - Combine all `HTMLNode` blocks into a single parent `HTMLNode` for the page.
    - Recursively convert the `HTMLNode` tree to an HTML string using the `to_html()` method, injecting it into the HTML template.
    - Save the complete HTML string to a file in the `/public` directory.

## Running the SSG

1. Run the `main.sh` script:
```
python3 src/main.py
cd public && python3 -m http.server 8888
```
2. If everything goes well, you should be able to see your webpage at `http://localhost:8888` in your browser!

## Prerequisites

- **Python**: Ensure you have Python installed. (Tested with Python 3.x)
- **Bash**: The `main.sh` script is a Bash script, so you'll need a Unix-like environment (Linux, macOS, or WSL on Windows).