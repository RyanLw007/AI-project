import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Install chromedriver
chromedriver_autoinstaller.install()

def build_url(journey_type, origin, dest, lor, date, time=None, return_date=None, return_time=None, return_lor=None, adults=1, extra_time=0):
    base_url = "https://www.nationalrail.co.uk/journey-planner/"
    url = f"{base_url}?type={journey_type}&origin={origin}&destination={dest}&leavingType={lor}&leavingDate={date}&adults={adults}&extraTime={extra_time}"
    if time:
        url += f"&leavingHour={time[:2]}&leavingMin={time[2:]}"
    if journey_type == "return" and return_date and return_time and return_lor:
        url += f"&returnType={return_lor}&returnDate={return_date}&returnHour={return_time[:2]}&returnMin={return_time[2:]}"
    return url + "#O"

def scrape_prices(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    prices = []
    try:
        wait = WebDriverWait(driver, 28)
        wait.until(EC.visibility_of_element_located((By.ID, "main-content")))

        main_section = driver.find_element(By.ID, "main-content")
        sections = main_section.find_elements(By.TAG_NAME, "section")

        for section in sections:
            list_items = section.find_elements(By.TAG_NAME, "li")
            for item in list_items:
                try:
                    button = item.find_element(By.XPATH, ".//button[contains(@id, 'result-card-selection-outward-')]")
                    price_span = button.find_element(By.XPATH, ".//span[@class='styled__StyledCalculatedFare-sc-1gozmfn-2 goNENa']")
                    price = price_span.text.strip('£')
                    prices.append(float(price))
                except Exception:
                    continue

        return prices
    except Exception:
        return []
    finally:
        driver.quit()

def find_lowest_price(prices):
    return min(prices) if prices else None

def format_date_url(date):
    year, month, day = date.split("-")
    return day + month + year[2:]

def format_time_url(time):
    return time.replace(":", "")

def lor_formatting(lor):
    return "departing" if lor == "leave" else "arriving"

def one_way(origin, dest, date, time, lor, adults=1, extra_time=0):
    url = build_url("single", origin, dest, lor_formatting(lor), format_date_url(date), format_time_url(time), adults=adults, extra_time=extra_time)
    prices = scrape_prices(url)
    return find_lowest_price(prices), url

def open_ticket(origin, dest, date, lor="departing", adults=1, extra_time=0):
    url = build_url("single", origin, dest, lor_formatting(lor), format_date_url(date), "1200", adults=adults, extra_time=extra_time)
    prices = scrape_prices(url)
    return find_lowest_price(prices), url

def open_return(origin, dest, leave_date, return_date, lor="departing", return_lor="departing", adults=1, extra_time=0):
    url = build_url("return", origin, dest, lor_formatting(lor), format_date_url(leave_date), "1200", format_date_url(return_date), "1200", lor_formatting(return_lor), adults=adults, extra_time=extra_time)
    prices = scrape_prices(url)
    return find_lowest_price(prices), url

def round_trip(origin, dest, leave_date, leave_time, return_date, return_time, lor, return_lor, adults=1, extra_time=0):
    url = build_url("return", origin, dest, lor_formatting(lor), format_date_url(leave_date), format_time_url(leave_time), format_date_url(return_date), format_time_url(return_time), lor_formatting(return_lor), adults=adults, extra_time=extra_time)
    prices = scrape_prices(url)
    return find_lowest_price(prices), url


# Example usage
if __name__ == "__main__":
    # print("One way journey price:", one_way("NRW", "LST", "2024-06-06", "12:15", "leave", 1, 0))
    # print("Open ticket journey price:", open_ticket("NRW", "LST", "2024-06-06", "leave", 1, 0))
    # print("Open return journey price:", open_return("NRW", "LST", "2024-06-06", "2024-06-10", "leave", "leave", 1, 0))
    # print("Round trip journey price:", round_trip("NRW", "LST", "2024-06-06", "12:15", "2024-06-10", "10:30", "leave", "leave", 1, 0))

    one = one_way("NRW","LST","2024-06-06","12:00","leave")
    print(one)
    two = one_way("CBG", "PMS", "2024-06-06", "13:00", "leave")
    print(two)
    three = one_way("NRW", "CBG", "2024-06-05", "14:00", "leave")
    print(three)

    six = round_trip("CBG", "PMS", "2024-06-04", "14:00", "2024-06-06", "14:00", "leave", "leave")
    print(six)
    seven = round_trip("NRW", "PMS", "2024-06-04", "14:00", "2024-06-06", "16:00", "leave", "leave")
    print(seven)
    eight = round_trip("CBG", "NRW", "2024-06-04", "14:00", "2024-06-06", "14:00", "leave", "leave")
    print(eight)

    eleven = one_way("PMS", "NRW", "2024-06-07", "10:00", "leave")
    print(eleven)
    twelve = one_way("NRW", "CBG", "2024-06-08", "09:00", "leave")
    print(twelve)
 
    seventeen = round_trip("CBG", "PMS", "2024-06-14", "07:00", "2024-06-15", "17:00", "leave", "leave")
    print(seventeen)
    eighteen = round_trip("NRW", "CBG", "2024-06-16", "14:00", "2024-06-17", "14:00", "leave", "leave")
    print(eighteen)




