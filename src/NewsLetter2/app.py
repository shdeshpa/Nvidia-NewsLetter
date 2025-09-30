# =============================================================================
#  Filename: app.py
#
#  Short Description: Streamlit UI for NVIDIA AI Newsletter
#
#  Creation date: 2025-09-30
#  Author: Shrinivas Deshpande
# =============================================================================

import json
import os
from datetime import datetime
from pathlib import Path

import streamlit as st
from loguru import logger

from NewsLetter2.crew import run_newsletter_generation
from NewsLetter2.models import Newsletter, ProcessedNewsArticle


# Page configuration
st.set_page_config(
    page_title="NVIDIA AI Newsletter",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Custom CSS for newsletter styling
def load_custom_css() -> None:
    """Apply custom CSS styling for professional newsletter appearance."""
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #76B900;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #666;
            text-align: center;
            margin-bottom: 2rem;
        }
        .editorial-box {
            padding: 1rem 0;
            border-left: 5px solid #76B900;
            padding-left: 1.5rem;
            margin-bottom: 2rem;
        }
        .news-card {
            padding: 1rem 0;
            margin-bottom: 1rem;
        }
        .news-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 0.5rem;
        }
        .news-source {
            font-size: 0.9rem;
            color: #76B900;
            margin-bottom: 0.5rem;
        }
        .section-divider {
            height: 2px;
            background: linear-gradient(to right, #76B900, transparent);
            margin: 2rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_newsletter_data() -> Newsletter | None:
    """
    Load newsletter data intelligently from cache, session, or file.
    
    Priority order:
    1. Session state (current session)
    2. Today's cache (if exists)
    3. Legacy output file (fallback)
    
    Returns:
        Newsletter object if available, None otherwise
    """
    from NewsLetter2.cache_manager import cache_manager
    from datetime import datetime
    
    # Check if newsletter exists in session state
    if "newsletter" in st.session_state:
        logger.info("Loading newsletter from session state")
        return st.session_state.newsletter
    
    # Check cache for today's newsletter
    if cache_manager.cache_exists():
        logger.info("Loading newsletter from today's cache")
        newsletter = cache_manager.load_from_cache()
        if newsletter:
            st.session_state.newsletter = newsletter
            st.session_state.loaded_from_cache = True
            st.session_state.cache_date = datetime.now().strftime("%Y-%m-%d")
            return newsletter
    
    # Fallback: Try loading from legacy output file
    output_file = Path("newsletter_output.json")
    if output_file.exists():
        try:
            logger.info("Loading newsletter from legacy output file")
            with open(output_file) as f:
                content = f.read()
                
                # Remove markdown code fences if present
                if content.startswith('```json'):
                    content = content[7:]
                elif content.startswith('```'):
                    content = content[3:]
                if content.endswith('```'):
                    content = content[:-3]
                content = content.strip()
                
                data = json.loads(content)
                newsletter = Newsletter(**data)
                st.session_state.newsletter = newsletter
                st.session_state.loaded_from_cache = False
                return newsletter
        except Exception as e:
            logger.error(f"Error loading newsletter from file: {e}")
    
    return None


def generate_newsletter() -> None:
    """Generate new newsletter using CrewAI workflow."""
    with st.spinner("🚀 Generating NVIDIA AI Newsletter... This may take a few minutes."):
        try:
            result = run_newsletter_generation()
            
            # CrewAI returns a CrewOutput object, load from file instead
            output_file = Path("newsletter_output.json")
            if output_file.exists():
                with open(output_file) as f:
                    content = f.read()
                    
                    # Remove markdown code fences if present
                    if content.startswith('```json'):
                        content = content[7:]
                    elif content.startswith('```'):
                        content = content[3:]
                    if content.endswith('```'):
                        content = content[:-3]
                    content = content.strip()
                    
                    data = json.loads(content)
                    newsletter = Newsletter(**data)
                    st.session_state.newsletter = newsletter
                    st.success("✅ Newsletter generated successfully!")
                    st.rerun()
            else:
                # Fallback: try to parse result directly
                if isinstance(result, dict):
                    newsletter = Newsletter(**result)
                elif hasattr(result, 'json'):
                    newsletter = Newsletter(**result.json())
                elif hasattr(result, 'raw'):
                    data = json.loads(result.raw)
                    newsletter = Newsletter(**data)
                else:
                    raise ValueError("Could not parse newsletter result")
                
                st.session_state.newsletter = newsletter
                st.success("✅ Newsletter generated successfully!")
                st.rerun()
            
        except Exception as e:
            logger.error(f"Error generating newsletter: {e}")
            st.error(f"Failed to generate newsletter: {str(e)}")


def render_landing_page(newsletter: Newsletter) -> None:
    """
    Render the newsletter landing page with editorial and article summaries.
    
    Args:
        newsletter: Complete newsletter data
    """
    load_custom_css()
    
    # Header
    st.markdown('<div class="main-header">🚀 NVIDIA AI Newsletter</div>', unsafe_allow_html=True)
    
    # Show cache indicator if loaded from cache
    if st.session_state.get("loaded_from_cache", False):
        st.info(f"📦 Loaded from cache: {st.session_state.get('cache_date', 'today')}")
    
    st.markdown(
        f'<div class="sub-header">Edition • {newsletter.generated_at.strftime("%B %d, %Y")}</div>',
        unsafe_allow_html=True,
    )
    
    # Editorial Section
    st.markdown('<div class="editorial-box">', unsafe_allow_html=True)
    st.markdown(f"## 📰 {newsletter.editorial.headline}")
    
    st.markdown("### 📝 Executive Summary")
    st.markdown(newsletter.editorial.narrative)
    st.markdown("")
    
    with st.expander("📊 **Trend Analysis** - Market Patterns & Insights", expanded=False):
        st.markdown(newsletter.editorial.trend_analysis)
    
    with st.expander("💡 **Product Leader Insights** - Strategic Recommendations", expanded=False):
        st.markdown(newsletter.editorial.product_leader_insights)
    
    with st.expander("⚔️ **NVIDIA vs Competition** - Competitive Landscape", expanded=False):
        st.markdown(newsletter.editorial.competition_analysis)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # News Articles Grid
    st.markdown("## 📡 Latest NVIDIA News")
    st.markdown("*Click 'Read Full Analysis' button below each article to view complete details*")
    st.markdown("")
    
    # Display articles in 2-column grid
    for idx in range(0, len(newsletter.articles), 2):
        cols = st.columns(2)
        
        for col_idx, col in enumerate(cols):
            article_idx = idx + col_idx
            if article_idx < len(newsletter.articles):
                article = newsletter.articles[article_idx]
                
                with col:
                    # Create card container
                    st.markdown('<div class="news-card">', unsafe_allow_html=True)
                    
                    # Thumbnail - try to display, skip if fails
                    if article.thumbnail:
                        try:
                            st.image(str(article.thumbnail), width='stretch')
                        except Exception:
                            # Show placeholder only if image fails
                            st.markdown("📰 *Image unavailable*")
                    
                    # Title and source
                    st.markdown(f"### {article.title}")
                    st.caption(f"📍 {article.source}")
                    
                    # Summary preview
                    st.markdown(article.short_summary)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Read more button
                    if st.button(
                        "📖 Read Full Analysis →", 
                        key=f"article_{article_idx}", 
                        use_container_width=True, 
                        type="primary"
                    ):
                        st.session_state.selected_article = article_idx
                        st.rerun()
                    
                    st.markdown("")  # Add spacing between cards


def render_article_page(article: ProcessedNewsArticle) -> None:
    """
    Render individual article page with detailed analysis.
    
    Args:
        article: Processed news article with detailed content
    """
    load_custom_css()
    
    # Back button
    if st.button("← Back to Newsletter"):
        st.session_state.selected_article = None
        st.rerun()
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Article header
    st.markdown(f'<div class="news-title">{article.title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="news-source">{article.source}</div>', unsafe_allow_html=True)
    
    if article.published_date:
        st.caption(f"Published: {article.published_date}")
    
    # Featured image with error handling
    if article.thumbnail:
        try:
            st.image(str(article.thumbnail), width='stretch')
        except Exception:
            st.info("📷 Image unavailable")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Quick summary in prominent box
    st.markdown("### 📋 Executive Summary")
    st.info(article.short_summary)
    
    st.markdown("")
    
    # Detailed article - ensure we show ALL content
    st.markdown("### 📊 In-Depth Analysis & Strategic Implications")
    
    # Display the full detailed article
    detailed_content = article.detailed_article
    
    # If content seems too short, provide context
    if len(detailed_content) < 300:
        st.warning("⚠️ Limited detailed content available for this article. Showing summary with context:")
        st.markdown(f"""
        **Article Context:**
        
        {article.short_summary}
        
        **Additional Analysis:**
        
        {detailed_content}
        
        **Strategic Implications for Technology Leaders:**
        
        This development in NVIDIA's ecosystem has several key implications:
        - **Market Position**: Reinforces NVIDIA's leadership in AI infrastructure
        - **Enterprise Impact**: Affects procurement and deployment decisions for AI platforms
        - **Competitive Dynamics**: Influences the broader semiconductor and AI chip landscape
        - **Product Strategy**: Provides insights for product managers evaluating AI solutions
        """)
    else:
        # Show full content with better formatting
        st.markdown(detailed_content)
    
    # Key takeaways section
    st.markdown("---")
    st.markdown("### 💡 Why This Matters for Tech Leaders")
    st.success("""
    **Strategic Takeaways:**
    - This article provides insights into NVIDIA's market positioning and technology strategy
    - Understanding these developments helps inform enterprise AI adoption decisions
    - The competitive landscape insights aid in vendor selection and partnership strategies
    - Product managers can leverage this analysis for platform and architecture planning
    """)
    
    # Original source link
    st.markdown("---")
    st.markdown(f"### 🔗 Read the Original Article")
    st.markdown(f"For complete details and additional context, visit the full article at **{article.source}**:")
    st.markdown(f"[{article.url}]({article.url})")
    
    # Back to top button
    st.markdown("")
    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⬆️ Back to Newsletter", key="back_top", use_container_width=True, type="primary"):
            st.session_state.selected_article = None
            st.rerun()


def main() -> None:
    """Main application entry point."""
    # Sidebar for generation
    with st.sidebar:
        st.title("⚙️ Newsletter Control")
        
        if st.button("Generate New Newsletter", type="primary"):
            generate_newsletter()
        
        st.markdown("---")
        
        # Cache status
        from NewsLetter2.cache_manager import cache_manager
        from datetime import datetime
        
        st.markdown("### 📦 Cache Status")
        
        if cache_manager.cache_exists():
            st.success(f"✅ Today's newsletter cached")
            st.caption(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        else:
            st.info("ℹ️ No cache for today")
        
        # List recent cached newsletters
        cached = cache_manager.list_cached_newsletters()
        if cached and len(cached) > 1:
            st.markdown("**Recent editions:**")
            for date, _ in cached[:5]:
                st.caption(f"• {date.strftime('%Y-%m-%d')}")
        
        # Clear old cache button
        if st.button("🗑️ Clear Old Cache (>7 days)", use_container_width=True):
            deleted = cache_manager.clear_old_cache(keep_days=7)
            if deleted > 0:
                st.success(f"Deleted {deleted} old cache file(s)")
            else:
                st.info("No old cache files to delete")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown(
            "This newsletter is powered by CrewAI agents using OpenAI API "
            "and SerpAPI for real-time NVIDIA news collection and analysis."
        )
    
    # Load newsletter data
    newsletter = load_newsletter_data()
    
    if newsletter is None:
        st.info("👋 Welcome! Click 'Generate New Newsletter' in the sidebar to get started.")
        st.markdown(
            """
            ### How it works:
            
            1. **Reporter Agent** searches for the 10 latest NVIDIA AI news using SerpAPI
            2. **Editor Agent** summarizes and analyzes each article for tech leaders
            3. **Senior Editor Agent** validates content, writes editorial, and provides 
               competitive analysis
            4. **You** get a professionally formatted newsletter with strategic insights!
            
            *Note: Generation takes 2-5 minutes depending on API response times.*
            """
        )
        return
    
    # Route to appropriate page
    if "selected_article" in st.session_state and st.session_state.selected_article is not None:
        article_idx = st.session_state.selected_article
        render_article_page(newsletter.articles[article_idx])
    else:
        render_landing_page(newsletter)


if __name__ == "__main__":
    main()
