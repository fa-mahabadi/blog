
# 📝 Django Blog Pro

A robust, feature-rich blogging engine built with Django and powered by PostgreSQL. This project implements advanced web features including full-text search, automated sitemaps, and a recommendation engine.

## 🚀 Features

- [x] Advanced Search: Full-text search engine powered by PostgreSQL (using Trigram similarity).

- [x] Content Organization: Comprehensive Tagging and Categorization system.

- [x] User Engagement: Interactive Comment system and Email notifications via Django.

- [x] Smart Discovery: “Similar Posts” recommendation engine based on content similarity.

- [x] SEO Ready: Integrated Sitemap and RSS feed support.

- [x] Enhanced UX: Pagination and custom Template Tags/Filters for reusable UI logic.

## 🛠 Tech Stack

* Backend: Python & Django

* Database: PostgreSQL (Primary) / SQLite (Development)

* Search Engine: PostgreSQL pg_trgm extension for fuzzy matching.

* Deployment Ready: Docker & Docker Compose support.

## ⚙️ Getting Started

#### Prerequisites
Ensure you have the following installed:

* Python 3.10+

* PostgreSQL (or use the provided Docker configuration)

* pip (Python package manager)

#### Installation & Setup

1. Clone the repository:
bash
    `git clone https://github.com/fa-mahabadi/blog.git`
    cd blog
2. Create and activate a virtual environment:

    ### On Windows
    `python -m venv venv`

    `venv\Scripts\activate`

    ### On macOS/Linux
    `python3 -m venv venv`

    `source venv/bin/activate`

3. Install dependencies:

    `pip install -r requirements.txt`

4. Database Setup:
If you are using PostgreSQL locally, update your settings.py. If using Docker, simply run:

    `docker-compose up -d`

5. Run Migrations:

    `python manage.py migrate`

6. Start the development server:

    `python manage.py runserver`

7. Visit `http://127.0.0.1:8000/` to see your blog in action!