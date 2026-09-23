# Katrin Merfeld — research folio

A responsive, interactive research folio for Dr. Katrin Merfeld. The site presents her work as chapters in a book, with an index, page-like transitions, and a print-friendly layout. It uses plain HTML, CSS, and a small amount of JavaScript, so there is no build step or dependency installation. It works directly on GitHub Pages and is easy to fork.

## Update the site

1. Edit the chapter sections in `index.html` to change the text, publication links, courses, and projects. Each section has a descriptive ID such as `research` or `teaching`.
2. Replace the two photographs in `assets/` while keeping their filenames, or update the image paths in `index.html`.
3. Edit `styles.css` to change the layout or colours. The Utrecht-inspired yellow is defined as `--yellow` near the top.
4. Commit and push to the default branch. GitHub Pages will publish the updated files.

The site intentionally uses a small yellow accent that alludes to Utrecht University. It does not use the university logo or present itself as an official university website. Chapter transitions respect reduced-motion preferences, and the content remains readable when JavaScript is unavailable.

## CV and publications

The site offers one [CV and publications PDF](assets/Katrin-Merfeld-CV-and-Publications.pdf) from the About and Publications chapters. It combines the supplied CV and publication record, updates the appointment and journal articles against Utrecht University's staff pages, includes her [2026 British Academy report](https://www.thebritishacademy.ac.uk/publications/integration-financing-and-just-transition-for-urban-sustainability/), and omits private home and mobile contact details. Please review the record with Katrin before using it for formal applications.

To update the PDF, edit the CV and publication data in `scripts/build_cv.py` and the conference list in `cv/conferences.txt`. Install ReportLab with `python -m pip install reportlab`, then run `python scripts/build_cv.py` from the repository root. Commit the rebuilt PDF with the source changes; GitHub Pages serves the PDF directly from `assets/`.

## Design reference

The book concept was developed after reviewing the MIT-licensed [Creative Personal Portfolio Website](https://github.com/trananhtuat/creative-portfolio-website) and the [Sketchbook](https://github.com/MengTo/sketchbook) experiment. This folio's layout, styling, interaction code, and content were written specifically for Katrin; no third-party photographs or copied template files are included.

## Publish a fork on GitHub Pages

Fork this repository, then open **Settings → Pages** in your fork. Under **Build and deployment**, choose **Deploy from a branch**, select your default branch and `/ (root)`, and save. GitHub will display the live URL on that page. If you rename the repository, GitHub Pages will use the new repository name in the URL.

## Content sources

Content was checked in September 2026 against the [Utrecht University staff profile](https://www.uu.nl/staff/KMerfeld), the [Utrecht University publications page](https://www.uu.nl/staff/KMerfeld/Publications), the [Utrecht University Research Portal](https://research-portal.uu.nl/en/persons/katrin-merfeld/), the [Business & Social Impact programme](https://www.uu.nl/en/masters/business-and-social-impact), and the public [NATURESCAPES](https://www.naturescapes-project.com/) and [ClimEx-PE](https://climexpe.elte.hu/) project sites. The original supplied documents remain local because the source CV contains private contact details; the new public CV includes professional contact details only. The Utrecht profile and research portal remain the live sources for future updates.

Photographs were supplied for this site. Their reuse rights are reserved by their respective owner; please do not reuse them outside this personal site without permission.

## Local preview

Open `index.html` in a web browser. No server is required.
