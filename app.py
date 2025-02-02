import streamlit as st
from datetime import datetime, timedelta

def calculate_days_in_country(repatriation_date, absence_dates):
    today = datetime.today().date()
    repatriation_date = datetime.strptime(repatriation_date, "%Y-%m-%d").date()
    
    # Считаем количество дней в стране за последние 5 лет
    five_years_ago = max(repatriation_date, today - timedelta(days=5*365))
    total_days = (today - five_years_ago).days
    
    # Вычитаем дни отсутствия в последние 5 лет
    days_absent = 0
    for absence_start, absence_end in absence_dates:
        absence_start = datetime.strptime(absence_start, "%Y-%m-%d").date()
        absence_end = datetime.strptime(absence_end, "%Y-%m-%d").date()
        
        if absence_end >= five_years_ago:
            effective_start = max(absence_start, five_years_ago)
            days_absent += (absence_end - effective_start).days
    
    days_present = total_days - days_absent
    return days_present, total_days

def determine_passport_eligibility(days_present, total_days, repatriation_date):
    years_since_repatriation = (datetime.today().date() - repatriation_date).days / 365
    
    if years_since_repatriation < 1:
        return "❌ Только 'теудат маавар' на 5 лет"
    
    percentage_present = days_present / total_days if total_days > 0 else 0
    
    if 1 <= years_since_repatriation < 5:
        if percentage_present >= 0.6:
            return "✅ Даркон на 5 лет"
        else:
            return "❌ Только 'теудат маавар' на 5 лет"
    
    if years_since_repatriation >= 5:
        if days_present >= 36 * 30:  # 36 месяцев (приблизительно)
            return "✅ Даркон на 10 лет"
        elif (datetime.today().date() - timedelta(days=365)) >= repatriation_date and (days_present / 365) >= 0.6:
            return "✅ Даркон на 5 лет (по исключению)"
        else:
            return "❌ Только 'теудат маавар' на 5 лет"
    
    return "❌ Нет данных для расчета"

# Интерфейс Streamlit
st.title("Калькулятор права на загранпаспорт Израиля 🇮🇱")

# Ввод даты репатриации
repatriation_date = st.date_input("Введите дату репатриации", min_value=datetime(2000, 1, 1))

# Ввод дат отсутствия за последние 5 лет
st.subheader("Введите даты отсутствия в стране за последние 5 лет")
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

# Расчет дней в стране и определение типа паспорта
if st.button("Рассчитать"):
    days_in_country, total_days = calculate_days_in_country(str(repatriation_date), st.session_state.absences)
    eligibility = determine_passport_eligibility(days_in_country, total_days, repatriation_date)
    
    st.success(f"📅 Вы находились в стране: **{days_in_country} дней из {total_days}**")
    st.info(f"📜 Ваш статус: {eligibility}")
