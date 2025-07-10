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
<img src="https://i.imgur.com/tstUSon.png" style="max-width:100%; height:auto; display:block; margin:auto;" alt="Disk Sanitization Steps"/>
<br />
<h3> 2.1.2 Python-Django</h3>
<br />
<br />
<img src="https://i.imgur.com/0gpaPQc.png" style="max-width:100%; height:auto; display:block; margin:auto;" alt="Disk Sanitization Steps"/>
<br />
<h3>2.1.3.Visual Studio Code</h3>
<br />
<br />
<img src="https://i.imgur.com/vLczaGc.png" style="max-width:100%; height:auto; display:block; margin:auto;" alt="Disk Sanitization Steps"/>
<br />

<h3>2.1.4 Windows PowerShell</h3>
<br />
<br />
<img src="https://i.imgur.com/swHorZU.png" style="max-width:100%; height:auto; display:block; margin:auto;" alt="Disk Sanitization Steps"/>
<br />

<h2> 2.2 Hardware</h2>
<h3> 2.2.1 ESP 32</h3>
<br />
<br />
<img src="https://i.imgur.com/PPFy0hz.png" style="max-width:100%; height:auto; display:block; margin:auto;" alt="Disk Sanitization Steps"/>
<br /> 

<h3>  2.2.2 RC522 RFID-Modul</h3>
<br />
<br />
<img src="https://i.imgur.com/ELRIocU.png" style="max-width:100%; height:auto; display:block; margin:auto;" alt="Disk Sanitization Steps"/>
<br /> 

<h3>  2.2.3 LCD Touchscreen 2.8inch SPI Module ILI9341</h3>
<br />
<br />
<img src="https://i.imgur.com/KETXBVF.png" style="max-width:100%; height:auto; display:block; margin:auto;" alt="Disk Sanitization Steps"/>
<br /> 

<h3>   2.2.4 Micro Servo 9G (SG90)</h3>
<br />
<br />
<img src="https://i.imgur.com/nnj8yPk.png" style="max-width:100%; height:auto; display:block; margin:auto;" alt="Disk Sanitization Steps"/>
<br />

<h2> 3 Programmablauf</h2>
Wird das Programm gestartet, 
<br />
<br />
<img src="https://i.imgur.com/kapRb6c.png" style="max-width:100%; height:auto; display:block; margin:auto;" alt="Disk Sanitization Steps"/>
<br />

<h2> Aufbau</h2>
<br />
<p align="center">
  <img src="https://i.imgur.com/a78HhZL.jpeg" style="max-width:100%; height:auto; display:block; margin:auto;" />
  <img src="https://i.imgur.com/7A9rFIG.jpeg" style="max-width:100%; height:auto; display:block; margin:auto;" />
</p>

<br />
<br />
<h2> Einlogen-Seite</h2>
Das Web-Interface soll durch Benutzername und Passwort geschützt sein. Der Zugang soll auf Administratoren beschränkt sein.
<br />
<br />
<img src="https://i.imgur.com/jcRT7aK.png" style="max-width:100%; height:auto; display:block; margin:auto;" alt="Disk Sanitization Steps"/>
<br />

<h2>Die Hauptseite</h2>
Die Web-Interface wurde realisiert, der Admin kann Benutzer eintragen bzw. löschen. Es ist außerdem möglich, eingetragene Benutzer zu editieren. Eingetragene Benutzer sind persistent gespeichert , d.h. bei einem Stromausfall bleiben alle Daten erhalten.
<br />
<br />
<img src="https://i.imgur.com/dNDweek.png" style="max-width:100%; height:auto; display:block; margin:auto;" alt="Disk Sanitization Steps"/>
<br />

<h2>Protokoll-Seite</h2>
Die Implementierung des Türprotokollierungssystems wurde erfolgreich abgeschlossen. Bei jeder Türöffnung werden nun der Benutzername, das Datum, die Uhrzeit sowie das verwendete Authentifizierungsverfahren protokolliert. Das Protokoll verfügt über eine einstellbare Länge; sobald die maximale Anzahl an Einträgen erreicht wird, werden die ältesten automatisch gelöscht. Zudem kann das Protokoll über das Benutzerinterface eingesehen werden.
<br />
<br />
<img src="https://i.imgur.com/eRvtwsB.png" style="max-width:100%; height:auto; display:block; margin:auto;" alt="Disk Sanitization Steps"/>
<br />
