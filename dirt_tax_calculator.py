import tkinter as tk
from tkinter import ttk
from datetime import datetime
from dateutil import relativedelta


def calculate_tax(cadastral_value, registration_date, termination_date, taxpayer_category_value, land_type_value, assignment_value):
    registration_date = datetime.strptime(registration_date, '%Y-%m-%d')
    termination_date = datetime.strptime(termination_date, '%Y-%m-%d')

    difference = relativedelta.relativedelta(registration_date, termination_date)
    month_total = difference.years * 12 + difference.months
    month_total = month_total - 1 if registration_date.day <= 15 else month_total

    avance_pay = [0, 0, 0]
    dirt_tax = 0

    if registration_date.day >= 15:
        if registration_date.month == 12:
            next_date = registration_date.replace(year=registration_date.year + 1, month=1, day=1)
        else:
            next_date = registration_date.replace(month=registration_date.month + 1, day=1)
    else:
        next_date = registration_date

    quarters = {
        'Q1': 0,
        'Q2': 0,
        'Q3': 0,
        'Q4': 0
    }

    while next_date <= termination_date:
        if next_date.month <= 3:
            quarters['Q1'] += 1
        elif next_date.month <= 6:
            quarters['Q2'] += 1
        elif next_date.month <= 9:
            quarters['Q3'] += 1

        if next_date.month == 12:
            next_date = next_date.replace(year=next_date.year + 1, month=1)
        else:
            next_date = next_date.replace(month=next_date.month + 1)

    avance_pay[0] = ((1 / 4) * cadastral_value * land_type_value * (quarters['Q1'] / 3) *
                     assignment_value * 1000000)
    avance_pay[1] = ((1 / 4) * cadastral_value * land_type_value * (quarters['Q2'] / 3) *
                     assignment_value * 1000000)
    avance_pay[2] = ((1 / 4) * cadastral_value * land_type_value * (quarters['Q3'] / 3) *
                     assignment_value * 1000000)

    if taxpayer_category_value == 0:
        dirt_tax = ((cadastral_value * land_type_value * (month_total / 12) * assignment_value * 1000000) - avance_pay[0]
                    - avance_pay[1] - avance_pay[2])
    else:
        avance_pay = [0, 0, 0]
        dirt_tax = cadastral_value * land_type_value * assignment_value * (month_total / 12) * 1000000

    return avance_pay, abs(dirt_tax)


def open_new_window():
    new_window = tk.Toplevel(root)
    new_window.geometry("200x200")
    new_window.title("...")

    registration_date = date_entry1.get()
    termination_date = date_entry2.get()

    cadastral_value = frac_entry1.get()
    taxpayer_category = select1.get()
    land_type = select2.get()
    assignment = select3.get()

    taxpayer_category_value = 0 if taxpayer_category == 'Никакая из нижеперечисленных' else \
        1 if taxpayer_category == 'Герой Советского Союза,Герой Российской Федераци' else \
            2 if taxpayer_category == 'Пенсионер или лицо достигших возраста 60 и 55 лет' else \
                3 if taxpayer_category == 'Ветеран или инвалид ВОВ' else \
                    4 if taxpayer_category == 'Физических лиц, имеющих трех и более несовершеннолетних детей.и т.д.' \
                        else taxpayer_category

    land_type_value = 0.015 if land_type == 'Прочих земельные участки' else \
        0.003 if land_type == 'Земли сельскохозяйственного назначения' else \
            0.003 if land_type == 'Занятых жилищным фондом и объектами инженерной инфраструктуры       ' else \
                0.003 if land_type == 'Земли для обеспечения обороны, безопасности и таможенных нужд' else \
                    land_type

    assignment_value = 2 if assignment == 'Жилищное строительство в течении 3 лет' else \
        1 if assignment == 'Жилищное строительство меньше 3 лет' else \
            4 if assignment == 'Жилищное строительство больше 3 лет' else \
                2 if assignment == 'Индивидуальное жилищное строительство 10 лет' else \
                    1 if assignment == 'Земельный участок' \
                        else assignment

    avance_pay, dirt_tax = calculate_tax(float(cadastral_value), str(registration_date), str(termination_date),
                                         int(taxpayer_category_value), float(land_type_value), int(assignment_value))

    avance_pay_label_q1 = tk.Label(new_window, text="Первый квартал")
    avance_pay_label_q1.pack()
    avance_pay_entry_q1 = tk.Entry(new_window)
    avance_pay_entry_q1.insert(0, avance_pay[0])
    avance_pay_entry_q1.pack()

    avance_pay_label_q2 = tk.Label(new_window, text="Второй квартал")
    avance_pay_label_q2.pack()
    avance_pay_entry_q2 = tk.Entry(new_window)
    avance_pay_entry_q2.insert(0, avance_pay[1])
    avance_pay_entry_q2.pack()

    avance_pay_label_q3 = tk.Label(new_window, text="Третий квартал")
    avance_pay_label_q3.pack()
    avance_pay_entry_q3 = tk.Entry(new_window)
    avance_pay_entry_q3.insert(0, avance_pay[2])
    avance_pay_entry_q3.pack()

    dirt_tax_label = tk.Label(new_window, text="Сумма налога:")
    dirt_tax_label.pack()
    dirt_tax_entry = tk.Entry(new_window)
    dirt_tax_entry.insert(0, dirt_tax)
    dirt_tax_entry.pack()


