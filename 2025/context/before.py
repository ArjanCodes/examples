import logging
from db import db_session, init_db, Article, Session

# -----------------------------------
# Application Logic
# -----------------------------------

def render_article(article_id: int, db: Session, logger: logging.Logger, api_key: str) -> str:
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        logger.error(f"Article {article_id} not found.")
        return "<p>Article not found.</p>"

    logger.info(f"Rendering article {article_id} using API key {api_key[:4]}...")
    html = f"<h1>{article.title}</h1><p>{article.body}</p>"
    return html

def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("app")

    init_db()

    with db_session() as session:

        api_key = "abcdef123456"

        html = render_article(1, session, logger, api_key)
        print(html)

        html = render_article(999, session, logger, api_key)  # not found
        print(html)


if __name__ == "__main__":
    main()

    
