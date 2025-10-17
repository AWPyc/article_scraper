from readability import Document
import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import logging
from dateparser import parse
import warnings

warnings.filterwarnings("ignore", category=FutureWarning, module='readability')

logging.basicConfig(filename="logs/logfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

USER_AGENT = "MyScraperBot/1.0"

def fetch_url_playwright(url):
    """Returns html page object and parsed url"""
    html, parsed_url = None, None
    context, browser = None, None

    with sync_playwright() as p:
        try:
            logger.info('Starting website session...')
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=USER_AGENT)
            page = context.new_page()
            logger.info('Session created. Blank page opened.')

            logger.info('Redirecting to url...')
            page.goto(url, timeout=10000)
            html = page.content()
            parsed_url = page.url
            logger.info('Successfully redirected to desired url.')

        except Exception as err:
            print(f'Domain {url} unreachable.')
            logger.error(f'Unable to open desired url. {err}')

        finally:
            if all([context, browser]):
                logger.info('Shutting down browser session.')
                context.close()
                browser.close()
            logger.info('Browser session closed.')



    return html, parsed_url

def parse_title(page) -> str | None:
    """Extracts title from Readability Document object, if not found returns None."""

    if len(page.title()) > 0:
        return page.title()

    logger.warning('Page title not found!')
    return None

def parse_html_content(page) -> str | None:
    """Extracts raw html from Readability Document object, if not found returns None."""

    if len(page.content()) > 0:
        return page.content()

    logger.warning('Could not parse raw html!')
    return None

def parse_plain_content(page) -> str | None:
    """Extracts content plain text from Readability Document object, if not found returns None."""

    soup = BeautifulSoup(page.summary(), 'lxml')
    plain_content = soup.get_text(separator='\n', strip=True)
    if plain_content:
        return plain_content.strip()

    logger.warning('Could not parse plain html text!')
    return None

def parse_url(html) -> str | None:
    """Extracts url from Playwright object, if not found returns None."""

    soup = BeautifulSoup(html,'lxml')

    possible_url_names = ['og:url', 'url']
    for name in possible_url_names:
        meta = soup.find('meta', property=name)
        if meta:
            return meta['content']

    logger.warning('Url not found!')
    return None

def parse_date(html) -> str | None:
    """Extracts published date from Playwright object, if not found returns None."""

    settings = {'RETURN_AS_TIMEZONE_AWARE': True}
    possible_names = ['article:published_time', 'datePublished', 'date', 'published', 'og:published',
                      'og:datePublished', 'og:published_time']

    soup = BeautifulSoup(html, 'lxml')
    for name in possible_names:
        meta = soup.find('meta', property=name)
        if meta:
            return parse(meta.get('content', None), settings=settings)

    for s in soup.find_all('script', type='application/ld+json'):
        try:
            payload = json.loads(s.string)
        except Exception:
            continue

        candidate = payload if isinstance(payload, list) else [payload]
        for obj in candidate:
            for key in possible_names:
                if key in obj:
                    return parse(obj.get(key, None), settings=settings)

    logger.warning('Date not found!')
    return None

def parse_website(url) -> dict | None:
    """
    Parses article websites':
        - title
        - raw html content
        - plain text content
        - url
        - published date
    """
    html, url = fetch_url_playwright(url)

    if html:
        page = Document(html)

        title = parse_title(page)
        html_content = parse_html_content(page)
        content = parse_plain_content(page)
        url = url if url else parse_url(html)
        date = parse_date(html)

        if not all([title, html_content, content, url, date]):
            logger.warning('Missing crucial fields in parsed article! Skipping article...')
            return None

        return {
            'title': title,
            'html_content': html_content,
            'content': content,
            'url': url,
            'date': date
        }

    logger.error('Could not obtain html object! Skipping...')
    return None
