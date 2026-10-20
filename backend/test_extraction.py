
import asyncio
from app.services.extraction_service import extract_chapter_text, ChapterExtractionError


async def main():
    url = input("Paste a chapter URL: ").strip()

    try:
        text = await extract_chapter_text(url)

        print("\n--- Extracted chapter text ---\n")
        print(text[:1500])
        print("\nTotal characters:", len(text))

    except ChapterExtractionError as exc:
        print(f"\nExtraction failed: {exc}")

if __name__ == "__main__":
    asyncio.run(main())