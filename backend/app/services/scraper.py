from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def get_chapter_text(url):
    print(f"Deploying a real browser to fetch: {url}")
    
    with sync_playwright() as p:
        # 1. Must be False so you can see and solve the CAPTCHA
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        
        print("Navigating... You have 15 seconds to solve the Cloudflare check!")
        
        # 2. We remove the strict 'networkidle' and timeout here. 
        # We just tell it to load the URL and immediately move to the next line of code.
        try:
            page.goto(url)
        except Exception as e:
            pass # Ignore initial load errors caused by Cloudflare redirects
            
        # 3. The Hard Pause
        # The Python script completely freezes here for 15 seconds. 
        # Use this time to click the checkbox in the Chrome window.
        page.wait_for_timeout(15000) 
        
        print("Time is up! Extracting the chapter text now...")
        html = page.content()
        browser.close()
        
    soup = BeautifulSoup(html, "html.parser")
    clean_text = soup.get_text(separator="\n", strip=True)
    
    return clean_text

if __name__ == "__main__":
    test_url = "https://www.69shuba.com/txt/1364/4697977" 
    extracted_text = get_chapter_text(test_url)
    
    print("\n--- Extracted Text ---")
    print(extracted_text[:500]) 
    print("...")