import streamlit as st


st.set_page_config(
    page_title = "Password-Checker",
    page_icon = "📚"
)

with st.sidebar:
    st.write("")

st.title("Password-Checker 📚")
st.subheader("How does it work? 🤔", divider="blue")

markdown_text = """
This project aimed to create a site that selects elements of a password and checks its strength using AI and a library created for this purpose.

On the site you can see two pages:
- **About** 📚 - a current page with a greeting and summary instructions on how the site works
- **Password** 🔒 - a site where all you have to do is enter your password and AI will do the job 😏

**Good Luck And Enjoy 😀**
"""

st.markdown(markdown_text)
