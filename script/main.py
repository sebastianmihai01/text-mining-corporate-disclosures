import os
import json
import re
from collections import defaultdict
import pymupdf


def load_taxonomy(taxonomy_path):
    """Load ESG taxonomy from JSON file"""
    with open(taxonomy_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_text_from_pdf(pdf_path):
    """Extract text content from PDF file"""
    try:
        doc = pymupdf.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.lower()  # Convert to lowercase for case-insensitive matching
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""


def count_term_frequencies(text, terms):
    """Count frequencies of terms in text with exact and partial matching"""
    frequencies = {}

    for term in terms:
        # Exact match (case-insensitive)
        exact_pattern = r"\b" + re.escape(term.lower()) + r"\b"
        exact_count = len(re.findall(exact_pattern, text))

        # Partial match (case-insensitive)
        partial_pattern = re.escape(term.lower())
        partial_count = len(re.findall(partial_pattern, text))

        frequencies[term] = {
            "exact_matches": exact_count,
            "partial_matches": partial_count,
            "total_matches": partial_count,  # Total includes both exact and partial
        }

    return frequencies


def process_esg_taxonomy(taxonomy, text):
    """Process ESG taxonomy and count term frequencies"""
    results = {"Environmental": {}, "Social": {}, "Governance": {}}

    for esg_category, categories in taxonomy.items():
        for category, subcategories in categories.items():
            results[esg_category][category] = {}

            for subcategory, terms in subcategories.items():
                if isinstance(terms, list):
                    # Direct list of terms
                    frequencies = count_term_frequencies(text, terms)
                    results[esg_category][category][subcategory] = frequencies
                elif isinstance(terms, dict):
                    # Nested structure
                    results[esg_category][category][subcategory] = {}
                    for nested_subcategory, nested_terms in terms.items():
                        if isinstance(nested_terms, list):
                            frequencies = count_term_frequencies(text, nested_terms)
                            results[esg_category][category][subcategory][
                                nested_subcategory
                            ] = frequencies

    return results


def print_results(file_name, results):
    """Print formatted results for a PDF file"""
    print(f"\n{'='*60}")
    print(f"Results for: {file_name}")
    print(f"{'='*60}")

    for esg_category, categories in results.items():
        print(f"\n{esg_category.upper()}:")
        print("-" * 40)

        for category, subcategories in categories.items():
            print(f"\n  {category}:")

            for subcategory, data in subcategories.items():
                if isinstance(data, dict) and "exact_matches" in data:
                    # Direct term results
                    if data["total_matches"] > 0:
                        print(
                            f"    {subcategory}: {data['total_matches']} matches "
                            f"({data['exact_matches']} exact, {data['partial_matches']} partial)"
                        )
                elif isinstance(data, dict):
                    # Nested results
                    print(f"    {subcategory}:")
                    for nested_subcategory, nested_data in data.items():
                        if nested_data["total_matches"] > 0:
                            print(
                                f"      {nested_subcategory}: {nested_data['total_matches']} matches "
                                f"({nested_data['exact_matches']} exact, {nested_data['partial_matches']} partial)"
                            )


def main():
    # Load taxonomy
    taxonomy_path = "dictionary/taxonomy.json"
    taxonomy = load_taxonomy(taxonomy_path)

    # Process each PDF in the documents folder
    documents_folder = "documents"

    if not os.path.exists(documents_folder):
        print(f"Documents folder '{documents_folder}' not found!")
        return

    pdf_files = [f for f in os.listdir(documents_folder) if f.endswith(".pdf")]

    if not pdf_files:
        print(f"No PDF files found in '{documents_folder}' folder!")
        return

    print(f"Found {len(pdf_files)} PDF file(s) to process...")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(documents_folder, pdf_file)
        print(f"\nProcessing: {pdf_file}")

        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)

        if not text:
            print(f"  No text extracted from {pdf_file}")
            continue

        # Process ESG taxonomy and count frequencies
        results = process_esg_taxonomy(taxonomy, text)

        # Print results
        print_results(pdf_file, results)


if __name__ == "__main__":
    main()
