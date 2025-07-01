# Description

Text mining tool made to analyse the semantics of corporate disclosures.

The script is fed a taxonomy dictionary, which is the direct result of a literature review on the topic of greenwashing, corporate disclosures, the discrepancy between sustainability definitions and their associated metrics.

# Organizational

The script is part of my MSc thesis, which focuses on analysing sustainability reporting through the means of this script.

Contact: i.mihai@student.utwente.nl \
Faculty: BMS, part of the University of Twente \
Date: June 2025

# Context

Multiple definitions of ESG have been found across the literature. \
<img width="508" alt="Screenshot 2025-06-20 at 14 12 28" src="https://github.com/user-attachments/assets/65ae1249-7b1c-42d6-aedb-44651691d132" />

Based on these terms, the taxonomy is created. The result of this is found under the directory "taxonomy/"

# Algorithm

The script is making use of the library PyMuPDF, which is a "high-performance Python library for data extraction, analysis, conversion & manipulation of PDF (and other) documents." \
This library is open-source and found at https://github.com/pymupdf/PyMuPDF

# How to run

Run the following commands in the main directory of this project.

**Step 1:** python3 -m venv text-mining-script (or just "python") \
**Step 2:** . text-mining-script/bin/activate \
**Step 3:** python -m pip install --upgrade pip \

# Result
<img width="565" alt="Screenshot 2025-07-01 at 23 36 55" src="https://github.com/user-attachments/assets/cb30fd6d-3712-49e8-9134-4e417d1712cb" />
