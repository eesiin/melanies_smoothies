# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())  # .json() to display readable response

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw: {st.__version__}")
st.write("""Choose the fruits you want in your custom Smoothie!""")

title = st.text_input("Name on Smoothie", "")
st.write("The name on your Smoothie will be ", title)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect('Choose up to 5 ingredients :', my_dataframe,
                                   max_selections=5)

if ingredients_list:
    ingredients_string = ''
    name_on_order = title

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered for ' + title + '!', icon="✅")
