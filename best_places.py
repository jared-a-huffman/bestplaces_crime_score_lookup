from pyzipcode import ZipCodeDatabase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def main():
    while True:
        zip_code = zipcode_request()
        result = city_state_lookup(zip_code)
        if result:
            break
    city, state = result
    city = city.replace(" ", "_")
    state = STATE_ABBREVIATIONS[state]

    url = f"https://www.bestplaces.net/crime/zip-code/{state}/{city.lower()}/{zip_code}"
    while True:
        crime_score = pull_crime_score(url)
        if crime_score:
            break
    clean_score = crime_score_cleanup(crime_score)
    for score in clean_score:
        print(score)


def crime_score_cleanup(crime_score):
    clean_score = []
    for i in crime_score:
        new = i.split("(T")
        clean_score.append(new[0])
    return clean_score


def pull_crime_score(url):
    try:
        driver = webdriver.Chrome()
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "violent crime")
        )

        h5_elements = driver.find_elements(By.TAG_NAME, "h5")
        crime_score = []
        for h5 in h5_elements:
            if (
                "violent crime" in h5.text.lower()
                or "property crime" in h5.text.lower()
            ):
                crime_score.append(h5.text)
        driver.quit()
        return crime_score
    except TimeoutException:
        driver.quit()
        return False


def zipcode_request():
    while True:
        zip_code = input("Zip Code: ")
        if zip_code.isdigit() and len(zip_code) == 5:
            return zip_code
        else:
            print("Incorrect zip code format.")


def city_state_lookup(zip_code):
    try:
        zcdb = ZipCodeDatabase()
        result = zcdb[zip_code]
        city = result.city
        state = result.state
    except KeyError:
        print("The zip code you entered could not be found")
        return False

    return city, state


STATE_ABBREVIATIONS = {
    "AL": "alabama",
    "AK": "alaska",
    "AZ": "arizona",
    "AR": "arkansas",
    "CA": "california",
    "CO": "colorado",
    "CT": "connecticut",
    "DE": "delaware",
    "FL": "florida",
    "GA": "georgia",
    "HI": "hawaii",
    "ID": "idaho",
    "IL": "illinois",
    "IN": "indiana",
    "IA": "iowa",
    "KS": "kansas",
    "KY": "kentucky",
    "LA": "louisiana",
    "ME": "maine",
    "MD": "maryland",
    "MA": "massachusetts",
    "MI": "michigan",
    "MN": "minnesota",
    "MS": "mississippi",
    "MO": "missouri",
    "MT": "montana",
    "NE": "nebraska",
    "NV": "nevada",
    "NH": "new_hampshire",
    "NJ": "new_jersey",
    "NM": "new_mexico",
    "NY": "new_york",
    "NC": "north_carolina",
    "ND": "north_dakota",
    "OH": "ohio",
    "OK": "oklahoma",
    "OR": "oregon",
    "PA": "pennsylvania",
    "RI": "rhode_island",
    "SC": "south_carolina",
    "SD": "south_dakota",
    "TN": "tennessee",
    "TX": "texas",
    "UT": "utah",
    "VT": "vermont",
    "VA": "virginia",
    "WA": "washington",
    "WV": "west_virginia",
    "WI": "wisconsin",
    "WY": "wyoming",
}


main()
