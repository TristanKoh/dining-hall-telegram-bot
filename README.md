# Dining Hall menu scraper using telegram bot 

## Objective
Yale NUS College used to have a dining hall menu (https://www.yale-nus.edu.sg/college-life/overview/residential-life/dining-experience/) which was updated at the end of every week, and categorised by day and by meal (breakfast, lunch, dinner).

As a student who had compulsory opt-in to the meal plan, there were days which we were tired of the dining hall options and would prefer to dine at the nearby food court at UTown. I found that it was quite troublesome to use the browser to check the menu options everytime. Instead, I thought it would be more efficient to use telegram as a front end (which was widely used by almost every student for their personal messaging), and on the back end, a python script would scrape the website, and pull the menu for the specific day which the user requested.

## Set up of app
The Telgram chatbot API was used as the front end for students to input commands by the day of the week. The backend was a python script that scraped the menu from the website on demand. The script was deployed on Heroku.

The main script can be found in __dining-hall-bot.py__, and the helper packages used for formatting and scraping can be found under __/packages__.

## Results
For instance, the user could use the command /today, and the bot will automatically pull the menu in telegram the chat window:

User:

/today

Telegram bot:

__breakfast__

*Salad: Selection of Salads and Dressings*

Whole Apples, Oranges or Bananas

Mixed Salad Bowl with Thousand Island

and Sherry Vinegar Dressing

*Healthy Snacks*

Cereals and Yogurts

Packet of Milk or Soya Milk

*Danish Counter*

Raisin Buns (G,E,D,V)

*Yakimix/ Euro American*

Waffle (G,E,D,V)

Chicken Frank (G,S)

Mediterranean Bean Stew (VE,S)

*Spices (HALAL)*

Steamed Carrot Cake (VE,G)

Braised Hard Boiled Egg (V,E)

Tau Sar Pau (VE,G)

*Non Vegan*

Waffle with Butter Chicken, Sausages Chipolata (E,G,D)

Scrambled Egg

*Vegan*

Sliced Banana and Nutella Spread on Wholemeal Bread (N,E,G,D)

Lettuce Salad with Lime Dressing

Cream Buns (G,E,D,V)

Strawberry Yogurt Cup (D)

Corn Rice (V,D)

Fish Kicap (S)

Sambal Taukwa (VE,S)

Stir-Fried Bayam w Carrot (VE,G,S)

Packet Milk & Soya Milk

Whole Fruit

Whole Dates


__lunch__

*Soup*

White Radish (VE)

*Salad Bar*

Whole Apples, Oranges or Bananas

Mixed Salad Bowl with Thousand Island

and Sherry Vinegar Dressing

*Yakimix/ Euro American*

Baked Chicken with Relish and Pineapple (G,S)

Sautéed Chickpeas with Onion (VE)

Chilli Kang Kong (VE,G,S)

Steamed Brinjal with Long Bean (VE)

*Spices (HALAL)*

Ikan Masak Kuah Kuning

Sambal Tau Kwa (VE,S)

Stir-Fried Bayam with Carrot (VE,G,S)

Boiled Lady Finger with Fried Garlic (VE)

*Dessert*

Hot Barley (VE)

Whole Fruits

*Drinks*

Infused Water

*Non Vegan*

Chicken Ham, Cheddar Cheese, Tomato Sauce, Pizza Bread (E,G,D)

on French Loaf Lettuce Salad with Lime Dressing

*Vegan*

Penne Pasta on Bowl, Kidney Bean, Cherry Tomato (VE,G)

Alfalfa Sprouts


__dinner__

*Soup*

Kimchi Soup (VE)

*Salad Bar*

Whole Apples, Oranges or Bananas

Mixed Salad Bowl with Thousand Island

and Sherry Vinegar Dressing

*Yakimix/ Euro American*

Roasted Chicken with Parmesan Cheese (D)

Mixed Bean with Pronto Sauce (VE)

Mixed Grilled Carrot (VE)

Sautéed Red Cabbage with Onion (VE)

*Spices (HALAL)*

Fish Korma (D)

Boiled Potato with Dry Chilli  (VE)

Sautéed Mixed Vegetables (VE)

Marrow with Cumin Seed (VE)

*Dessert*

Cut Fruits (VE)

Whole Fruits

*Drinks*

Cordial Drink
