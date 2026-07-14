"""AI Scraper Pro - Professional web scraping framework."""

from .core import Scraper
from .proxy import ProxyManager
from .user_agents import random_user_agent

__version__ = "1.0.0"
__all__ = ["Scraper", "ProxyManager", "random_user_agent"]
