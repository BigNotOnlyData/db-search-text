import requests
import pandas as pd
import streamlit as st

from config import Tabs, API_URL


def get_response_from_api(tab: Tabs, output, **kwargs) -> requests.Response | None:
    """
    Отправляет запрос к API
    :param tab: название вкладки
    :param output: блок контейнера (st.empty()) для вывода информации в случае ошибок
    :param kwargs: параметры запроса
    :return: ответ от API  или None в случае ошибки запроса
    """
    try:
        match tab:
            case Tabs.search:
                response = requests.get(url=API_URL, **kwargs)
            case Tabs.create:
                response = requests.post(url=API_URL, **kwargs)
            case Tabs.update:
                response = requests.put(url=API_URL, **kwargs)
            case Tabs.delete:
                post_id = kwargs.pop('post_id')
                response = requests.delete(url=f'{API_URL}/{post_id}', **kwargs)
            case _:
                raise ValueError("Вкладки не существует")

    except requests.exceptions.ConnectionError as e:
        output.error(f"Проблемы с подключением к API: {e}")
    except Exception as e:
        output.error(f"Ошибка: {e}")
    else:
        return response


def checking_response_status(tab: Tabs, response: requests.Response, output) -> None:
    """
    Показ результатов запроса в соответсвии с кодом статуса
    :param tab: название вкладки
    :param response: ответ от API
    :param output: блок контейнера (st.empty()) для вывода информации
    """
    # res = response.json()

    match response.status_code:
        case requests.codes.OK:
            display_success_result(tab=tab, response=response.json(), output=output)
        case requests.codes.NOT_FOUND | requests.codes.UNPROCESSABLE_ENTITY:
            output.warning(response.json()['detail'])
        case _:
            output.warning(response.text)


def display_success_result(tab: Tabs, response: dict, output):
    """
    Вывод информации в случае успешного запроса
    :param tab: название вкладки
    :param response: ответ от API
    :param output: блок контейнера (st.empty()) для вывода информации
    :return:
    """
    match tab:
        case Tabs.search:
            df = pd.DataFrame(response['response']).set_index('id')
            output.dataframe(df, use_container_width=True)
        case Tabs.create:
            with output.container():
                st.success('Успешно создана запись:')
                st.json(response)
        case Tabs.update:
            output.success(f"Запись с id={response['id']} обновлена")
        case Tabs.delete:
            output.success(f"Запись с id={response['id']} удалена")
        case _:
            raise ValueError("Вкладки не существует")


def run_request_processing(tab: Tabs, **kwargs):
    """
    Запускает процесс отправки запросов к API и обработки ответов

    :param tab: название вкладки
    :param kwargs: параметры для методов запросов 'requests'
    :return:
    """
    output = st.empty()
    response = get_response_from_api(tab=tab, output=output, **kwargs)

    if response is not None:
        checking_response_status(tab=tab, response=response, output=output)

