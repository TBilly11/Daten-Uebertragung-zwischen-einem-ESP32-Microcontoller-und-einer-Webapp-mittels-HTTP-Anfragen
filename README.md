# Datenübertragung zwischen einem ESP32-Microcontoller und einer Webanwendung  mittels HTTP-Anfragen
<h1>1 Projektspräsentation</h1>

Es soll ein elektronisches Gerät realisiert werden, mit dem es möglich ist, durch eine Zwei-Faktor-Authentifizierung ein Türschloss zu öffnen. Folgende Anforderungen sollen hierzu umgesetzt werden:

- Es soll eine Hardware aufgebaut werden, die mit einem ESP 32, einem Touch-Display, einem NFC-Reader und einer Ansteuerung für ein Türschloss ausgestattet ist. Außerdem sollen zwei Status-LEDs vorgesehen werden. Die Hardware soll in einem Gehäuse verbaut werden.

- Es soll ein Web-Interface realisiert werden, mit dem man Benutzer eintragen bzw. löschen kann. Es soll außerdem möglich sein, eingetragene Benutzer zu editieren. Das Web-Interface soll durch Benutzername und Passwort geschützt sein. Der Zugang soll auf Administratoren beschränkt sein. Eingetragene Benutzer sollen persistent gespeichert werden, d.h. bei einem Stromausfall bleiben alle Daten erhalten.

- Um die Tür zu öffnen, soll ein Benutzer eine NFC-Karte (Studentenkarte) an den Kartenleser halten können. Falls der Benutzer registriert ist, soll eine E-Mail an den Benutzer verschickt werden, in der eine einmalige sechsstellige Nummer angegeben ist (eTAN). Über das Touchdisplay des elektronischen Türschlosses muss diese Nummer eingegeben und bestätigt werden. Geschieht dies Fehlerfrei, wird das Türschloss geöffnet.

- Bei der Eingabe der Geheimnummer sollen einfache Korrekturen möglich sein (z.B. letzte Ziffer löschen).

- Es soll möglich sein, die Tür auch durch Ein Faktor-Authentifizierung zu öffnen. Dies soll aber nur erlaubt sein, wenn dies für den Benutzer eingetragen wurde. Bei der Ein-Faktor-Authentifizierung soll man das Türschloss öffnen können, indem man nur eine wenigstens 8-Stellige Geheimnummer eingibt. Jeder Benutzer soll dabei eine andere Nummer verwenden müssen.

- Es soll jeweils protokolliert werden, wenn die Tür geöffnet wird. Im Einzelnen soll dabei der Benutzername, das Datum, die Uhrzeit sowie das verwendete Authentifizierungsverfahren gespeichert werden. Das Protokoll soll eine einstellbare Länge aufweisen. Wenn die eingestellte Anzahl an Einträgen überschritten wird, sollen die ältesten Einträge automatisch gelöscht werden. Das Protokoll soll über das Benutzerinterface eingesehen werden können.

<h1> 2 Projektumgebung </h1>
<h2> 2.1 Software</h2>
<h3> 2.1.1 Arduino IDE</h3>
<br />
<br />
<img src="https://i.imgur.com/tstUSon.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />
<h3> 2.1.2 Python-Django</h3>
<br />
<br />
<img src="https://i.imgur.com/0gpaPQc.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />
<h3>2.1.3.Visual Studio Code</h3>
<br />
<br />
<img src="https://i.imgur.com/vLczaGc.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />

<h3>2.1.4 Windows PowerShell</h3>
<br />
<br />
<img src="https://i.imgur.com/swHorZU.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />


<h2> 2.2 Hardware</h2>
<h3> 2.2.1 ESP 32</h3>
<br />
<br />
<img src="https://i.imgur.com/PPFy0hz.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br /> 

<h3>  2.2.2 RC522 RFID-Modul</h3>
<br />
<br />
<img src="https://i.imgur.com/ELRIocU.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br /> 

<h3>  2.2.3 LCD Touchscreen 2.8inch SPI Module ILI9341</h3>
<br />
<br />
<img src="https://i.imgur.com/kZnzVf6.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br /> 

<h3>   2.2.4 Micro Servo 9G (SG90)</h3>
<br />
<br />
<img src="https://i.imgur.com/af6Yt23.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>

<br />
<h2> 3 Programmablauf</h2>
 Wird das Programm gestartet, erfolgt die Erzeugung des Display Objektes „lc“ und allen weiteren benötigten Variablen. Dann wird die setup() Funktion
 aufgerufen. Hier werden einmalig die LEDs des Displays sicherheitshalber ausgeschalten.
 Zudem wird die Helligkeit der LEDs eingestellt und falls sich die Matrizen im Energiespar
modus befinden, werden sie aufgeweckt. Darüber hinaus werden Einstellungen für die serielle
 Schnittstelle festgelegt und die Analogpins für den Joystick als Inputs deklariert.
 Aus Sicht des Benutzers erfolgt der erste Schritt im seriellen Monitor. Dort wird der User
 aufgefordert des Spiel mit einer Joystickbewegung zu starten. Nach erfolgter Eingabe beginnt
 das Spiel. Die Schlange, die nur aus einem Element besteht, und das Essen werden zufällig
 auf den Displays ausgegeben. Die Schlange bewegt sich noch nicht. Erst wenn der Benutzer
 eine Richtung vorgibt, setzt sie sich in Bewegung.
 Wurde das Spiel gestartet, werden nacheinander folgende Schritte ausgeführt: Je nach Rich
tung der Schlange werden in einer Funktion die Koordinaten (x, y und Display) der einzelnen
 Schlangenelemente geändert, damit die Schlange sich fortbewegt. Danach werden alle LEDs
 der Displays ausgeschalten, damit die Schlange ihre Größe behält. Direkt im Anschluss wer
den die aktualisierte Schlange und das Essen ausgegeben. Zudem wird in einer Funktion
 überprüft ob die Schlange des Essen gegessen hat. Ist dies der Fall vergrößert sie sich, die
 Geschwindigkeit steigt und das Essen wird neu positioniert. Zudem wird gecheckt ob die
 Schlange sich selbst getroffen hat und deswegen das Spiel abgebrochen werden muss. Danach
 erfolgt eine Delay-Funktion. Die Verzögerung ist von der aktuellen Bewegungsgeschwindig
keit der Schlange abhängig. Je geringer der Wert der Geschwindigkeitsvariable ist, desto
 schneller werden die gerade beschriebenen Funkionen aufgerufen, was zu einer schnelleren
 Bewegung der Schlange führt. Solange das Spiel läuft, werden die gerade genannten Schritte
 immer wieder durchgeführt. Außerdem wird dauerhaft, unabhängig von dem Delay, über
prüft in welcher Position der Joystick steht und speichert je nach Position die Richtung in
 einer Variablen.
 Trifft die Schlange sich selber wird die Schleife verlassen. Die LEDs werden ausgeschaltet. Es
 wird die erreichte Punktzahl des Benutzers auf dem seriellen Monitor sowie auf den Matri
zen ausgegeben. Wurde das Spiel schon mal gespielt, wird der Highscore aus dem EEPROM
 des Arduino gelesen. Ist die erreichte Punktzahl größer als der Highscore, wird diese in den
 EEPROM gespeichert. Wurde der Highscore nicht übertroffen, geschieht nichts.
 Danach kann der Benutzer durch eine Joystickbewegung das Spiel erneut starten und das
 Programm beginnt wieder von vorne zu laufen.
<br />
<br />
<img src="https://i.imgur.com/mO39alt.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />

