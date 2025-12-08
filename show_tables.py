import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'aamcare.settings'
import django
django.setup()

from django.db import connection

cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()

print("=== ALL DATABASE TABLES ===")
for t in tables:
    print(f"  - {t[0]}")
