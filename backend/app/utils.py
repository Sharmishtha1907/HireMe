from pathlib import Path

from pypdf import PdfReader



def extract_text(self, file_path: str) -> str:

    path = Path(file_path)

    if path.suffix.lower() != ".pdf":
        raise ValueError(
            "Only PDF resumes are supported."
        )

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    result = "\n".join(pages).strip()

    if not result:
        raise ValueError(
            "Could not extract text from resume."
        )

    return result