import csv
basic_data = []
correct_data = []
incorrect_data = []

with open('Beispieldaten Einkaufspreise.csv', 'r') as Input_File:
    read = csv.DictReader(Input_File, delimiter=';')
    for line in read:
        line['Status'] = []
        basic_data.append(line)


def kalk_right_place(article4):
    for e, line4 in enumerate(article4):
        if e == 1:
            line4['Kalk'] = 'X'
        else:
            line4['Kalk'] = ''


def double_price_or_value(double_value):
    for value in double_value:
        result = double_value.count(value)
        if result > 1:
            return False
    return True


def squadron_correct(article2):
    squadron = []
    for line2 in article2:
        if line2['Menge'] == '':
            line2['Status'].append('Staffelwert fehlt')
            return False
        else:
            squadron.append(int(line2['Menge']))
    rv2 = double_price_or_value(squadron)
    if rv2:
        flag = 0
        test_correct = squadron[:]
        test_correct.sort()
        if test_correct == squadron:
            flag = 1
        if flag:
            return True
        else:
            for line3 in article2:
                line3['Status'].append('Staffelwert nicht aufsteigend')
            return False
    else:
        for line5 in article2:
            line5['Status'].append('Gleicher Staffelwert')
        return False


def price_correct_squadron(article3):
    price_order = []
    for line2 in article3:
        if line2['Preis'] == '':
            line2['Status'].append('Preis fehlt')
            return False
        else:
            price_order.append(float(line2['Preis'].replace(',', '.')))
    rv = double_price_or_value(price_order)
    if rv:
        flag = 0
        test_correct2 = price_order[:]
        test_correct2.sort(reverse=True)
        if test_correct2 == price_order:
            flag = 1
        if flag:
            return True
        else:
            for line3 in article3:
                line3['Status'].append('Preise nicht absteigend')
            return False
    else:
        for line4 in article3:
            line4['Status'].append('Doppelter Preis')
        return False


# main

article = []
for i, dataset in enumerate(basic_data):
    if i == 0:
        article.append(dataset)
    else:
        if dataset['Material'] in [art['Material'] for art in article]:
            article.append(dataset)
        else:
            if len(article) >= 2:
                rv_squadron = squadron_correct(article)
                rv_price = price_correct_squadron(article)
                if rv_squadron and rv_price:
                    kalk_right_place(article)
                    for item in article:
                        correct_data.append(item)
                else:
                    for item2 in article:
                        incorrect_data.append(item2)
            else:
                for art in article:
                    if art['Preis'] == '' or art['Preis'] == '0':
                        art['Status'].append('Kein Preis')
                        incorrect_data.append(art)
                    else:
                        if int(art['Menge']) > 1:
                            art['Kalk'] = 'X'
                            correct_data.append(art)
                        else:
                            correct_data.append(art)
            article.clear()
            article.append(dataset)

# print(article)
# TODO der letzte Artikel in der Schleife muss noch verarbeitet werden.

for print_out in incorrect_data:
    resolved_status = ''
    for status in print_out['Status']:
        resolved_status += status + ', '
    print_out['Status'] = resolved_status


with open('Fehlerliste.csv', 'w') as csvfile:
    fieldnames = ['Lieferant', 'Liferanten_Nr', 'Material', 'Preiseinheit', 'Mengeneinheit',
                  'Menge', 'Preis', 'Waehrung', 'Code', 'Beginn', 'Ende', 'Kalk', 'Status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    for see in incorrect_data:
        writer.writerow(see)

print(len(basic_data))
print(len(correct_data))
print(len(incorrect_data))
