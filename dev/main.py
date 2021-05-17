from random import randint
import tkinter as tk
from decimal import Decimal as d

all_count = 2
level = 0
money_count = 0
death_time = d('20')
death_timer = 0
reproduction_timer = 0
recovery_timer = d('15')
farm_parameters = {'recovery_time': d('15'), 'birth_number': d('5'),
                   'pair_number': d('3'), 'auto_percent': d('0.5'),
                   'death_percent': d('0.07'), 'price': d('10')}
upgrades = {'recovery_time': d('5'), 'birth_number': d('10'),
            'pair_number': d('20'), 'auto_percent': d('0.1'),
            'death_percent': d('0.005')}
costs = {'recovery_time': d('100'), 'birth_number': d('100'),
         'pair_number': d('100'), 'auto_percent': d('100'),
         'death_percent': d('100')}
cost_upgrades = {'recovery_time': d('40'), 'birth_number': d('60'),
                 'pair_number': d('80'), 'auto_percent': d('100'),
                 'death_percent': d('100')}


def count_check():
    global all_count
    count_info.configure(text='Количество кроликов: {}'.format(max(0, all_count)))
    if all_count == 0:
        print('У вас больше не осталось кроликов')
    if all_count == 1:
        print('У вас остался только 1 кролик')


def level_check():
    global all_count
    global level
    if all_count < 10:
        count_check()
        level = 0
        level_info.configure(text='Уровень фермы: {}'.format(level))
    else:
        new_level = 0
        all_count_copy = all_count
        while all_count_copy >= 10:
            new_level += 1
            all_count_copy //= 10
        level = new_level
        level_info.configure(text='Уровень фермы: {}'.format(level))


def info_update():
    level_check()
    count_check()


