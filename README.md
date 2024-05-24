# GrabFood Scraper

This project is a web scraper for GrabFood that extracts restaurant information for specified locations. The scraper is built using Selenium, BeautifulSoup, and other Python libraries. Additionally, a Streamlit application is provided to interact with the scraper through a user-friendly interface.

## Features

- Scrapes restaurant details such as name, cuisine, rating, delivery time, distance, promotional offers, and more.
- Saves the scraped data in a compressed NDJSON format.
- Uses multithreading to scrape multiple locations concurrently.
- Provides a Streamlit application for easy interaction.

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/grabfood-scraper.git
    cd grabfood-scraper
    ```

2. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Download ChromeDriver:**

    The scraper uses Selenium with ChromeDriver. The `webdriver-manager` package will handle the installation of ChromeDriver.

## Usage

### Running the Streamlit Application

1. **Create or update the `GrabFoodScraper.py` file:**

    Ensure that the `GrabFoodScraper` class is defined as shown in the provided script.

2. **Create the Streamlit app file:**

    Create a file named `streamlit_app.py` with the following content:

    ```python
    import streamlit as st
    from GrabFoodScraper import GrabFoodScraper

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
    ```

3. **Run the Streamlit application:**

    ```sh
    streamlit run streamlit_app.py
    ```

    This will open a new browser window where you can enter the locations and trigger the scraping process.

## Project Structure

