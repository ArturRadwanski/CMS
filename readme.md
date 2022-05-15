instalacja:
cd client
npm install
npm run build

uruchomienie projektu:
cd server
py server.py

konto admina:
login: admin
hasło: admin

nowego użytkownika można w dowolnej chwili zarejestrować, aby utworzyć nowego admina trzeba najpierw
utworzć konto użytkownika, a potem nadać mu prawa administratora z konta innego administratora (hasła się nie wyświetlają bo są haszowane ale można je zmieniać)

Edytowanie kontentu:
Pozwala zmienić treść strony home i stopki:
-dodawać nowe newsy
-edytować zawartowść i zdjęcie w bloku
-usuwać slidy ze slidera
-zmiana zawartości stopki(stopka wysuwa się po najechaniu na dolną część strony)
-zmiany należy zapisać przez wciśnięcie przycisku exit edit mode i potwierdzenie zmian

aby dodać nowy slide należy z konta administratora przejść do zakładki Add Slide

Edytowanie stylu:
-zmiana kolorów strony
-zmiana rodzaju menu(burger/klasyczne)
-zmiana kolejności wyświetlania elementów w stronie home
-zmiana fonta
-export i import ustawień

komentarze dodaje się do poszczególnych artykułów, użytkownik może usuwać komentarze dodane przez siebie
przycisk szukaj wyszukuje słów kluczowych w tytułach i kategoriach, można sortować wyniki po kategorii lub po tytule

w galerii admin może dodawać i usuwać zdjęcia

admin może edytować nick hasło i uprawnienia dowolnego użytkownika z wyjątkiem head admina
użytkownik może zmienić jedynie swój nick i hasło