def reproduction(rep_type):
    global farm_parameters
    global all_count
    global recovery_timer
    if rep_type == 'hand':
        reproduction_button.configure(state=tk.DISABLED)
        recovery_timer = farm_parameters['recovery_time']
    birth_count = max(1, farm_parameters['birth_number'] + randint(-3, 3))
    birth_count *= min(all_count // 2, farm_parameters['pair_number'])
    if rep_type == 'auto':
        birth_count *= farm_parameters['auto_percent']
    birth_count = int(birth_count)
    all_count += birth_count
    info_update()


def death():
    global farm_parameters
    global all_count
    death_count = farm_parameters['death_percent'] * all_count
    death_count = int(death_count)
    all_count -= death_count
    info_update()


def sale(number):
    global farm_parameters
    global all_count
    global money_count
    all_count -= number
    money_count += farm_parameters['price'] * number
    money_info.configure(text='Количество монеток: {}'.format(money_count))
    info_update()


def upgrade_parameter(parameter, cost):
    global money_count
    global farm_parameters
    global upgrades
    global costs
    global cost_upgrades
    money_count -= cost
    if parameter == 'auto_percent':
        farm_parameters[parameter] += upgrades[parameter]
    elif parameter == 'death_percent':
        farm_parameters[parameter] -= upgrades[parameter]
    elif parameter == 'recovery_time':
        farm_parameters[parameter] -= farm_parameters[parameter] * upgrades[parameter] / 100
        farm_parameters[parameter].quantize(d('0.01'))
    elif farm_parameters[parameter] < 10:
        farm_parameters[parameter] += 2
    else:
        farm_parameters[parameter] += int(farm_parameters[parameter] * upgrades[parameter] / 100)
    costs[parameter] += int(costs[parameter] * cost_upgrades[parameter] / 100)
    upgrade_info_and_buttons_update()


def death_timer_update():
    global death_timer
    global death_time
    death_timer -= d('1')
    death_time_info.configure(text='Время до вымирания: {} сек.'.format(death_timer))
    root.after(1000, death_timer_update)


def death_cycle():
    global death_time
    global death_timer
    death_timer = death_time
    death()
    root.after(1000 * death_time, death_cycle)


def reproduction_timer_update():
    global reproduction_timer
    global farm_parameters
    reproduction_timer -= d('0.1')
    reproduction_time_info.configure(text='Время до авторазмножения: {} сек.'.format(reproduction_timer))
    root.after(100, reproduction_timer_update)


def reproduction_cycle():
    global farm_parameters
    global reproduction_timer
    reproduction_timer = farm_parameters['recovery_time'] * farm_parameters['auto_percent']
    reproduction('auto')
    root.after(int(1000 * farm_parameters['recovery_time'] * farm_parameters['auto_percent']),
               reproduction_cycle)


def recovery_timer_update():
    global recovery_timer
    global farm_parameters
    if recovery_timer > 0:
        recovery_timer -= d('0.1')
        recovery_timer_info.configure(text='Время до активации: {} сек.'.format(recovery_timer))
    else:
        recovery_timer_info.configure(text='')
        reproduction_button.configure(state=tk.NORMAL)
    root.after(100, recovery_timer_update)


root = tk.Tk()
root.poll = True
entry = tk.Entry()
root.title('Rabbits')
root.geometry('1000x500')

info_frame = tk.LabelFrame(root, relief=tk.RAISED, borderwidth=2, text='Информация о ферме')
info_frame.grid(column=0, row=0, padx=5, pady=5)

count_info = tk.Label(info_frame,
                      text='Количество кроликов: {}'.format(all_count))
money_info = tk.Label(info_frame,
                      text='Количество монеток: {}'.format(money_count))
level_info = tk.Label(info_frame,
                      text='Уровень фермы: {}'.format(level))
death_time_info = tk.Label(info_frame,
                           text='Время до вымирания: {} сек.'.format(death_timer))
reproduction_time_info = tk.Label(info_frame,
                                  text='Время до авторазмножения: {} сек.'.format(reproduction_timer))
farm_info_labels = [count_info, money_info, level_info,
                    death_time_info, reproduction_time_info]
for i in range(0, len(farm_info_labels)):
    farm_info_labels[i].grid(column=0, row=i)

# блок магазина
sell_num = tk.IntVar()
sell_num.set(0)
sell_frame = tk.LabelFrame(root, relief=tk.RAISED, borderwidth=2, text='Магазин')
sell_frame.grid(column=1, row=0, padx=5, pady=5)
sell_buttons_values = [1, 5, 10, 30, 50, 100, 300, 500, 1000, 3000, 5000, 10000]
sell_buttons = []
for value in sell_buttons_values:
    sell_buttons.append(tk.Radiobutton(sell_frame, text='{}'.format(value),
                                       variable=sell_num, value=value))

num = 0
for row in range(0, 4):
    for column in range(0, 3):
        sell_buttons[num].grid(column=column, row=row)
        num += 1

sell_button = tk.Button(sell_frame, text='Продать',
                        command=lambda: sale(sell_num.get()), state=tk.DISABLED)
sell_button.grid(column=1, row=4)


def sale_check():
    global all_count
    global sell_num
    if all_count < sell_num.get():
        sell_button.configure(state=tk.DISABLED)
    else:
        sell_button.configure(state=tk.NORMAL)
    root.after(10, sale_check)


# блок размножения
reproduction_frame = tk.LabelFrame(root, text='Размножение',
                                   relief=tk.RAISED, borderwidth=2)
reproduction_frame.grid(column=2, row=0)
reproduction_button = tk.Button(reproduction_frame, text='Размножить кроликов',
                                state=tk.DISABLED,
                                command=lambda: reproduction('hand'))
recovery_timer_info = tk.Label(reproduction_frame,
                               text='Время до активации: {} сек.'.format(recovery_timer))
reproduction_button.grid(column=0, row=0)
recovery_timer_info.grid(column=0, row=1)

# блок улучшения
# инфо
upgrading_frame = tk.LabelFrame(root, text='Улучшение фермы',
                                relief=tk.RAISED, borderwidth=2)
upgrading_frame.grid(column=0, row=1, columnspan=2)

names = ['recovery_time', 'birth_number', 'pair_number',
         'auto_percent', 'death_percent', 'price']
text_on_upgrade_labels = ['Время восстановления кнопки размножения: {} сек.',
                          'Среднее количество кроликов в потомстве: {}.',
                          'Количество пар, размножающихся за 1 нажатие: {}.',
                          'Параметры авторазмножения: {}% от параметров выше.',
                          'Смертность: {}% от популяции.',
                          'Цена продажи 1 кролика: {} монеток.']
upgrade_info_labels = []
for i in range(0, len(names)):
    upgrade_info_labels.append(tk.Label(upgrading_frame,
                                        text=text_on_upgrade_labels[i].format(farm_parameters[names[i]])))
    upgrade_info_labels[i].grid(column=0, row=i)

# кнопки
text_on_upgrade_buttons = ['Уменьшить на {}% \n Стоимость: {} монеток',
                           'Увеличить на {}% \n Стоимость: {} монеток',
                           'Увеличить на {}% \n Стоимость: {} монеток',
                           'Увеличить на {}% \n Стоимость: {} монеток',
                           'Уменьшить на {}% \n Стоимость: {} монеток']

upgrade_buttons = []

for i in range(0, len(names) - 1):
    upgrade_buttons.append(tk.Button(upgrading_frame,
                                     text=text_on_upgrade_buttons[i].format(upgrades[names[i]], costs[names[i]]),
                                     command=lambda i=i: upgrade_parameter(names[i], costs[names[i]])))
    upgrade_buttons[i].grid(column=2, row=i)


def upgrade_info_and_buttons_update():
    money_info.configure(text='Количество монеток: {}'.format(money_count))

    for lab in range(0, len(upgrade_info_labels)):
        upgrade_info_labels[lab].configure(
            text=text_on_upgrade_labels[lab].format(farm_parameters[names[lab]]))
    for lab in range(0, len(upgrade_buttons)):
        upgrade_buttons[lab].configure(
            text=text_on_upgrade_buttons[lab].format(upgrades[names[lab]], costs[names[lab]]))


def update_price_check():
    global costs
    global upgrade_buttons
    global names
    global money_count
    for button in range(0, len(upgrade_buttons)):
        if costs[names[button]] > money_count:
            upgrade_buttons[button].configure(state=tk.DISABLED)
        else:
            upgrade_buttons[button].configure(state=tk.NORMAL)
    root.after(10, update_price_check)


reproduction_cycle()
reproduction_timer_update()
death_cycle()
death_timer_update()
recovery_timer_update()
sale_check()
update_price_check()

root.mainloop()
