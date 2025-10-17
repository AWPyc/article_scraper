# Web Article Scraper 🌐

A simple article web scraper with integrated DRF API to access scraped data. 

---

## ⚙️ Features

* Scraping web articles
* Articles list to scrape can be extended 
  * ```/static/article_urls.list.json```
* Django management command
* DRF API:
    * All scraped data available at API in JSON format 
    * Filtering articles by domain, partial or full url
    * Articles can be added or modified manually via API
* PostgreSQL database
* Dockerized environment with **docker-compose**

---

## 🐳 Run with Docker

1. Clone the repository:

   ```bash
   git clone https://github.com/AWPyc/article_scraper.git
   cd article_scraper
   ``` 

2. Copy example environment and adjust values:

   ```bash
   cp .env_example .env
   ```

   Adjust values in `.env`:

   ```
   DEBUG=true
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

   POSTGRES_USER=example_user
   POSTGRES_PASSWORD=example_passwd
   POSTGRES_DB=example_db
   ```

3. Build and run:

   ```bash
   docker-compose up --build
   ```

4. Migrations should be done automatically, if not run them manually (only needed first time if container didn’t do it):

   ```bash
   docker-compose run migrate
   ```

5. API endpoints:

   * Root API: `http://localhost:8000/`
   * Admin panel: `http://localhost:8000/admin/`
   * Articles list: `http://localhost:8000/articles/`
   * Articles' details: `http://localhost:8000/articles/<article_id>/`


6. Scraper usage:
   * Enter docker container:
     ```docker exec -it scraper-backend bash```
   * Run command:
     ```python3 manage.py scrape_articles```

---
