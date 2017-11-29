# UPS Raport Creator

Program generujący tzw. 'koniec dnia', czyli protokół przekazania paczek z danego dnia. Raport taki można sobie w prosty
 sposób wygenerować jeśli korzystamy z programu WorldShip. Jeśli jednak korzystamu wyłącznie z serwisu webowego UPS, 
 raport taki jest niedostępny. 

## Konfiguracja

W pliku config.py musimy podać nasz login i hasło do serwisu UPS, a także nazwę naszego konta, która pojawia się po 
zalogowaniu (program wykorzystuje ją aby sprawdzić czy logowanie się powiodło).

## Jak działa?

Po uruchomiuniu run.py w katalogu 'files' pojawią się dwa pliki. Jeden .csv (pełne dane o paczkach pobrane z serwisu 
UPS) oraz .xlsx, czyli nasz raport z niezbędnymi polami. Pliki będą tworzone osobno dla każdego dnia. Jeśli wykonamy 
analizę ponownie danego dnia, pliki zostaną nadpisane.
