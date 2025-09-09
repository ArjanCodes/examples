import logging
from dataclasses import dataclass
from typing import Protocol, Any
from db import db_session, init_db, Article

# -----------------------------------
# Protocols for loose coupling
# -----------------------------------

class LoggerProtocol(Protocol):
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def error(self, msg: str, *args: Any, **kwargs: Any) -> None: ...

class DBProtocol(Protocol):
    def query(self, *args: Any, **kwargs: Any) -> Any: ...

# -----------------------------------
# Context Object
# -----------------------------------

@dataclass
class AppContext:
    user_id: int
    db: DBProtocol
    logger: LoggerProtocol
    config: dict[str, Any]

# -----------------------------------
# Application Logic
# -----------------------------------

def render_article(article_id: int, db: DBProtocol, logger: LoggerProtocol) -> str:
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        logger.error(f"Article {article_id} not found.")
        return "<p>Article not found.</p>"

    logger.info(f"Rendering article {article_id}")
    html = f"<h1>{article.title}</h1><p>{article.body}</p>"
    return html

def send_to_external_service(html: str, api_key: str) -> None:
    print(f"Sending to API with key {api_key[:4]}... Content: {html[:30]}...")

def publish_article(article_id: int, context: AppContext) -> None:
    html = render_article(
        article_id,
        db=context.db,
        logger=context.logger,
    )
    send_to_external_service(html, context.config['api_key'])

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

        publish_article(1, context)
        publish_article(2, context)
        publish_article(999, context)  # Not found example

if __name__ == "__main__":
    main()

    
