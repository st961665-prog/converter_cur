import streamlit as st
import requests
import os


st.set_page_config(page_title="Конвертер Валют", page_icon="💱")

st.title("Конвертер Валют")
st.write("Узнайте актуальный курс валют в реальном времени.")

 
BASE_URL = "https://api.frankfurter.app"

@st.cache_data
def get_supported_currencies():
    try:
        response = requests.get(f"{BASE_URL}/currencies", timeout=5)
        if response.status_code == 200:
            return response.json() # Возвращает словарь {код: название}
        return {}
    except Exception as e:
        st.error(f"Ошибка: {e}")
        return {}

def get_exchange_rate(from_currency, to_currency):
    try:
        url = f"{BASE_URL}/latest"
        params = {"from": from_currency, "to": to_currency}
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            # Структура: {'rates': {'EUR': 0.92}, ...}
            rates = data.get('rates', {})
            if to_currency in rates:
                return rates[to_currency]
        return None
    except Exception as e:
        st.error(f"Ошибка: {e}")
        return None

currencies_dict = get_supported_currencies()

if currencies_dict:
    currency_codes = list(currencies_dict.keys())
    
    col1, col2 = st.columns(2)
    
    with col1:
        from_currency = st.selectbox(
            "Из валюты:",
            currency_codes,
            index=currency_codes.index("RUB") if "RUB" in currency_codes else 0
        )

    with col2:
        to_currency = st.selectbox(
            "В валюту:",
            currency_codes,
            index=currency_codes.index("USD") if "USD" in currency_codes else 1
        )

    st.divider()

    if st.button("Рассчитать курс"):
        if from_currency == to_currency:
            st.info(f"Курс {from_currency} к {from_currency} всегда равен 1.0")
        else:
            with st.spinner('Загрузка актуальных данных...'):
                rate = get_exchange_rate(from_currency, to_currency)
                
                if rate is not None:
                    st.success("Курс получен успешно!")
                    
                    st.markdown(f"""
                    ### 💱 Результат
                    **1 {from_currency}** = **{rate:,.4f} {to_currency}**
                    """)
                    
                    inverse_rate = 1 / rate
                    st.caption(f"*(Обратный курс: 1 {to_currency} ≈ {inverse_rate:,.4f} {from_currency})*")
                else:
                    st.error("Не удалось получить курс. Проверьте ключ API или соединение с интернетом.")
else:
    st.error("Не удалось загрузить список валют. Проверьте ваш API ключ и подключение к интернету.")
    st.warning("Убедитесь, что вы установили переменную окружения EXCHANGE_RATE_API_KEY или вставили ключ в код.")

st.markdown("---")
st.caption("Данные предоставлены сервисом Frankfurter-API")