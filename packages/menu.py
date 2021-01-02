import requests
from bs4 import BeautifulSoup
DH_LINK = "https://studentlife.yale-nus.edu.sg/dining-experience/daily-dining-menu/"


# Function to pull the menu and then format the menu for the day
# TODO: Ideally the bot should only pull once a week, but the parsing would be more difficult getting "today's" menu
# would require conversion from UTC to SGT, and a separate thread to query the time constantly

def formatMenu(day) :
    """ 
    Accepts a int day (day of week) (ie. 1 for mon, 2 for tues etc)
    Queries the dining hall page and returns a formatted string for bot to use to reply 
    """

    # Get the html from the webpage
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}
    r = requests.get(DH_LINK, headers = headers)
    soup = BeautifulSoup(r.text, "html.parser")

    day_to_tab_dict = {1 : "tab1", 2 : "tab2", 3 : "tab3", 4 : "tab4", 5 : "tab5", 6 : "tab6", 7 : "tab7"}

    menu = ""
    meals = soup.find("div", {"id" : day_to_tab_dict[day]}).findAll(class_ = "menu-list")

    # If day is not weekend
    if day != 6 and day != 7 :

        # Loop through breakfast, lunch & dinner
        for index in range(3) :
            # Bold the meal text
            menu = menu + "<b>" + meals[index].find("h4").get_text() + "</b>" + "\n"
            
            # Find the stations (ie. salad bar, yakimix etc.) and the dishes (ie. kung pao chicken etc)
            stations = meals[index].findAll("strong")
            dishes = meals[index].findAll("td")

            # Convert to text 
            stations = [station.get_text() for station in stations]
            dishes = [dish.get_text() for dish in dishes]

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


def formatMenu_Today() :
    """ 
    No arguments. Functionally same as the formatMenu function above.
    Queries the webpage, finds the active DH tab (which indicates that it is today's menu), 
    Pulls the text from that tab and formats it for the bot to reply
    """

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}
    r = requests.get(DH_LINK, headers = headers)
    soup = BeautifulSoup(r.text, "html.parser")

    today_tab = soup.find(class_ = "tabs dining").find(class_ =  "active").get("rel")

    # Extract fourth char of tab string (ie. tab4 returns 4), since that is the day of week
    day = int(today_tab[3])

    day_to_tab_dict = {1 : "tab1", 2 : "tab2", 3 : "tab3", 4 : "tab4", 5 : "tab5", 6 : "tab6", 7 : "tab7"}

    menu = ""
    meals = soup.find("div", {"id" : day_to_tab_dict[day]}).findAll(class_ = "menu-list")

    if day != 6 or day != 7 :

        for index in range(3) :

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