"""Core scraping engine."""

import requests
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup
from .user_agents import random_user_agent
from .proxy import ProxyManager

class Scraper:
    """Professional web scraper with anti-bot features."""
    
    def __init__(
        self,
        use_proxies: bool = False,
        rotate_user_agent: bool = True,
        delay: float = 1.0,
        timeout: int = 30,
        proxies: list = None
    ):
        self.use_proxies = use_proxies
        self.rotate_user_agent = rotate_user_agent
        self.delay = delay
        self.timeout = timeout
        self.proxy_manager = ProxyManager(proxies or [])
        self.session = requests.Session()
    
    def scrape(
        self,
        url: str,
        selectors: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Scrape a URL and extract data."""
        # Prepare request
        req_headers = headers or {}
        if self.rotate_user_agent:
            req_headers["User-Agent"] = random_user_agent()
        
        # Get proxy
        proxy = None
        if self.use_proxies:
            proxy = self.proxy_manager.get_proxy()
        
        # Make request
        try:
            response = self.session.get(
                url,
                headers=req_headers,
                proxies={"http": proxy, "https": proxy} if proxy else None,
                timeout=self.timeout
            )
            response.raise_for_status()
        except requests.RequestException as e:
            return {"error": str(e), "url": url}
        
        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract data
        if selectors:
            data = {}
            for key, selector in selectors.items():
                element = soup.select_one(selector)
                data[key] = element.text.strip() if element else None
            return data
        
        return {
            "url": url,
            "status": response.status_code,
            "title": soup.title.string if soup.title else None,
            "links": len(soup.find_all("a")),
            "images": len(soup.find_all("img"))
        }
    
    def export(self, data: Any, format: str = "json", file: str = None):
        """Export scraped data."""
        import json
        import csv
        
        if format == "json":
            content = json.dumps(data, indent=2)
            if file:
                with open(file, "w") as f:
                    f.write(content)
            return content
        
        elif format == "csv":
            if isinstance(data, list) and data:
                keys = data[0].keys()
                output = ",".join(keys) + "\n"
                for row in data:
                    output += ",".join(str(row.get(k, "")) for k in keys) + "\n"
                if file:
                    with open(file, "w") as f:
                        f.write(output)
                return output
        
        return str(data)
