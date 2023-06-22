import streamlit as st


def create_form() -> bool:
    with st.form("create"):
        st.write("Создать запись в БД")
        st.text_area('text', key='create_text')
        st.text_input('rubrics', key='create_rubrics')
        submitted = st.form_submit_button("Создать")
        return submitted


def update_form() -> bool:
    with st.form("update"):
        st.write("Обновить запись в БД по id")
        st.number_input('id', min_value=1, key='update_id')
        st.text_area('text', key='update_text')
        st.text_input('rubrics', key='update_rubrics')
        submitted = st.form_submit_button("Обновить")
        return submitted


def delete_form() -> bool:
    with st.form("delete"):
        st.write("Удалить запись в БД по id")
        st.number_input('id', min_value=1, key='delete_id')
        submitted = st.form_submit_button("Удалить")
        return submitted
