               ____==========_______		       ________________.  ___     .______
    _--____   |    | ""  " "|       \		      /                | /   \    |   _  \
   /  )8}  ^^^| 0  |  =     |  o  0  |	   	     |   (-----|  |----`/  ^  \   |  |_)  |
 </_ +-==B vvv|""  |  =     | '  "" "|  	     		\   \    |  |    /  /_\  \  |      /
    \_____/   |____|________|________|		 .-----)   |   |  |   /  _____  \ |  |\  \-------.
             (_(  )\________/___(  )__)	       |________/    |__|  /__/     \__\| _| `.________|
               |\  \            /  /\		  ____    __    ____  ___     .______    ________.	
               | \  \          /  /\ \		  \   \  /  \  /   / /   \    |   _  \  /        |
               | |\  \        /  /  \ \            \   \/    \/   / /  ^  \   |  |_)  ||   (-----` 
               (  )(  )       (  \   (  )   	    \            / /  /_\  \  |      /  \   \
                \  / /        \  \   \  \            \    /\    / /  _____  \ |  |\  \---)   |
                 \|  |\        \  \  |  |   		\__/  \__/ /__/     \__\|__| `._______/
                  |  | )____    \  \ \  )___ 
                  (  )  /  /    (  )  (/  /  
                 /___\ /__/     /___\ /__/   

The AT-AT, By Core21
https://asciiart.website/
------------------------------------------------

################################################
#        						     #
#	INFOPROG 2023 - Házi forduló             #
#							     #
#	Veres Benedek Zoltán                     #
#	Selye János Gimnázium, Komárom, III.A    #
#							     #
################################################



#Szükségletek:
	- Lehető legfrissebb python a számítógépen(3.11)
	- A program felinstalálása (amennyiben megtalálható a venv mappa, akkor a program fel van instalálva, esetleges
	  hiba esetén, nem indul el a program, próbálja kitörölni ezt a mappát, majd újra felinstalálni a setup.bat segítségével)


#Instalálás
	- Indítsa el a setup.bat fájlt, pár percet vesz igénybe, míg létrehozza a szükséges virtuális környezetet,
	  az instaláció végeztével megjelenik egy "sikeres instaláció" szöveg
	
	- a program futtatható a start.bat fájl segítségével


#A program használata:
	Gombok:
		- Mai nap:
			- Kírja a mai nap teendőit
		- Felvitel:
			- Felvihet egy új eseményt a programba
		- Keresés:
			- A naptár widget segítségével keresni tud a dátumok között, azokat a napokat, amelyeken
			  már van valamilyen esemény azok pirosak lesznek
		- Listázás:
			- Kiírja a naplo.txt fájlból az összes dátumot (a naplo.txt file a data menüpont alatt található
		- Törlés:
			- Kitörli az összes olyan eseményt, melynek a dátuma öregebb a mainál.
		
	Config:
		- config mappában található itt átállítható a napló forráshelye azzal hogy megadjuk az útját az új naplónak(vagy a main.py programhoz 		  képest relatívan, ahogy a pythonban lehet)
		- átállítható a 250 karakteres leírás limit. FONTOS: a program felülete úgy van felépítve, hogy legfeljebb 250 karaktert tudjon 			  kilistázni

		
#stress test generator:
	- Az algoritmusok tesztelése képpen írtam egy generátor programot, ami több ezer soros naplókat generál le hogy tesztelni tudjuk a 		  	  datacontainer idejét a tool/stress_test mappában elérhető



		