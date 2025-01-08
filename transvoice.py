from deltachat2 import MsgData, events, Bot, AttrDict
from deltabot_cli import BotCli
from gtts import gTTS
from googletrans import Translator
import os

cli = BotCli("multibot")

@cli.on(events.NewMessage(command="/tts"))
def traductorpro(bot, accid, event):  # < Traduce a Voz >
    msg = event.msg
    translator = Translator()  # Crea un objeto de la clase Translator
    
    try:
        # Valida que el formato del comando sea correcto
        if len(msg.text.split()) < 3:
            bot.rpc.send_msg(accid, msg.chat_id, MsgData(text="Por favor usa el formato correcto: /tts [lenguaje] [texto]"))
            return
        
        lang, text = msg.text[5:].split(' ', 1)  # Define la palabra o texto a traducir
        traduccion = translator.translate(text, dest=lang)  # Traduce el texto al idioma deseado
        tts = gTTS(traduccion.text, lang=lang)  # Convertimos el texto traducido a voz en el mismo idioma designado
        tts.save("text_to_speech.mp3")  # Guardamos en formato .mp3
        
        bot.rpc.send_msg(accid, msg.chat_id, MsgData(file="text_to_speech.mp3"))
    except Exception as e:
        bot.rpc.send_msg(accid, msg.chat_id, MsgData(text=f"Ocurrió un error: {str(e)}"))
    finally:
        if os.path.exists("text_to_speech.mp3"):
            os.remove("text_to_speech.mp3")  # Borramos el audio


from googletrans import Translator

@cli.on(events.NewMessage(command="/tr"))
def traductor(bot, accid, event):
    msg = event.msg
    translator = Translator()  # Crea un objeto de la clase Translator
    
    try:
        # Valida que el formato del comando sea correcto
        if len(msg.text.split()) < 3:
            bot.rpc.send_msg(accid, msg.chat_id, MsgData(text="Por favor usa el formato correcto: /tr [lenguaje] [texto]"))
            return

        lang, text = msg.text[4:].split(' ', 1)  # Define la palabra o texto a traducir
        traduccion = translator.translate(text, dest=lang)  # Traduce el texto al idioma deseado
        bot.rpc.send_msg(accid, msg.chat_id, MsgData(text=traduccion.text))
    except Exception as e:
        bot.rpc.send_msg(accid, msg.chat_id, MsgData(text=f"Ocurrió un error: {str(e)}"))


