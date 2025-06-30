import re
from playwright.sync_api import sync_playwright

def get_x_follower_count(username: str) -> int | None:
    """Usa Playwright para obtener el número de seguidores de un perfil de X."""
    url = f"https://x.com/{username}"
    followers = None
    print(f"--- Iniciando scraping para @{username} ---")
    print(f"Lanzando navegador para ir a: {url}")

    with sync_playwright() as p:
        browser = None
        try:
            browser = p.chromium.launch(
                channel="chrome",
                headless=True,
                args=["--start-maximized"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
                no_viewport=True,
            )
            page = context.new_page()
            page.goto(url, wait_until="load", timeout=60000)
            print("Página cargada. Buscando el contador de seguidores...")

            followers_locator = page.get_by_role("link", name=re.compile(r"seguidores|followers", re.IGNORECASE))
            followers_locator.wait_for(timeout=30000)
            
            followers_text = followers_locator.get_attribute("aria-label") or followers_locator.inner_text()
            print(f"Texto encontrado: '{followers_text}'")

            followers_digits = re.findall(r'\d+', followers_text)
            if followers_digits:
                followers = int("".join(followers_digits))
        except Exception as e:
            print(f"Ha ocurrido un error durante el scraping: {e}")
            if 'page' in locals():
                page.screenshot(path='error_screenshot.png', full_page=True)
                print("Se ha guardado una captura de pantalla del error en 'error_screenshot.png'")
        finally:
            if browser and browser.is_connected():
                browser.close()
    
    if followers is not None:
        print(f"Scraping exitoso: @{username} tiene {followers} seguidores.")
    else:
        print(f"No se pudo obtener el número de seguidores para @{username}.")
    
    return followers 