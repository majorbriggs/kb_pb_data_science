import pandas as pd

testowe = pd.read_csv('sys_testowy.csv', encoding='utf-8')

treningowe = pd.read_csv('sys_treningowy.csv', encoding='utf-8')

# nazwa wiersza z zestawu testowego
WYBRANY_ZESTAW = 'x1'

print(f'wybrany zestaw: {WYBRANY_ZESTAW}')

grouped_by_class = {}

# W tej petli ponizej iteruje po zestawach treningowych, i wpisuje je do słownika, gdzie kluczami są wartości klasy.
# chce sobie w ten sposob pogrupowac zestawy treningowe,
# W wyniku tej petli, slownik grouped_by_class wyglada mniej wiecej tak:
# {
#   "2" : [ zestaw_treningowy0,  zestaw_treningowy1, zestaw_treningowy2],
#   "4" : [ zestaw_treiningowy2, zestaw_treningowy4,  zestaw_treiningowy5]
# }
# czyli pod kluczem z wartoscia klasy wpisuje liste zestawow treningowych w ktorych c ma wartosc tego klucza

# Dzieki temu za pomocą grouped_by_class[2] mozesz uzyskac liste zestawow treningowych z klasa C=2,
# a za pomoca grouped_by_class[4] liste zestawow treningowych z klasa C=4.
# pozniej wykorzystuje to w metodzie liczacej te skladowe prawdopodobienstwa, tam dostaje
# liste zestawow z danej klasy za pomoca grouped_by_class[klasa]

for index, zestaw_treningowy in treningowe.iterrows():
    klasa = zestaw_treningowy[-1] # dla kolejnego zestawu zapisuje jego klase (ostatnia kolumna (c))
    if klasa not in grouped_by_class: # jesli nasz slownik jeszcze nie ma w sobie klucza dla tej klasy,
        grouped_by_class[klasa] = list() # dodaje do slownika pod tym kluczem pusta liste,
        # (ta linia powyzej wykona sie  tylko  dwa razy, raz doda pusta liste pod kluczem 2, a drugi raz pod kluczem 4
        # potem dla kazdego kolejnego zestawu treningowego, slownik ma juz te dwie listy, wiec, mozemy do tych list dodawac zestawy
    grouped_by_class[klasa].append(zestaw_treningowy)  # dodaje pod kluczem wybranej klasy kolejne zestawy treningowe

# wyciagam zestaw testowy (x1, x2, x3, itd., wedlug tego co jest w zmiennej na samej gorze skryptu)
zestaw_testowy = testowe.loc[WYBRANY_ZESTAW]

# Metoda wylicza prawdopodobienstwo skladowe typu P(a1 = 2|c = 4), dla danej kolumny i klasy
def prawd(kolumna, klasa):
    # wyciagam wartosc kolumny
    wartosc_atrybutu_z_zestawu_testowego = zestaw_testowy.loc[kolumna]
    licznik_wystapien = 0

    # zapisujemy ile mamy zestawow treningowych z daną klasą (w tym przykladzie to jest zawsze po 3, ale ta metoda
    # zadziala tez jak dodasz wiecej zestawow treningowych)

    # wyciagniecie ze slownika zestawow treningowych w ktorych c ma wartosc ktora mamy w zmiennej klasa
    zestawy_treningowe_z_danej_klasy = grouped_by_class[klasa]
    liczba_zestawow_z_danej_klasy = len(zestawy_treningowe_z_danej_klasy)

    # teraz iteruje po zestawach treningowych, i sprawdzam czy zadana kolumna w zestawie treningowym ma oczekiwana wartosc
    # z zestawu testowego, jeśli tak, dodaje do licznika wystąpien
    for i in zestawy_treningowe_z_danej_klasy:
        if i.loc[kolumna] == wartosc_atrybutu_z_zestawu_testowego:
            licznik_wystapien += 1
    return licznik_wystapien / liczba_zestawow_z_danej_klasy


p_a1_c2 = prawd("a1", 2)
p_a2_c2 = prawd("a2", 2)
p_a3_c2 = prawd("a3", 2)
p_a4_c2 = prawd("a4", 2)

p_a1_c4 = prawd("a1", 4)
p_a2_c4 = prawd("a2", 4)
p_a3_c4 = prawd("a3", 4)
p_a4_c4 = prawd("a4", 4)

zestawy_treningowe_z_klasa_2 = grouped_by_class[2] # wyciagam ze slownika liste zestawow dla klucza 2
zestawy_treningowe_z_klasa_4 = grouped_by_class[4]

# w naszym przykladzie to jest 3/6 = 0.5, ale ogólnie dziele tu liczbe zestawow z daną klasą, przez liczbe wszystkich zestawow treningowych
P_C2 = len(zestawy_treningowe_z_klasa_2) / len(treningowe)
P_C4 = len(zestawy_treningowe_z_klasa_4) / len(treningowe)

print(f'P(a1|c = 2) = {p_a1_c2}')
print(f'P(a2|c = 2) = {p_a2_c2}')
print(f'P(a3|c = 2) = {p_a3_c2}')
print(f'P(a4|c = 2) = {p_a4_c2}')
print()
print(f'P(a1|c = 4) = {p_a1_c4}')
print(f'P(a2|c = 4) = {p_a2_c4}')
print(f'P(a3|c = 4) = {p_a3_c4}')
print(f'P(a4|c = 4) = {p_a4_c4}')

Param_X_C_2 = P_C2 * (p_a1_c2 + p_a2_c2 + p_a3_c2 + p_a4_c2)

Param_X_C_4 = P_C4 * (p_a1_c4 + p_a2_c4 + p_a3_c4 + p_a4_c4)

# prawdopodobienstwo że C = 2 dla wybranego zestawu
print(f'Param_C2 = {Param_X_C_2}')

# prawdopodobienstwo że C = 4
print(f'Param_C4 = {Param_X_C_4}')

if Param_X_C_2 > Param_X_C_4:
    decyzja = 2
else:
    decyzja = 4

# tutaj wyciagam oryginalna "decyzje eksperta" z zestawu testowego (ostatnia kolumna), zeby porownac pozniej
# z ta ktora z naszych wyliczen miala teraz wieksze prawdopodobienstwo i stwierdzic czy klasyfikacja jest poprawna
oryginalna_decyzja = zestaw_testowy[-1]

print(f'Decyzja dla zestawu {WYBRANY_ZESTAW}: {decyzja}')
print(f'Oryginalna decyzją (ukryta decyzja eksperta): {oryginalna_decyzja}')
if (decyzja != oryginalna_decyzja):
    print("Blędna klasyfikacja")
else:
    print("Prawidłowa klasyfikacja")

# w przypadku zestawow x3 i x4, wszystkie p wynoszą zero, wiec ostateczna decyzja jest losowa
if (Param_X_C_4 == Param_X_C_2 == 0):
    print("P_C_4 == P_C_2 wiec obiekt dostal decyzję losową")

# Jak pisalem na gorze, ten skrypt moze
# dzialac dla wiekszej liczby zestawow treningowych (przez to ze te skladowe p wylicza w petli po wszystkich zestawach
# ktore w kolumnie c mają zadana klase
# mozesz to sprawdzic podmieniajac na gorze 'sys_treningowy.csv' na 'sys_treningowy_dodane_zestawy.csv'
