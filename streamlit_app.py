from urllib.error import URLError

import pandas
import requests
import snowflake.connector
import streamlit

my_fruit_list = pandas.read_csv(
    "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
)
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌 🥭 Build Your Own Fruit Smoothie 🥝 🍇')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect(
    "Pick some fruits:",
    list(my_fruit_list.index),
    ['Banana', 'Strawberries']
)
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice!')


def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get(
        f"https://fruityvice.com/api/fruit/{fruit_choice}"
    )
    fruityvice_normalized = pandas.json_normalize(
        fruityvice_response.json()
    )
    return fruityvice_normalized


try:
    fruit_choice = streamlit.text_input(
        'What fruit would you like information about?'
    )
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        selected_fruit_choice_info = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(selected_fruit_choice_info)

except URLError as error:
    streamlit.error()

streamlit.header("The fruit load list contains")


def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
        return my_cur.fetchall()


if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)


def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute(f"INSERT INTO FRUIT_LOAD_LIST VALUES ('{new_fruit}')")
    return 'Thanks for adding ' + new_fruit


add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add Fruit to List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    result = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(result)