@cli.on(events.NewMessage(command="/langs"))
def langs(bot, accid, event):
    msg=event.msg
    list ="""
    <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de Idiomas</title>
    <style>
        body { 
            font-family: Arial, sans-serif;
            margin: 20px; 
            background-color: #f9f9f9;
                   } 
        h1 { 
            text-align: center; color: #333;
               } 
       ul { 
            list-style-type: none; 
            padding: 0; 
            text-align: center; 
             } 
       li { 
             background-color: #fff; 
             margin: 5px 0; 
             padding: 10px; 
             border: 1px solid #ddd;
             border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
             display: inline-block; width: 200px;
             } 
        li span { 
             font-weight: bold; 
             }
    </style>
</head>
<body>
    <h1>Lista de Idiomas</h1>
    <ul>
       <li><span>aa</span> afar</li>
<li><span>ab</span> abjasio (o abjasiano)</li>
<li><span>ae</span> avéstico</li>
<li><span>af</span> afrikáans</li>
<li><span>ak</span> akano</li>
<li><span>am</span> amhárico</li>
<li><span>an</span> aragonés</li>
<li><span>ar</span> árabe</li>
<li><span>as</span> asamés</li>
<li><span>av</span> avar (o ávaro)</li>
<li><span>ay</span> aimara</li>
<li><span>az</span> azerí</li>
<li><span>ba</span> baskir</li>
<li><span>be</span> bielorruso</li>
<li><span>bg</span> búlgaro</li>
<li><span>bh</span> bhoyapurí</li>
<li><span>bi</span> bislama</li>
<li><span>bm</span> bambara</li>
<li><span>bn</span> bengalí</li>
<li><span>bo</span> tibetano</li>
<li><span>br</span> bretón</li>
<li><span>bs</span> bosnio</li>
<li><span>ca</span> catalán</li>
<li><span>ce</span> checheno</li>
<li><span>ch</span> chamorro</li>
<li><span>co</span> corso</li>
<li><span>cr</span> cree</li>
<li><span>cs</span> checo</li>
<li><span>cu</span> eslavo eclesiástico antiguo</li>
<li><span>cv</span> chuvasio</li>
<li><span>cy</span> galés</li>
<li><span>da</span> danés</li>
<li><span>de</span> alemán</li>
<li><span>dv</span> maldivo (o dhivehi)</li>
<li><span>dz</span> dzongkha</li>
<li><span>ee</span> ewé</li>
<li><span>el</span> griego (moderno)</li>
<li><span>en</span> inglés</li>
<li><span>eo</span> esperanto</li>
<li><span>es</span> español (o castellano)</li>
<li><span>et</span> estonio</li>
<li><span>eu</span> euskera</li>
<li><span>fa</span> persa</li>
<li><span>ff</span> fula</li>
<li><span>fi</span> finés (o finlandés)</li>
<li><span>fj</span> fiyiano (o fiyi)</li>
<li><span>fo</span> feroés</li>
<li><span>fr</span> francés</li>
<li><span>fy</span> frisón (o frisio)</li>
<li><span>ga</span> irlandés (o gaélico)</li>
<li><span>gd</span> gaélico escocés</li>
<li><span>gl</span> gallego</li>
<li><span>gn</span> guaraní</li>
<li><span>gu</span> guyaratí (o gujaratí)</li>
<li><span>gv</span> manés (gaélico manés o de Isla de Man)</li>
<li><span>ha</span> hausa</li>
<li><span>he</span> hebreo</li>
<li><span>hi</span> hindi (o hindú)</li>
<li><span>ho</span> hiri motu</li>
<li><span>hr</span> croata</li>
<li><span>ht</span> haitiano</li>
<li><span>hu</span> húngaro</li>
<li><span>hy</span> armenio</li>
<li><span>hz</span> herero</li>
<li><span>ia</span> interlingua</li>
<li><span>id</span> indonesio</li>
<li><span>ie</span> occidental</li>
<li><span>ig</span> igbo</li>
<li><span>ii</span> yi de Sichuán</li>
<li><span>ik</span> iñupiaq</li>
<li><span>io</span> ido</li>
<li><span>is</span> islandés</li>
<li><span>it</span> italiano</li>
<li><span>iu</span> inuktitut (o inuit)</li>
<li><span>ja</span> japonés</li>
<li><span>jv</span> javanés</li>
<li><span>ka</span> georgiano</li>
<li><span>kg</span> kongo (o kikongo)</li>
<li><span>ki</span> kikuyu</li>
<li><span>kj</span> kuanyama</li>
<li><span>kk</span> kazajo (o kazajio)</li>
<li><span>kl</span> groenlandés (o kalaallisut)</li>
<li><span>km</span> camboyano (o jemer)</li>
<li><span>kn</span> canarés</li>
<li><span>ko</span> coreano</li>
<li><span>kr</span> kanuri</li>
<li><span>ks</span> cachemiro (o cachemir)</li>
<li><span>ku</span> kurdo</li>
<li><span>kv</span> komi</li>
<li><span>kw</span> córnico</li>
<li><span>ky</span> kirguís</li>
<li><span>la</span> latín</li>
<li><span>lb</span> luxemburgués</li>
<li><span>lg</span> luganda</li>
<li><span>li</span> limburgués</li>
<li><span>ln</span> lingala</li>
<li><span>lo</span> lao</li>
<li><span>lt</span> lituano</li>
<li><span>lu</span> luba-katanga (o chiluba)</li>
<li><span>lv</span> letón</li>
<li><span>mg</span> malgache (o malagasy)</li>
<li><span>mh</span> marshalés</li>
<li><span>mi</span> maorí</li>
<li><span>mk</span> macedonio</li>
<li><span>ml</span> malayalam</li>
<li><span>mn</span> mongol</li>
<li><span>mr</span> maratí</li>
<li><span>ms</span> malayo</li>
<li><span>mt</span> maltés</li>
<li><span>my</span> birmano</li>
<li><span>na</span> nauruano</li>
<li><span>nb</span> noruego bokmål</li>
<li><span>nd</span> ndebele del norte</li>
<li><span>ne</span> nepalí</li>
<li><span>ng</span> ndonga</li>
<li><span>nl</span> neerlandés (u holandés)</li>
<li><span>nn</span> nynorsk</li>
<li><span>no</span> noruego</li>
<li><span>nr</span> ndebele del sur</li>
<li><span>nv</span> navajo</li>
<li><span>ny</span> chichewa</li>
<li><span>oc</span> occitano</li>
<li><span>oj</span> ojibwa</li>
<li><span>om</span> oromo</li>
<li><span>or</span> oriya</li>
<li><span>os</span> osético (u osetio, u oseta)</li>
<li><span>pa</span> panyabí (o penyabi)</li>
<li><span>pi</span> pali</li>
<li><span>pl</span> polaco</li>
<li><span>ps</span> pastú (o pastún, o pashto)</li>
<li><span>pt</span> portugués</li>
<li><span>qc</span> quechua</li>
<li><span>rm</span> romanche</li>
<li><span>rn</span> kirundi</li>
<li><span>ro</span> rumano</li>
<li><span>ru</span> ruso</li>
<li><span>rw</span> ruandés (o kiñaruanda)</li>
<li><span>sa</span> sánscrito</li>
<li><span>sc</span> sardo</li>
<li><span>sd</span> sindhi</li>
        <li><span>se</span> sami septentrional</li>
<li><span>sg</span> sango</li>
<li><span>si</span> cingalés</li>
<li><span>sk</span> eslovaco</li>
<li><span>sl</span> esloveno</li>
<li><span>sm</span> samoano</li>
<li><span>sn</span> shona</li>
<li><span>so</span> somalí</li>
<li><span>sq</span> albanés</li>
<li><span>sr</span> serbio</li>
<li><span>ss</span> suazi (o swati, o siSwati)</li>
<li><span>st</span> sesotho</li>
<li><span>su</span> sundanés (o sondanés)</li>
<li><span>sv</span> sueco</li>
<li><span>sw</span> suajili</li>
<li><span>ta</span> tamil</li>
<li><span>te</span> télugu</li>
<li><span>tg</span> tayiko</li>
<li><span>th</span> tailandés</li>
<li><span>ti</span> tigriña</li>
<li><span>tk</span> turcomano</li>
<li><span>tl</span> tagalo</li>
<li><span>tn</span> setsuana</li>
<li><span>to</span> tongano</li>
<li><span>tr</span> turco</li>
<li><span>ts</span> tsonga</li>
<li><span>tt</span> tártaro</li>
<li><span>tw</span> twi</li>
<li><span>ty</span> tahitiano</li>
<li><span>ug</span> uigur</li>
<li><span>uk</span> ucraniano</li>
<li><span>ur</span> urdu</li>
<li><span>uz</span> uzbeko</li>
<li><span>ve</span> venda</li>
<li><span>vi</span> vietnamita</li>
<li><span>vo</span> volapük</li>
<li><span>wa</span> valón</li>
<li><span>wo</span> wolof</li>
<li><span>xh</span> xhosa</li>
<li><span>yi</span> yídish (o yidis, o yiddish)</li>
<li><span>yo</span> yoruba</li>
<li><span>za</span> chuan (o chuang, o zhuang)</li>
<li><span>zh</span> chino</li>
<li><span>zu</span> zulú</li>
    </ul>
</body>
</html>

    """
    bot.rpc.send_msg(accid, msg.chat_id,
                     MsgData(text="Listado de idiomas",html=list))


@cli.on(events.NewMessage(command="/help"))
def _help(bot: Bot, accid: int, event: AttrDict) -> None:
    send_help(bot, accid, event.msg.chat_id  )

def send_help(bot: Bot, accid: int, chat_id: int) -> None:
    texto = """
    **Comandos disponibles**

    **/tts** [lenguaje] [texto] - Convertir texto a voz
    **/tr**  [lenguaje] [texto] - Traducir texto a diferentes idiomas
    **/langs** - Listado de idiomas disponibles
    """
    bot.rpc.send_msg(accid, chat_id, MsgData(text=texto))


if __name__ == "__main__":
  cli.start()
