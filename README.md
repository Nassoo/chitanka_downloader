# chitanka-downloader

Програмата е създадена с цел да бъдат изтегляни и обновявани архиви на "[Моята библиотека](https://chitanka.info/)". За момента е налична версия само за Windows.  
За да я използвате, изтеглете файла **[ChitankaDownloader.zip](https://github.com/Nassoo/chitanka-downloader/releases/download/windows/ChitankaDownloader.zip)** и го разархивирайте в папка по Ваш избор (не е необходима инсталация - може да я използвате и от USB памет).
В папката ще се създаде подпапката user_data, в която се съхранява необходимата информация, за да е възможно обновяването на архива. Не изтривайте и не променяйте съдържанието &#x45d; - в противен случай обновяването може да не работи, както се очаква.
Освен нея, ще откриете и файл ChitankaDownloader.exe - стартирайте го и следвайте инструкциите на екрана.

За да работи, е необходимо да сте изтеглили и стартирали "[Моята библиотека като преносима версия](https://forum.chitanka.info/chitanka-standalone-edition-t6309.html)".
Това се налага, тъй като ако всички файлове се изтеглят директно от официалната страница на [Моята библиотека](https://chitanka.info/), това би довело до претоварване на сървъра и отказване на заявките. Все пак е добре да имате достъп до интернет, за да може при евентуален проблем в преносимата версия да се изтеглят файловете от официалната страница (за момента има само един файл, който не може да бъде изтеглен от преносимата версия).

Основната единица в базата данни на сайта е "произведение". Някои от произведенията са част от книги, а други - не. Тази програма ще включи в създадените архиви всички книги, както и произведенията, които не са част от книга, без да ги дублира (т.е. произведение, което е част от книга, няма да бъде изтегляно отделно - напр. стихотворението "Генуа" от А. Далчев ще бъде включено в книгата "Ангелът на Шартър" и няма да бъде свалено като самостоятелен файл).  
Данните ще бъдат подредени по следния модел:
* [А]
  * [Азимов, Айзък]
    * [Фондацията]
      * Айзък Азимов - Ф - 1) Прелюдия за Фондацията.fb2.zip
      * Айзък Азимов - Ф - 2) Битката за Фондацията.fb2.zip
      * ...
    * Айзък Азимов - А-шахта.fb2.zip
    * Айзък Азимов - Аз съм в Порт Марс без Хилда.fb2.zip
    * ...

Първоначалното стратиране на ChitankaDownloader.exe ще е сравнително бавно (изчакайте няколко секунди). Изтеглянето на всички файлове ще отнеме дълго време (около 4-5 часа). Ако прекъснете процеса от бутона "Изход", при следващото стартиране можете да изберете "Само обнови" - така файловете ще продължат да се изтеглят от там, докъдето са стигнали.  
След като всички файлове са свалени на Вашия диск, можете периодично до обновявате данните в архива, без да се налага да теглите всички файлове отначало. За целта първо обновете "[Моята библиотека като преносима версия](https://forum.chitanka.info/chitanka-standalone-edition-t6309.html)", както е описано [тук](https://chitanka.info/resources/own-server). След това стартирайте ChitankaDownloader.exe и изберете "Само обнови".  

В базата данни на "[Моята библиотека](https://chitanka.info/)" информацията за поредиците и номерата им е налична само за произведенията, но не и за книгите. След като процесът по изтегляне/обновяване на архива завърши, ще имате възможност да ги импортирате  във файловете, съдържащи книги от поредица. По този начин софтуерът на устройството, от което четете, ще има достъп до метаданните и ще показва информацията коректно. Тази стъпка е налична само ако сте избрали формат fb2.zip.  
Това засяга единствено метаданните в самите файлове - в структурата на архива информацията за поредиците и номерата им е налична (в имената на папките и на файловете), без значение дали сте избрали да се импортира информацията и независимо от формата на книгите.

Програмата е с интерфейс изцяло на български, тъй като това е езикът на произведенията в "[Моята библиотека](https://chitanka.info/)".