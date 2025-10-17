from django.core.management.base import BaseCommand
from scraper.scraper import parse_website
import logging
import json
from articles.models import Article

ARTICLE_LIST = 'static/article_urls_list.json'

logging.basicConfig(filename="logs/logfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:

        try:
            with open(ARTICLE_LIST) as f:
                json_data = json.load(f)
        except Exception as err:
            print(f'Error reading JSON file! Error: {err}')
            return

        logger.info(f'Starting scraping articles.')
        for i, url in enumerate(json_data['urls']):
            print(f'Scraping article {i+1}/{len(json_data["urls"])}')

            if not Article.objects.filter(url=url).exists():
                data = parse_website(url)

                if data:
                    try:
                        obj = Article.objects.create(
                            title=data['title'],
                            html_content=data['html_content'],
                            content=data['content'],
                            url=data['url'],
                            published=data['date']
                        )
                        logger.info(f'Article {obj} saved to db successfully.')

                    except Exception as err:
                        logger.critical(f'Unable to save object to db! {err}')

            else:
                logger.info('Article already in database. Skipping...')

        print("All articles scraped.")
        logger.info('All defined articles scraped. Session closed.')