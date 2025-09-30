# =============================================================================
#  Filename: cache_manager.py
#
#  Short Description: Cache management for newsletter data
#
#  Creation date: 2025-09-30
#  Author: Shrinivas Deshpande
# =============================================================================

"""
Cache manager for storing and retrieving newsletter data.

Handles date-based caching to avoid regenerating newsletters multiple times per day.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from loguru import logger

from NewsLetter2.models import Newsletter


class CacheManager:
    """Manages caching of newsletter data with date-based filenames."""
    
    def __init__(self, cache_dir: str = "cache"):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory path for cache storage
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        logger.info(f"Cache manager initialized with directory: {self.cache_dir}")
    
    def _get_cache_filename(self, date: Optional[datetime] = None) -> str:
        """
        Generate cache filename for a specific date.
        
        Args:
            date: Date for cache file (defaults to today)
            
        Returns:
            Filename in format: newsletter_YYYY-MM-DD.json
        """
        if date is None:
            date = datetime.now()
        return f"newsletter_{date.strftime('%Y-%m-%d')}.json"
    
    def _get_cache_path(self, date: Optional[datetime] = None) -> Path:
        """
        Get full path to cache file for a specific date.
        
        Args:
            date: Date for cache file (defaults to today)
            
        Returns:
            Full path to cache file
        """
        return self.cache_dir / self._get_cache_filename(date)
    
    def cache_exists(self, date: Optional[datetime] = None) -> bool:
        """
        Check if cache exists for a specific date.
        
        Args:
            date: Date to check (defaults to today)
            
        Returns:
            True if cache file exists for the date
        """
        cache_path = self._get_cache_path(date)
        exists = cache_path.exists()
        
        if exists:
            logger.info(f"Cache found: {cache_path}")
        else:
            logger.info(f"No cache found for {date or 'today'}")
        
        return exists
    
    def load_from_cache(self, date: Optional[datetime] = None) -> Optional[Newsletter]:
        """
        Load newsletter from cache for a specific date.
        
        Args:
            date: Date to load (defaults to today)
            
        Returns:
            Newsletter object if cache exists and is valid, None otherwise
        """
        cache_path = self._get_cache_path(date)
        
        if not cache_path.exists():
            logger.warning(f"Cache file not found: {cache_path}")
            return None
        
        try:
            logger.info(f"Loading newsletter from cache: {cache_path}")
            
            with open(cache_path, 'r') as f:
                content = f.read()
            
            # Clean markdown code fences if present
            if content.startswith('```json'):
                content = content[7:]
            elif content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            data = json.loads(content)
            newsletter = Newsletter(**data)
            
            logger.success(f"Successfully loaded newsletter from cache")
            return newsletter
            
        except Exception as e:
            logger.error(f"Error loading from cache: {e}")
            return None
    
    def save_to_cache(
        self, 
        newsletter: Newsletter, 
        date: Optional[datetime] = None
    ) -> bool:
        """
        Save newsletter to cache with date-based filename.
        
        Args:
            newsletter: Newsletter object to cache
            date: Date for cache file (defaults to today)
            
        Returns:
            True if save was successful
        """
        cache_path = self._get_cache_path(date)
        
        try:
            logger.info(f"Saving newsletter to cache: {cache_path}")
            
            # Convert to JSON
            data = newsletter.model_dump(mode='json')
            
            # Write to cache file
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.success(f"Newsletter cached successfully: {cache_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving to cache: {e}")
            return False
    
    def list_cached_newsletters(self) -> list[tuple[datetime, Path]]:
        """
        List all cached newsletters with their dates.
        
        Returns:
            List of (date, filepath) tuples for all cached newsletters
        """
        cached = []
        
        for cache_file in self.cache_dir.glob("newsletter_*.json"):
            try:
                # Extract date from filename: newsletter_YYYY-MM-DD.json
                date_str = cache_file.stem.replace("newsletter_", "")
                date = datetime.strptime(date_str, "%Y-%m-%d")
                cached.append((date, cache_file))
            except ValueError:
                logger.warning(f"Invalid cache filename format: {cache_file}")
        
        # Sort by date (newest first)
        cached.sort(key=lambda x: x[0], reverse=True)
        
        return cached
    
    def clear_old_cache(self, keep_days: int = 7) -> int:
        """
        Remove cache files older than specified days.
        
        Args:
            keep_days: Number of days to keep (default: 7)
            
        Returns:
            Number of files deleted
        """
        cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_date = cutoff_date.replace(day=cutoff_date.day - keep_days)
        
        deleted = 0
        
        for date, cache_file in self.list_cached_newsletters():
            if date < cutoff_date:
                try:
                    cache_file.unlink()
                    logger.info(f"Deleted old cache: {cache_file}")
                    deleted += 1
                except Exception as e:
                    logger.error(f"Error deleting {cache_file}: {e}")
        
        return deleted


# Global cache manager instance
cache_manager = CacheManager()
