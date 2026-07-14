"""Proxy rotation manager."""

import random
from typing import List, Optional

class ProxyManager:
    """Manages proxy rotation for scraping."""
    
    def __init__(self, proxies: List[str] = None):
        self.proxies = proxies or []
        self.current_index = 0
    
    def get_proxy(self) -> Optional[str]:
        """Get next proxy in rotation."""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
    
    def add_proxy(self, proxy: str):
        """Add a proxy to the pool."""
        if proxy not in self.proxies:
            self.proxies.append(proxy)
    
    def remove_proxy(self, proxy: str):
        """Remove a proxy from the pool."""
        if proxy in self.proxies:
            self.proxies.remove(proxy)
    
    def get_random_proxy(self) -> Optional[str]:
        """Get a random proxy."""
        if not self.proxies:
            return None
        return random.choice(self.proxies)
