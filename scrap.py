import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import ndjson
import gzip
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

class GrabFoodScraper:
    def __init__(self, base_url, locations, max_workers=5):
        self.base_url = base_url
        self.locations = locations
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.max_workers = max_workers
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    def get_location_url(self, location):
        return f"{self.base_url}?location={location}"
    
    def scrape_location(self, location):
        url = self.get_location_url(location)
        self.driver.get(url)
        time.sleep(random.uniform(3, 6))
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        restaurants = []
        
        for restaurant in soup.find_all('div', class_='restaurant-card'):
            data = self.extract_restaurant_data(restaurant)
            if data:
                restaurants.append(data)
        
        return restaurants
    
    def extract_restaurant_data(self, restaurant):
        try:
            name = restaurant.find('h2').text.strip()
            cuisine = restaurant.find('p', class_='cuisine').text.strip()
            rating = restaurant.find('div', class_='rating').text.strip()
            delivery_time = restaurant.find('div', class_='delivery-time').text.strip()
            distance = restaurant.find('div', class_='distance').text.strip()
            promo = restaurant.find('div', class_='promo')
            promo_available = bool(promo)
            promo_details = promo.text.strip() if promo else None
            image_link = restaurant.find('img')['src']
            restaurant_id = restaurant['data-restaurant-id']
            latitude = restaurant['data-latitude']
            longitude = restaurant['data-longitude']
            delivery_fee = restaurant.find('div', class_='delivery-fee').text.strip()
            
            return {
                "Restaurant Name": name,
                "Restaurant Cuisine": cuisine,
                "Restaurant Rating": rating,
                "Estimate time of Delivery": delivery_time,
                "Restaurant Distance from Delivery Location": distance,
                "Promotional Offers Listed for the Restaurant": promo_details,
                "Restaurant Notice If Visible": None,
                "Image Link of the Restaurant": image_link,
                "Is promo available": promo_available,
                "Restaurant ID": restaurant_id,
                "Restaurant latitude and longitude": (latitude, longitude),
                "Estimate Delivery Fee": delivery_fee
            }
        except Exception as e:
            logging.error(f"Error extracting data for restaurant: {e}")
            return None

    def save_data(self, data, filename='restaurants.ndjson.gz'):
        with gzip.open(filename, 'wt', encoding='utf-8') as f:
            writer = ndjson.writer(f)
            writer.writerows(data)
        logging.info(f"Data saved to {filename}")
    
    def run(self):
        all_restaurants = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_location = {executor.submit(self.scrape_location, location): location for location in self.locations}
            for future in as_completed(future_to_location):
                location = future_to_location[future]
                try:
                    restaurants = future.result()
                    logging.info(f"Scraped {len(restaurants)} restaurants from location: {location}")
                    all_restaurants.extend(restaurants)
                except Exception as e:
                    logging.error(f"Error scraping location {location}: {e}")
        
        unique_restaurants = {restaurant['Restaurant ID']: restaurant for restaurant in all_restaurants}.values()
        self.save_data(unique_restaurants)
