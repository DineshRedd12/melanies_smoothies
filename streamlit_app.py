# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(":balloon: Customize Your Smoothie! :balloon: ")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)
name_on_order = st.text_input("Name On Smoothie:")
st.write("The name on you smoothie will be:",name_on_order)
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

options = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5
)

st.write("You selected:", options)
ingredients_list=st.multiselect('choose up to 5 ingredients:',my_dataframe)
if ingredients_list:
    
    ingredients_string =''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+''
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
import requests
if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen+''
        st.subheader(fruit_chosen +'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
