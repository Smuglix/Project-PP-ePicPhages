import streamlit as st
import dbbact_api_call
from dbbact_api_call import find_human_associated_bacteria, compare_phage

# Set up your UI with Streamlit
st.title("PhagePhriend: Bacteriophage Cocktail Selector")
st.subheader("We gotchu to bust those nasty bacteria, without harming the good ones (⌐■_■)")

find_human_associated_bacteria()

# Let users input the bacteria they want to get rid of
bacteria_input = st.text_input("What bacteria do you want to get rid of? (Separate names with commas)")

if st.button("Find Phage Cocktail"):
    try:
        bacteria_list = [b.strip() for b in bacteria_input.split(",")]
        phage_cocktail = compare_phage(bacteria_list)
        combined_cocktail = set()

        for bacteria, phage_result in phage_cocktail.items():
            filtered = phage_result['filtered']
            less_filtered = phage_result['less_filtered']
            if filtered:
                combined_cocktail.update(filtered)
            elif less_filtered:
                combined_cocktail.update(less_filtered)

        if combined_cocktail:
            with st.expander("Final Combined Phage Cocktail:"):
                st.write(', '.join(combined_cocktail))
        else:
            st.error("We tried our best, man, but we just can't find any phages for these bacteria. (ಥ﹏ಥ)")

        for bacteria, phage_result in phage_cocktail.items():
            filtered = phage_result['filtered']
            less_filtered = phage_result['less_filtered']
            if filtered:
                with st.expander(f"Filtered phage cocktail for {bacteria}:"):
                    st.write(', '.join(filtered))
            elif less_filtered:
                with st.expander(
                        f"Not filtered phage cocktail for {bacteria} because we couldn't find phages that doesn't hurt the good ones ¯\_(ツ)_/¯ (remember, these may affect other bacteria as well):"):
                    st.write(', '.join(less_filtered))

    except Exception as e:
        st.error(
            f"Damn, didn't find these bacteria you gave me, make sure you wrote them the right way `(*>﹏<*)′: {e}")
