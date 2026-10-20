from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)

from urllib.parse import urlsplit

ALLOWED_HOSTS = {
    "51shucheng.net",
    "www.51shucheng.net"
}

class ChapterExtractionError(Exception):
    """Raised when chapter text cannot be extracted."""

class UnsupportedChapterUrlError(ChapterExtractionError):
    """Raised when a URL is outside the supported sources"""

def validate_chapter_url(url: str) -> None:
    try:
        parsed = urlsplit(url)
        hostname = (parsed.hostname or "").lower()
        port = parsed.port

    except ValueError as exc:
        raise UnsupportedChapterUrlError("Invalid chapter URL.") from exc

    if (
        parsed.scheme not in {"http", "https"}
        or hostname not in ALLOWED_HOSTS
        or parsed.username is not None
        or parsed.password is not None
        or (port is not None and port not in {80, 443})
    ):
        raise UnsupportedChapterUrlError(
            "This source is not supported. "
            "Currently, only 51shucheng.net chapter URLs are allowed."
        )

async def extract_chapter_text(url: str) -> str:
    """Open a visible browser, extract chapter text, and close it."""
    
    validate_chapter_url(url)

    async with async_playwright() as playwright:
        browser = None

        try:
            browser = await playwright.chromium.launch(headless=False)
            page = await browser.new_page()

            async def guard_document_navigation(route):
                if route.request.resource_type == "document":
                    try:
                        validate_chapter_url(route.request.url)
                    except UnsupportedChapterUrlError:
                        await route.abort()
                        return

                await route.continue_()

            await page.route("**/*", guard_document_navigation)

            await page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000,
            )

            content = page.locator("#neirong")
            await content.wait_for(
                state="visible",
                timeout=120000,
            )

            text = (await content.inner_text()).strip()

            if len(text) < 200:
                raise ChapterExtractionError("The extracted chapter appears too short.")

            return text

        except ChapterExtractionError:
            raise

        except PlaywrightTimeoutError as exc:
            raise ChapterExtractionError("The chapter did not appear within the time limit.") from exc

        except Exception as exc:
            raise ChapterExtractionError("Unable to load or extract this chapter.") from exc

        finally:
            if browser is not None:
                await browser.close()