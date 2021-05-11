from random import randint
from tkinter import *
from decimal import Decimal as d

all_count = 2
level = 0
money_count = 0
death_time = d('20')
death_timer = 0
reproduction_timer = 0
recovery_timer = d('15')
farm_parameters = {'recovery_time': d('15'), 'birth_number': d('5'), 'pair_number': d('3'),
                   'auto_percent': d('0.5'), 'death_percent': d('0.07'), 'price': d('10')}
upgrades = {'recovery_time': d('5'), 'birth_number': d('10'), 'pair_number': d('20'),
            'auto_percent': d('0.1'), 'death_percent': d('0.005')}
costs = {'recovery_time': d('100'), 'birth_number': d('100'), 'pair_number': d('100'),
         'auto_percent': d('100'), 'death_percent': d('100')}
cost_upgrades = {'recovery_time': d('40'), 'birth_number': d('60'), 'pair_number': d('80'),
                 'auto_percent': d('100'), 'death_percent': d('100')}


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


def reproduction(rep_type):
    global farm_parameters
    global all_count
    global recovery_timer
    if rep_type == 'hand':
        reproduction_button.configure(state=DISABLED)
        recovery_timer = farm_parameters['recovery_time']
    birth_count = max(1, farm_parameters['birth_number'] + randint(-3, 3))
    birth_count *= min(all_count // 2, farm_parameters['pair_number'])
    if rep_type == 'auto':
        birth_count *= farm_parameters['auto_percent']
    birth_count = int(birth_count)
    all_count += birth_count
    count_check()
    level_check()


def death():
    global farm_parameters
    global all_count
    death_count = farm_parameters['death_percent'] * all_count
    death_count = int(death_count)
    all_count -= death_count
    level_check()
    count_check()


def sale(number):
    global farm_parameters
    global all_count
    global money_count
    all_count -= number
    money_count += farm_parameters['price'] * number
    money_info.configure(text='Количество монеток: {}'.format(money_count))
    level_check()
    count_check()


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
        farm_parameters[parameter] -= (farm_parameters[parameter] * upgrades[parameter] / 100).quantize(d('0.01'))
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
        reproduction_button.configure(state=NORMAL)
    root.after(100, recovery_timer_update)


root = Tk()
root.poll = True
entry = Entry()
root.title('Rabbits')
root.geometry('1000x500')

info_frame = LabelFrame(root, relief=RAISED, borderwidth=2, text='Информация о ферме')
info_frame.grid(column=0, row=0, padx=5, pady=5)
count_info = Label(info_frame, text='Количество кроликов: {}'.format(all_count))
money_info = Label(info_frame, text='Количество монеток: {}'.format(money_count))
level_info = Label(info_frame, text='Уровень фермы: {}'.format(level))
death_time_info = Label(info_frame, text='Время до вымирания: {} сек.'.format(death_timer))
reproduction_time_info = Label(info_frame, text='Время до авторазмножения: {} сек.'.format(reproduction_timer))
count_info.grid(column=0, row=0)
money_info.grid(column=0, row=1)
level_info.grid(column=0, row=2)
death_time_info.grid(column=0, row=3)
reproduction_time_info.grid(column=0, row=4)

sell_num = IntVar()
sell_num.set(0)
sell_frame = LabelFrame(root, relief=RAISED, borderwidth=2, text='Магазин')
sell_frame.grid(column=1, row=0, padx=5, pady=5)
sell_button1 = Radiobutton(sell_frame, text='1', variable=sell_num, value=1)
sell_button5 = Radiobutton(sell_frame, text='5', variable=sell_num, value=5)
sell_button10 = Radiobutton(sell_frame, text='10', variable=sell_num, value=10)
sell_button30 = Radiobutton(sell_frame, text='30', variable=sell_num, value=30)
sell_button50 = Radiobutton(sell_frame, text='50', variable=sell_num, value=50)
sell_button100 = Radiobutton(sell_frame, text='100', variable=sell_num, value=100)
sell_button300 = Radiobutton(sell_frame, text='300', variable=sell_num, value=300)
sell_button500 = Radiobutton(sell_frame, text='500', variable=sell_num, value=500)
sell_button1000 = Radiobutton(sell_frame, text='1000', variable=sell_num, value=1000)
sell_button3000 = Radiobutton(sell_frame, text='3000', variable=sell_num, value=3000)
sell_button5000 = Radiobutton(sell_frame, text='5000', variable=sell_num, value=5000)
sell_button10000 = Radiobutton(sell_frame, text='10000', variable=sell_num, value=10000)
sell_button = Button(sell_frame, text='Продать', command=lambda: sale(sell_num.get()), state=DISABLED)


def sale_check():
    global all_count
    global sell_num
    if all_count < sell_num.get():
        sell_button.configure(state=DISABLED)
    else:
        sell_button.configure(state=NORMAL)
    root.after(10, sale_check)


sell_button1.grid(column=0, row=0)
sell_button5.grid(column=1, row=0)
sell_button10.grid(column=2, row=0)
sell_button30.grid(column=0, row=1)
sell_button50.grid(column=1, row=1)
sell_button100.grid(column=2, row=1)
sell_button300.grid(column=0, row=2)
sell_button500.grid(column=1, row=2)
sell_button1000.grid(column=2, row=2)
sell_button3000.grid(column=0, row=3)
sell_button5000.grid(column=1, row=3)
sell_button10000.grid(column=2, row=3)
sell_button.grid(column=1, row=4)

reproduction_frame = LabelFrame(root, text='Размножение', relief=RAISED, borderwidth=2)
reproduction_frame.grid(column=2, row=0)
reproduction_button = Button(reproduction_frame, text='Размножить кроликов', state=DISABLED,
                             command=lambda: reproduction('hand'))
recovery_timer_info = Label(reproduction_frame, text='Время до активации: {} сек.'.format(recovery_timer))
reproduction_button.grid(column=0, row=0)
recovery_timer_info.grid(column=0, row=1)

upgrading_frame = LabelFrame(root, text='Улучшение фермы', relief=RAISED, borderwidth=2)
upgrading_frame.grid(column=0, row=1, columnspan=2)
recovery_time_info = Label(upgrading_frame, text='Время восстановления кнопки размножения: {} сек.'
                           .format(farm_parameters['recovery_time']))
birth_number_info = Label(upgrading_frame, text='Среднее количество кроликов в потомстве: {}.'
                          .format(farm_parameters['birth_number']))
pair_number_info = Label(upgrading_frame, text='Количество пар, размножающихся за 1 нажатие: {}.'
                         .format(farm_parameters['pair_number']))
auto_percent_info = Label(upgrading_frame, text='Параметры авторазмножения: {}% от параметров выше.'
                          .format(farm_parameters['auto_percent'] * 100))
death_percent_info = Label(upgrading_frame,
                           text='Смертность: {}% от популяции.'.format(farm_parameters['death_percent']*100))
price_info = Label(upgrading_frame, text='Цена продажи 1 кролика: {} монеток.'.format(farm_parameters['price']))

recovery_time_info.grid(column=0, row=0)
birth_number_info.grid(column=0, row=1)
pair_number_info.grid(column=0, row=2)
auto_percent_info.grid(column=0, row=3)
death_percent_info.grid(column=0, row=4)
price_info.grid(column=0, row=5)

recovery_time_upgrade = Button(upgrading_frame, text='Уменьшить на {}% \n Стоимость: {} монеток'
                               .format(upgrades['recovery_time'], costs['recovery_time']),
                               command=lambda: upgrade_parameter('recovery_time', costs['recovery_time']))
birth_number_upgrade = Button(upgrading_frame, text='Увеличить на {}% \n Стоимость: {} монеток'
                              .format(upgrades['birth_number'], costs['birth_number']),
                              command=lambda: upgrade_parameter('birth_number', costs['birth_number']))
pair_number_upgrade = Button(upgrading_frame, text='Увеличить на {}% \n Стоимость: {} монеток'
                             .format(upgrades['pair_number'], costs['pair_number']),
                             command=lambda: upgrade_parameter('pair_number', costs['pair_number']))
auto_percent_upgrade = Button(upgrading_frame, text='Увеличить на {}% \n Стоимость: {} монеток'
                              .format(upgrades['auto_percent'] * 100, costs['auto_percent']),
                              command=lambda: upgrade_parameter('auto_percent', costs['auto_percent']))
death_percent_upgrade = Button(upgrading_frame, text='Уменьшить на {}% \n Стоимость: {} монеток'
                               .format(upgrades['death_percent']*100, costs['death_percent']),
                               command=lambda: upgrade_parameter('death_percent', costs['death_percent']))
upgrade_buttons = [recovery_time_upgrade, birth_number_upgrade, pair_number_upgrade,
                   auto_percent_upgrade, death_percent_upgrade]
names = ['recovery_time', 'birth_number', 'pair_number', 'auto_percent', 'death_percent']

recovery_time_upgrade.grid(column=1, row=0)
birth_number_upgrade.grid(column=1, row=1)
pair_number_upgrade.grid(column=1, row=2)
auto_percent_upgrade.grid(column=1, row=3)
death_percent_upgrade.grid(column=1, row=4)


def upgrade_info_and_buttons_update():
    money_info.configure(text='Количество монеток: {}'.format(money_count))
    recovery_time_info.configure(text='Время восстановления кнопки размножения: {} сек.'
                                 .format(farm_parameters['recovery_time']))
    birth_number_info.configure(text='Среднее количество кроликов в потомстве: {}.'
                                .format(farm_parameters['birth_number']))
    pair_number_info.configure(text='Количество пар, размножающихся за 1 нажатие: {}.'
                               .format(farm_parameters['pair_number']))
    auto_percent_info.configure(text='Параметры авторазмножения: {}% от параметров выше.'
                                .format(farm_parameters['auto_percent'] * 100))
    death_percent_info.configure(text='Смертность: {}% от популяции.'.format(farm_parameters['death_percent']*100))
    price_info.configure(text='Цена продажи 1 кролика: {} монеток.'.format(farm_parameters['price']))
    recovery_time_upgrade.configure(text='Уменьшить на {}% \n Стоимость: {} монеток'
                                    .format(upgrades['recovery_time'], costs['recovery_time']))
    birth_number_upgrade.configure(text='Увеличить на {}% \n Стоимость: {} монеток'
                                   .format(upgrades['birth_number'], costs['birth_number']))
    pair_number_upgrade.configure(text='Увеличить на {}% \n Стоимость: {} монеток'
                                  .format(upgrades['pair_number'], costs['pair_number']))
    auto_percent_upgrade.configure(text='Увеличить на {}% \n Стоимость: {} монеток'
                                   .format(upgrades['auto_percent'] * 100, costs['auto_percent']))
    death_percent_upgrade.configure(text='Уменьшить на {}% \n Стоимость: {} монеток'
                                    .format(upgrades['death_percent']*100, costs['death_percent']))


def update_price_check():
    global costs
    global upgrade_buttons
    global names
    global money_count
    for i in range(0, 5):
        if costs[names[i]] > money_count:
            upgrade_buttons[i].configure(state=DISABLED)
        else:
            upgrade_buttons[i].configure(state=NORMAL)
    root.after(10, update_price_check)


reproduction_cycle()
reproduction_timer_update()
death_cycle()
death_timer_update()
recovery_timer_update()
sale_check()
update_price_check()

root.mainloop()
