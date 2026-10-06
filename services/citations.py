import re


def extract_citations(text: str):

    pattern = r"https?://[^\s\]\)>]+"

    citations = re.findall(
        pattern,
        text
    )

    unique_citations = []

    for citation in citations:

        citation = citation.rstrip(
            ".,;:"
        )

        if citation not in unique_citations:

            unique_citations.append(
                citation
            )

    return unique_citations