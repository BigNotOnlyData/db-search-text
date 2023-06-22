import streamlit as st

from tabs import tabs_interface


def main():
    st.set_page_config(
        page_title="PES",
        page_icon="🐶",
    )
    st.title('Поисковик по БД: PostgreSQL+ElasticSearch')
    tabs_interface()


if __name__ == "__main__":
    main()
