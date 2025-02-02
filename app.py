import streamlit as st
from datetime import datetime, timedelta

# Функция для расчета дней в стране
def calculate_days_in_country(repatriation_date, absence_dates):
    today = datetime.today().date()
    repatriation_date = datetime.strptime(repatriation_date, "%Y-%m-%d").date()

    # Считаем общее количество дней
    total_days = (today - repatriation_date).days

    # Вычитаем дни отсутствия
    for absence in absence_dates:
        absence_start = datetime.strptime(absence[0], "%Y-%m-%d").date()
        absence_end = datetime.strptime(absence[1], "%Y-%m-%d").date()
        total_days -= (absence_end - absence_start).days

    return total_days

# Интерфейс Streamlit
st.title("Калькулятор дней в стране 🇮🇱")

# Ввод даты репатриации
repatriation_date = st.date_input("Введите дату репатриации", min_value=datetime(2000, 1, 1))

# Ввод дат отсутствия
absence_dates = []
st.subheader("Введите даты отсутствия в стране")
if "absences" not in st.session_state:
    st.session_state.absences = []

# Форма для ввода периодов отсутствия
col1, col2, col3 = st.columns(3)
with col1:
    absence_start = st.date_input("Начало отсутствия", key="absence_start")
with col2:
    absence_end = st.date_input("Конец отсутствия", key="absence_end")
with col3:
    if st.button("Добавить период"):
        if absence_start < absence_end:
            st.session_state.absences.append((str(absence_start), str(absence_end)))

# Вывод списка периодов отсутствия
if st.session_state.absences:
    st.write("Периоды отсутствия:")
    for i, (start, end) in enumerate(st.session_state.absences):
        st.write(f"{i+1}. {start} - {end}")

    if st.button("Очистить периоды"):
        st.session_state.absences = []

# Расчет дней в стране
if st.button("Рассчитать"):
    days_in_country = calculate_days_in_country(str(repatriation_date), st.session_state.absences)
    passport_date = repatriation_date + timedelta(days=5*365)

    st.success(f"📅 Вы находитесь в стране: **{days_in_country} дней**")
    st.info(f"📜 Предполагаемая дата получения паспорта: **{passport_date.strftime('%Y-%m-%d')}**")
