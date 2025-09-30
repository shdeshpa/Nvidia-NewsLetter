# =============================================================================
#  Filename: models.py
#
#  Short Description: Pydantic models for NVIDIA AI newsletter data structures
#
#  Creation date: 2025-09-30
#  Author: Shrinivas Deshpande
# =============================================================================

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class RawNewsArticle(BaseModel):
    """
    Raw news article collected by the Reporter agent.
    
    Represents an unprocessed news item from SerpAPI search results.
    """
    
    title: str = Field(..., description="Article headline")
    source: str = Field(..., description="Publication or website name")
    url: HttpUrl = Field(..., description="Link to the original article")
    snippet: str = Field(..., description="Brief excerpt from the article")
    thumbnail: Optional[HttpUrl] = Field(None, description="Image URL if available")
    published_date: Optional[str] = Field(None, description="Publication date")


class ProcessedNewsArticle(BaseModel):
    """
    Processed news article after Editor agent summarization.
    
    Contains both a concise summary for the landing page and detailed analysis
    for the individual article view.
    """
    
    title: str = Field(..., description="Article headline")
    source: str = Field(..., description="Publication or website name")
    url: HttpUrl = Field(..., description="Link to the original article")
    thumbnail: Optional[HttpUrl] = Field(None, description="Featured image URL")
    short_summary: str = Field(
        ...,
        description="2-3 sentence engaging summary for landing page"
    )
    detailed_article: str = Field(
        ...,
        description="20-30 sentence in-depth analysis with business implications"
    )
    published_date: Optional[str] = Field(None, description="Publication date")


class Editorial(BaseModel):
    """
    Front-page editorial content created by Senior Editor agent.
    
    Provides strategic analysis, trend insights, competitive positioning,
    and actionable recommendations for tech leaders.
    """
    
    headline: str = Field(..., description="Editorial title")
    narrative: str = Field(
        ...,
        description="800-1000 word editorial on NVIDIA's AI position"
    )
    trend_analysis: str = Field(
        ...,
        description="Analysis of patterns across the 10 news stories"
    )
    product_leader_insights: str = Field(
        ...,
        description="Actionable insights for enterprise leaders and PMs"
    )
    competition_analysis: str = Field(
        ...,
        description="NVIDIA vs AMD, Intel, and hyperscalers comparison"
    )
    image_url: Optional[HttpUrl] = Field(None, description="Featured image for editorial")
    created_at: datetime = Field(default_factory=datetime.now)


class Newsletter(BaseModel):
    """
    Complete newsletter package ready for UI rendering.
    
    Contains the editorial and all processed news articles, validated
    and approved by the Senior Editor agent.
    """
    
    editorial: Editorial = Field(..., description="Front-page editorial content")
    articles: list[ProcessedNewsArticle] = Field(
        ...,
        description="List of 10 processed NVIDIA news articles",
        min_length=10,
        max_length=10
    )
    generated_at: datetime = Field(default_factory=datetime.now)
    edition_number: Optional[int] = Field(None, description="Newsletter edition number")
