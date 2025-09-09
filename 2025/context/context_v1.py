import logging
from dataclasses import dataclass
from typing import Any
from db import db_session, init_db, Article , Session

# -----------------------------------
# Context Object
# -----------------------------------

@dataclass
class AppContext:
    user_id: int
    db: Session
    logger: logging.Logger
    config: dict[str, Any]

# -----------------------------------
# Application Logic
# -----------------------------------

def render_article(article_id: int, context: AppContext) -> str:
    article = context.db.query(Article).filter(Article.id == article_id).first()
    if not article:
        context.logger.error(f"Article {article_id} not found.")
        return "<p>Article not found.</p>"

    context.logger.info(f"Rendering article {article_id}")
    html = f"<h1>{article.title}</h1><p>{article.body}</p>"
    return html
# -----------------------------------
# Entry Point
# -----------------------------------

def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("app")

    init_db()

    with db_session() as session:
        context = AppContext(
            user_id=42,
            db=session,
            logger=logger,
            config={"api_key": "abcdef123456"},
        )

        html = render_article(1, context)
        print(html)

        html = render_article(999, context)  # not found
        print(html)

if __name__ == "__main__":
    main()

    
