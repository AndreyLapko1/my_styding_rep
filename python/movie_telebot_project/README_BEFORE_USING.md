# movie_telebot
# 1. Description
### Telegram-bot to search for movies by: selected category, release year (mixed selection option = True).  Search by keyword. There is a view of the most popular queries, as well as the output of their number (search by the most popular queries = True)
## Archive: ```movie_telebot_project```
## Files: ```app.py```, ```database.py```, ```images.py```, ```movie_telebot.py```    





## ```app.py``` - Application file. Processing requests and outputting information to a telegram bot  
```def display``` - function of outputting information for users in the form of telegram-buttons  
```def show_film_info``` - function to display information about the selected movie.  Takes the result from the search_info function of the database.py file  
```def search_by_keyword``` - keyword search function.  Takes the result from the search_by_keyword function of the database.py file  
```def search_by_category_year``` - Search function by year and by category. Takes the result from the show_categories or search_by_category_year function from database.py  
```def search_only_by_ctg ``` - Search function by category only. Accepts the result from the show_categories function  
```def search_by_year``` - Year search function with the ability to mix with category search. Takes the result from the search_by_year function from database.py  
```def out_common``` - A function showing the 5 most popular queries  
```def most_common_queries``` - Function that gets the result of popular queries sampling from the show_most_common from database.py function

## ```database.py``` - Database file.Processing movie searches and most popular queries  
```class QueryDatabaseWrite``` - Class of write database  
```def tracker``` - Function for tracking queries and recording them in the database  
```def show_most_common``` - A function that searches for 5 popular queries in the database  
```def close``` - Function for closing the connection

## ```images.py``` - A file with a dictionary
```genre_images``` - A dictionary that contains paths to photos categorized by movie category

## ```movie_telebot.py``` - file of user interaction with telegram-bot. Button presses processing file
```def start_message``` - Function to start interaction with the bot after sending the ```/start``` command. Shows the main menu of action selection  
```def close_resources``` - Function to close all connections when the ```Выход``` key is pressed. Calls the function of closing connections (database.py)  
```def callback_inline``` - Function for handling main and side menu button presses  
```def handle_year``` - Year tracking function (entered from the keyboard) to search by year
```def handle_keyword``` - Keyword tracking function (entered from the keyboard) for keyword search


# 2. Start-up instructions

### Step 1.
From the ```movie_telebot_project``` folder extract the img folder. Place it on the desktop
### Step 2.
Create an .env file with the following parameters:  
```host=```host to sakila database  
```user=```bd_user  
```password=```bd_password  
```database=```bd_sakila  
```host_write=```host to edit database  
```user_write=```bd_user  
```password_write=```bd_password  
```database_write=```290724-ptm_fd_Andrey_Lapko   
```token```=bot's token
### Step 3.
Run the ```movie_telebot.py``` file
### Step 4.
Go to telegram and search for ```MovieSearchBot```.  
```@searchmooviebot```
### Step 5.  
Send ```MovieSearchBot``` the command ```/start```






