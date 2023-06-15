import streamlit as st
import dbbact_api_call
from dbbact_api_call import find_human_associated_bacteria, compare_phage

# Set up your UI with Streamlit
st.title("PhagePhriend: Bacteriophage Cocktail Selector")
st.subheader("We gotchu to bust those nasty bacteria, without harming the good ones (⌐■_■)")

# Let users input the bacteria they want to get rid of
bacteria_input = st.text_input("What bacteria do you want to get rid of? (Separate names with commas)")

if st.button("Find Phage Cocktail"):
    # Call your functions just like in your main.py
    find_human_associated_bacteria()

    try:
        bacteria_list = [b.strip() for b in bacteria_input.split(",")]
        phage_cocktail = compare_phage(bacteria_list)  # Modify compare_phage() in dbbact_api_call.py to accept the bacteria_list as a parameter
        st.success(f"Here's your phage cocktail, my dude: {phage_cocktail}")

    except Exception as e:
        st.error(f"Damn, didn't find these bacteria you gave me, make sure you wrote them the right way, you dumbass: {e}")