# 1) server:
# 1.1) for run with new db structure:
# web: alembic revision --autogenerate -m "add telegram id"; alembic upgrade head; gunicorn app:app
# 1.2) for simple run:
web: gunicorn app:app

# 2) telegram bot:
# telegram: python tg_bot.py