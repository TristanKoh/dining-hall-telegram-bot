from re import findall
import requests
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}

r = requests.get("https://studentlife.yale-nus.edu.sg/dining-experience/daily-dining-menu/", headers = headers)

soup = BeautifulSoup(r.text, "html.parser")

# This finds the name of the first meal, if brunch, then list index only has 2.
meal_names = soup.find("div", {"class" : "menu-list"}).find("h4").text
meal_names

meals = soup.find("div", {"id" : "tab1"}).findAll(class_ = "menu-list")
stations = meals[0].findAll("u")
dishes = meals[0].findAll("p")

stations
dishes


def formatMenu(day) :
    """ 
    Accepts a int day (day of week) (ie. 1 for mon, 2 for tues etc)
    Queries the dining hall page and returns a formatted string for bot to use to reply 
    """

    # Get the html from the webpage
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}
    r = requests.get("https://studentlife.yale-nus.edu.sg/dining-experience/daily-dining-menu/", headers = headers)
    soup = BeautifulSoup(r.text, "html.parser")

    day_to_tab_dict = {1 : "tab1", 2 : "tab2", 3 : "tab3", 4 : "tab4", 5 : "tab5", 6 : "tab6", 7 : "tab7"}

    menu = ""
    meals = soup.find("div", {"id" : day_to_tab_dict[day]}).findAll(class_ = "menu-list")

    # If day is not weekend (ie the name of first meal is not brunch)
    first_meal_name = meals[0].find("h4").text
    
    if first_meal_name != "brunch" :

        # Loop through breakfast, lunch & dinner
        for index in range(3) :
            # Bold the meal text
            menu = menu + "<b>" + meals[index].find("h4").get_text() + "</b>" + "\n"
            
            # Find the stations (ie. salad bar, yakimix etc.) and the dishes (ie. kung pao chicken etc)
            stations = meals[index].findAll("u")
            dishes = meals[index].findAll("p")

            # Convert to text 
            stations = [station.get_text() for station in stations]
            dishes = [dish.get_text() for dish in dishes]
            print(stations)
            print(dishes)

            # Format the dishes
            for dish in dishes :

                # If dish is station name, print dish text with underline
                if dish in stations :
                    menu = menu + "<u>" + dish + "</u>" + "\n"
                
                else :
                    menu = menu + dish + "\n"
            
            # Add new lines to separate the meals from another
            menu = menu + "\n" + "\n"
        
        return menu
    

    else :
        for index in range(2) :

            menu = menu + "<b>" + meals[index].find("h4").get_text() + "</b>" + "\n"
            
            stations = meals[index].findAll("strong")
            dishes = meals[index].findAll("td")

            stations = [station.get_text() for station in stations]
            dishes = [dish.get_text() for dish in dishes]

            for dish in dishes :

                if dish in stations :
                    menu = menu + "<u>" + dish + "</u>" + "\n"
                
                else :
                    menu = menu + dish + "\n"
            
            menu = menu + "\n" + "\n"
        
        return menu


monday = formatMenu(1)

monday