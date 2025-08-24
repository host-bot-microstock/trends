# scraper.py (Revisi Lengkap untuk Perbaikan Akhir)

import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
import time
import random
import os

# Import baru untuk Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# --- Daftar User-Agent untuk Rotasi ---
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
]


def get_random_user_agent():
    """Mengembalikan User-Agent acak."""
    return random.choice(USER_AGENTS)


# --- Fungsi untuk Mengukur Permintaan (Demand) ---
def get_google_trends_score(keyword: str) -> int:
    """
    Mengambil skor popularitas dari Google Trends dengan jeda yang lebih lama.
    """
    try:
        time.sleep(random.uniform(8, 12))
        # Argumen 'method_whitelist' Dihapus karena tidak valid
        pytrends = TrendReq(hl='en-US', tz=360, retries=3, backoff_factor=0.5)
        pytrends.build_payload([keyword],
                               cat=0,
                               timeframe='today 3-m',
                               geo='',
                               gprop='')
        interest_over_time_df = pytrends.interest_over_time()

        if interest_over_time_df.empty or keyword not in interest_over_time_df.columns:
            print(
                f"Peringatan: Tidak ada data Google Trends untuk '{keyword}'.")
            return 0

        last_score = interest_over_time_df[keyword].iloc[-1]
        print(f"Skor Google Trends untuk '{keyword}': {last_score}")
        return int(last_score)

    except Exception as e:
        print(
            f"Error saat mengambil data Google Trends untuk '{keyword}': {e}")
        return 0


# --- Fungsi untuk Mengukur Kompetisi (Supply) dengan SELENIUM yang Diperbaiki ---
def get_shutterstock_competition_selenium(keyword: str) -> int:
    """
    Melakukan scraping ke Shutterstock menggunakan Selenium dengan konfigurasi Replit.
    """
    print(
        f"Menganalisis Shutterstock untuk '{keyword}' menggunakan Selenium...")
    formatted_keyword = keyword.replace(' ', '-')
    url = f"https://www.shutterstock.com/search/{formatted_keyword}"

    # Setup Opsi Chrome agar bisa berjalan di Replit
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
    chrome_options.add_argument("window-size=1920,1080")

    # Menentukan lokasi biner Chrome di Replit
    chrome_options.binary_location = '/usr/bin/google-chrome'

    driver = None
    try:
        # Menentukan lokasi driver yang diinstal oleh webdriver-manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)

        # Jeda acak untuk meniru perilaku manusia dan menunggu halaman dimuat
        time.sleep(random.uniform(4, 6))

        # Mencari elemen yang berisi jumlah hasil
        result_element = driver.find_element(
            By.XPATH, "//*[contains(text(), 'stock images')]")

        result_text = result_element.text
        # Ekstrak hanya angka dari teks
        number_str = ''.join(
            filter(str.isdigit,
                   result_text.split("stock images")[0]))

        if number_str:
            competition_count = int(number_str)
            print(
                f"Jumlah kompetisi di Shutterstock untuk '{keyword}': {competition_count}"
            )
            return competition_count

        print(
            f"Peringatan: Tidak dapat menemukan jumlah kompetisi Shutterstock untuk '{keyword}'."
        )
        return 0

    except NoSuchElementException:
        print(
            f"Peringatan: Elemen jumlah kompetisi tidak ditemukan di halaman untuk '{keyword}'."
        )
        return 0
    except Exception as e:
        print(
            f"Error saat scraping Selenium ke Shutterstock untuk '{keyword}': {e}"
        )
        return 0
    finally:
        if driver:
            driver.quit()
