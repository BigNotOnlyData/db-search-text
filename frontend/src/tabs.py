
import streamlit as st

import forms
from api import run_request_processing
from config import Tabs


def tabs_interface():
    for tab, name in zip(st.tabs(Tabs), Tabs):
        with tab:
            match name:
                case Tabs.search:
                    tab_search(name)
                case Tabs.create:
                    tab_create(name)
                case Tabs.update:
                    tab_update(name)
                case Tabs.delete:
                    tab_delete(name)
                case _:
                    pass


def tab_search(tab: Tabs):
    query = st.text_input('Поисковой запрос').strip()

    if query:
        with st.spinner(f'Поиск "{query}"'):
            run_request_processing(tab=tab,
                                   params={'q': query})


def tab_create(tab: Tabs):
    with st.expander(':arrow_down:'):
        st.write('*id* и *created_date* создаются автоматически')

    if forms.create_form():
        with st.spinner(f'Создание...'):
            run_request_processing(tab=tab,
                                   json={'text': st.session_state.create_text,
                                         'rubrics': st.session_state.create_rubrics})


def tab_update(tab: Tabs):
    if forms.update_form():
        with st.spinner(f'Обновление...'):
            run_request_processing(tab=tab,
                                   json={'id': st.session_state.update_id,
                                         'text': st.session_state.update_text,
                                         'rubrics': st.session_state.update_rubrics,
                                         })


def tab_delete(tab: Tabs):
    if forms.delete_form():
        with st.spinner(f'Удаление...'):
            run_request_processing(tab=tab,
                                   post_id=st.session_state.delete_id)
