from argparse import Namespace
from deltachat2 import Bot, ChatType, CoreEvent, EventType, MsgData, NewMsgEvent, events, AttrDict
from deltabot_cli import BotCli
from gtts import gTTS
from googletrans import Translator
from googletrans.constants import LANGUAGES as gt_languages
from gtts.lang import tts_langs
import os
import tempfile
import logging

# Configuración del logging para depurar errores
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

cli = BotCli("multibot")

HELP = "Bot para traducir y Convertir texto a voz en múltiples idiomas"

def generar_tabla_idiomas_html():
    """
    Genera una tabla HTML con el listado de idiomas comunes entre gTTS y googletrans.
    Se aplica CSS inline para mejorar la presentación.
    """
    gtts_languages = tts_langs()
    common_langs = {code: gt_languages[code] for code in gtts_languages if code in gt_languages}

    html = """
    <html>
      <head>
        <style type="text/css">
          body { font-family: Arial, sans-serif; }
          h2 { text-align: center; color: #333; }
          table { border-collapse: collapse; width: 100%; }
          th, td { border: 1px solid #ddd; padding: 8px; }
          th { background-color: #4CAF50; color: white; text-align: left; }
          tr:nth-child(even){background-color: #f2f2f2;}
          tr:hover { background-color: #ddd; }
        </style>
      </head>
      <body>
        <h2>Listado de Idiomas Soportados</h2>
        <table>
          <tr>
            <th>Código</th>
            <th>Idioma</th>
          </tr>
    """
    for code, name in sorted(common_langs.items()):
        html += f"          <tr><td><strong>{code}</strong></td><td>{name.title()}</td></tr>\n"
    html += """
        </table>
      </body>
    </html>
    """
    return html

def send_message(bot, accid, chat_id, text=None, file=None, html=None):
    try:
        bot.rpc.send_msg(accid, chat_id, MsgData(text=text, file=file, html=html))
    except Exception as e:
        logging.error("Error enviando mensaje", exc_info=True)
        bot.rpc.send_msg(accid, chat_id, MsgData(text=f"Ocurrió un error: {str(e)}"))

@cli.on_init
def on_init(bot: Bot, args: Namespace) -> None:
    for accid in bot.rpc.get_all_account_ids():
        bot.rpc.set_config(accid, "displayname", "TransVoice")
        bot.rpc.set_config(accid, "selfstatus", HELP)
        bot.rpc.set_config(accid, "delete_device_after", str(60 * 60 * 24))

@cli.on(events.NewMessage(command="/tts"))
def traductor_pro(bot, accid, event):
    handle_translation(bot, accid, event, convert_to_speech=True)

@cli.on(events.NewMessage(command="/tr"))
def traductor(bot, accid, event):
    handle_translation(bot, accid, event, convert_to_speech=False)

def handle_translation(bot, accid, event, convert_to_speech=False):
    msg = event.msg
    chat = bot.rpc.get_basic_chat_info(accid, msg.chat_id)
    if chat.chat_type == ChatType.SINGLE:
        bot.rpc.markseen_msgs(accid, [msg.id])
    bot.rpc.send_reaction(accid, msg.id, ["⏳"])
    translator = Translator()

    try:
        parts = msg.text.split()
        if len(parts) < 3:
            send_message(bot, accid, msg.chat_id, "Por favor usa el formato correcto: /tts [lenguaje] [texto]")
            bot.rpc.send_reaction(accid, msg.id, [])
            return

        lang = parts[1].lower()
        text = ' '.join(parts[2:])

        # Validar que el idioma sea soportado (usamos googletrans para la validación)
        if lang not in gt_languages:
            send_message(
                bot, accid, msg.chat_id,
                f"El código de idioma '{lang}' no es válido. Consulta /langs para ver los idiomas disponibles."
            )
            bot.rpc.send_reaction(accid, msg.id, [])
            return

        traduccion = translator.translate(text, dest=lang)

        if convert_to_speech:
            tts = gTTS(traduccion.text, lang=lang)
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                filename = tmp_file.name
            tts.save(filename)
            send_message(bot, accid, msg.chat_id, file=filename)
            os.remove(filename)
        else:
            send_message(bot, accid, msg.chat_id, traduccion.text)

        bot.rpc.send_reaction(accid, msg.id, [])
    except Exception as e:
        logging.error("Error en handle_translation", exc_info=True)
        send_message(bot, accid, msg.chat_id, f"Ocurrió un error: {str(e)}")
        bot.rpc.send_reaction(accid, msg.id, [])

@cli.on(events.NewMessage(command="/langs"))
def langs(bot, accid, event):
    msg = event.msg
    chat = bot.rpc.get_basic_chat_info(accid, msg.chat_id)
    if chat.chat_type == ChatType.SINGLE:
        bot.rpc.markseen_msgs(accid, [msg.id])
    listado_html = generar_tabla_idiomas_html()
    send_message(bot, accid, msg.chat_id, text="**Idiomas disponibles:**", html=listado_html)

@cli.on(events.NewMessage(command="/help"))
def _help(bot: Bot, accid: int, event: AttrDict) -> None:
    msg = event.msg
    chat = bot.rpc.get_basic_chat_info(accid, msg.chat_id)
    if chat.chat_type == ChatType.SINGLE:
        bot.rpc.markseen_msgs(accid, [msg.id])
    send_help(bot, accid, msg.chat_id)

def send_help(bot: Bot, accid: int, chat_id: int) -> None:
    texto = """
    **Comandos disponibles**

    **/tts** [lenguaje] [texto] - Convertir texto a voz  
    **/tr**  [lenguaje] [texto] - Traducir texto a diferentes idiomas  
    **/langs** - Mostrar el listado de idiomas disponibles  
    **/help** - Mostrar los comandos disponibles  
    """
    send_message(bot, accid, chat_id, texto)

if __name__ == "__main__":
    cli.start()
