import streamlit as st
from GrabFoodScraper import GrabFoodScraper  # Import your scraper class
import os

def main():
    st.title("GrabFood Scraper")
    st.markdown("""
        This application scrapes restaurant information from GrabFood for specified locations.
        Enter the locations and click on 'Scrape' to get the data.
    """)

    locations_input = st.text_area("Enter locations (one per line)", "")
    if st.button("Scrape"):
        locations = [location.strip() for location in locations_input.split('\n') if location.strip()]
        if locations:
            base_url = "https://food.grab.com/sg/en"
            scraper = GrabFoodScraper(base_url=base_url, locations=locations)
            with st.spinner("Scraping..."):
                scraper.run()
            st.success("Scraping completed. Data saved to 'restaurants.ndjson.gz'.")
        else:
            st.error("Please enter at least one location.")

if __name__ == "__main__":
    main()