root = tk.Tk()
root.geometry("700x300")
root.title("Калькулятор земельног налога")

frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor='center')

date_label1 = tk.Label(frame, text="Дата начала учета (yyyy-mm-dd):")
date_entry1 = tk.Entry(frame)
date_label2 = tk.Label(frame, text="Дата прекращения учета (yyyy-mm-dd): ")
date_entry2 = tk.Entry(frame)

frac_label1 = tk.Label(frame, text="Введите кадастровую стоимость (млн. руб):")
frac_entry1 = tk.Entry(frame)

select_label1 = tk.Label(frame, text="Укажите категорию налогоплательщика: ")
select1_values = ['Никакая из нижеперечисленных', 'Герой Советского Союза,Герой Российской Федераци',
                  'Пенсионер или лицо достигших возраста 60 и 55 лет', 'Ветеран или инвалид ВОВ',
                  'Физических лиц, имеющих трех и более несовершеннолетних детей.и т.д.']
select1 = ttk.Combobox(frame, values=select1_values)
select1['width'] = max([len(value) for value in select1_values])

select_label2 = tk.Label(frame, text="Укажите вид земельного участка:")
select2_values = ['Земли сельскохозяйственного назначения',
                  'Занятых жилищным фондом и объектами инженерной инфраструктуры       ',
                  'Земли для обеспечения обороны, безопасности и таможенных нужд',
                  'Прочих земельные участки']
select2 = ttk.Combobox(frame, values=select2_values)
select2['width'] = max([len(value) for value in select2_values])

select_label3 = tk.Label(frame, text="Укажите назначение: ")
select3_values = ['Жилищное строительство в течении 3 лет', 'Жилищное строительство меньше 3 лет',
                  'Жилищное строительство больше 3 лет',
                  'Индивидуальное жилищное строительство 10 лет',
                  'Земельный участок']
select3 = ttk.Combobox(frame, values=select3_values)
select3['width'] = max([len(value) for value in select3_values])

open_button = tk.Button(frame, text="Расчитать", command=open_new_window)

date_label1.grid(row=0, column=0, pady=10)
date_entry1.grid(row=0, column=1, pady=10)
date_label2.grid(row=1, column=0, pady=10)
date_entry2.grid(row=1, column=1, pady=10)

frac_label1.grid(row=2, column=0, pady=10)
frac_entry1.grid(row=2, column=1, pady=10)

select_label1.grid(row=5, column=0, pady=10)
select1.grid(row=5, column=1, pady=10)
select_label2.grid(row=6, column=0, pady=10)
select2.grid(row=6, column=1, pady=10)
select_label3.grid(row=7, column=0, pady=10)
select3.grid(row=7, column=1, pady=10)

open_button.grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()