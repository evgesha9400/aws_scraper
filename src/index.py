import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import Settings

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


settings = Settings()
engine = create_engine(settings.database_dsn)
SessionLocal = sessionmaker(bind=engine)


def get_soup(url: str, timeout=600) -> BeautifulSoup:
    """
    :param url: URL to load
    :param timeout: Timeout in seconds
    :return: BeautifulSoup instance
    """
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    logger.info("Getting URL")
    driver.get(url)
    logger.info("Waiting for element")
    logger.info("Getting page source")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup


def check_db():
    """Check database connection."""
    try:
        # Create a new session
        session = SessionLocal()

        # Execute a simple statement to check the connection
        session.execute("SELECT 1").fetchall()

        # Close the session
        session.close()

        print("Database connection successful.")

    except Exception as e:
        print(f"Failed to connect to the database. Error: {e}")


def handler(event, context):
    logger.info(f"Getting soup from {settings.url}")
    soup = get_soup(settings.url)
    logger.info(f"Soup: {soup.text[:60]}...")
    check_db()


if __name__ == "__main__":
    handler(None, None)
