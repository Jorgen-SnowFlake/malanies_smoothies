# Import python packages
import streamlit as st
streamlit.title('My Parents New Healthy Diner')
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)


# neu 08.05.2025, Box für Name der bestellung
# import streamlit as st
#title = st.text_input('Movie title', 'Life of Brian')
#st.write('The current movie title is', title)
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)
# neu 08.05.2025, Box für Name der Bestellung


cnx = st.connection("snowflake") 
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)    
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

# 2025-04-25
# Build a SQL Insert Statement & Test It
 
my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_string + """', '"""+name_on_order+ """')"""

#st.write(my_insert_stmt)
#st.stop()
# Add a Submit Button
time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()

    st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")


# Insert the Order into Snowflake
# if ingredients_string:
#     session.sql(my_insert_stmt).collect()
 #    st.success('Your Smoothie is ordered!', icon="✅")
