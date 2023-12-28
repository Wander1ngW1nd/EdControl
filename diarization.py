from pydub import AudioSegment
from pyannote.audio import Pipeline
from datetime import timedelta
import torch
import re
import whisper
import json
import os
from audio_extract import extract_audio

# videoFile - переменная берется из video_analyse.py далее превращается в audio.wav и далее работа идет с этим файлом

# convert_video = os.VIDEO_PATH.join(VIDEO_PATH, videoFile.name)
def path_for_audio(path,video_file):
    convert_video = os.path.join(path, video_file)
    extract_audio(input_path=convert_video, output_path="./audio.wav", output_format='wav', overwrite=True)
    pass

def millisec(timeStr):
    spl = timeStr.split(":")
    s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
    return s

def timeStr(t):
        return '{0:02d}:{1:02d}:{2:06.2f}'.format(round(t // 3600), 
                                                    round(t % 3600 // 60), 
                                                    t % 60)

def dz_result(audio_wav):
    spacermilli = 2000
    spacer = AudioSegment.silent(duration=spacermilli)
    audio = AudioSegment.from_wav(audio_wav) # Указать откуда этот файл приходит
    audio = spacer.append(audio, crossfade=0)
    audio.export('input_prep.wav', format='wav')

    pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token= ('INPUT TOKEN') or True ) # Тут надо вписать токен с HuggingFace
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pipeline.to(device)

    DEMO_FILE = {'uri': 'blabla', 'audio': 'input_prep.wav'}
    dz = pipeline(DEMO_FILE)  

    with open("diarization.txt", "w") as text_file:
        text_file.write(str(dz))

    dzs = open('diarization.txt').read().splitlines()

    groups = []
    g = []
    lastend = 0

    for d in dzs:   
        if g and (g[0].split()[-1] != d.split()[-1]):      #same speaker
            groups.append(g)
            g = []
    
        g.append(d)
    
        end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=d)[1]
        end = millisec(end)
        if (lastend > end):       #segment engulfed by a previous segment
            groups.append(g)
            g = [] 
        else:
            lastend = end
        if g:
            groups.append(g)

    audio = AudioSegment.from_wav("input_prep.wav")
    gidx = -1
    for g in groups:
        start = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0]
        end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[-1])[1]
        start = millisec(start) #- spacermilli
        end = millisec(end)  #- spacermilli
        gidx += 1
        audio[start:end].export(str(gidx) + '.wav', format='wav')
        print(f"group {gidx}: {start}--{end}")

    del   DEMO_FILE, pipeline, spacer,  audio, dz

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = whisper.load_model('small', device = device)                         # ВЫБОР РАЗМЕРА МОДЕЛИ 

    for i in range(len(groups)):
        audiof = str(i) + '.wav'
        result = model.transcribe(audio=audiof, language='ru', word_timestamps=True)#, initial_prompt=result.get('text', ""))
        with open(str(i)+'.json', "w") as outfile:
            json.dump(result, outfile, indent=4) 

    speakers = {'SPEAKER_00':('Teacher', '#e1ffc7', 'darkgreen'), 'SPEAKER_01':('Student', 'white', 'darkorange') }
    def_boxclr = 'white'
    def_spkrclr = 'orange'

    audio_title = 'Online Education'

    preS = '\n<!DOCTYPE html>\n<html lang="ru">\n\n<head>\n\t<meta charset="UTF-8">\n\t<meta name="viewport" content="whtmlidth=device-width, initial-scale=1.0">\n\t<meta http-equiv="X-UA-Compatible" content="ie=edge">\n\t<title>' + \
    audio_title+ \
    '</title>\n\t<style>\n\t\tbody {\n\t\t\tfont-family: sans-serif;\n\t\t\tfont-size: 14px;\n\t\t\tcolor: #111;\n\t\t\tpadding: 0 0 1em 0;\n\t\t\tbackground-color: #efe7dd;\n\t\t}\n\n\t\ttable {\n\t\t\tborder-spacing: 10px;\n\t\t}\n\n\t\tth {\n\t\t\ttext-align: left;\n\t\t}\n\n\t\t.lt {\n\t\t\tcolor: inherit;\n\t\t\ttext-decoration: inherit;\n\t\t}\n\n\t\t.l {\n\t\t\tcolor: #050;\n\t\t}\n\n\t\t.s {\n\t\t\tdisplay: inline-block;\n\t\t}\n\n\t\t.c {\n\t\t\tdisplay: inline-block;\n\t\t}\n\n\t\t.e {\n\t\t\t/*background-color: white; Changing background color */\n\t\t\tborder-radius: 10px;\n\t\t\t/* Making border radius */\n\t\t\twidth: 50%;\n\t\t\t/* Making auto-sizable width */\n\t\t\tpadding: 0 0 0 0;\n\t\t\t/* Making space around letters */\n\t\t\tfont-size: 14px;\n\t\t\t/* Changing font size */\n\t\t\tmargin-bottom: 0;\n\t\t}\n\n\t\t.t {\n\t\t\tdisplay: inline-block;\n\t\t}\n\n\t\t#player-div {\n\t\t\tposition: sticky;\n\t\t\ttop: 20px;\n\t\t\tfloat: right;\n\t\t\twidth: 40%\n\t\t}\n\n\t\t#player {\n\t\t\taspect-ratio: 16 / 9;\n\t\t\twidth: 100%;\n\t\t\theight: auto;\n\t\t}\n\n\t\ta {\n\t\t\tdisplay: inline;\n\t\t}\n\t</style>';
    preS += '\n\t<script>\n\twindow.onload = function () {\n\t\t\tvar player = document.getElementById("audio_player");\n\t\t\tvar player;\n\t\t\tvar lastword = null;\n\n\t\t\t// So we can compare against new updates.\n\t\t\tvar lastTimeUpdate = "-1";\n\n\t\t\tsetInterval(function () {\n\t\t\t\t// currentTime is checked very frequently (1 millisecond),\n\t\t\t\t// but we only care about whole second changes.\n\t\t\t\tvar ts = (player.currentTime).toFixed(1).toString();\n\t\t\t\tts = (Math.round((player.currentTime) * 5) / 5).toFixed(1);\n\t\t\t\tts = ts.toString();\n\t\t\t\tconsole.log(ts);\n\t\t\t\tif (ts !== lastTimeUpdate) {\n\t\t\t\t\tlastTimeUpdate = ts;\n\n\t\t\t\t\t// Its now up to you to format the time.\n\t\t\t\t\tword = document.getElementById(ts)\n\t\t\t\t\tif (word) {\n\t\t\t\t\t\tif (lastword) {\n\t\t\t\t\t\t\tlastword.style.fontWeight = "normal";\n\t\t\t\t\t\t}\n\t\t\t\t\t\tlastword = word;\n\t\t\t\t\t\t//word.style.textDecoration = "underline";\n\t\t\t\t\t\tword.style.fontWeight = "bold";\n\n\t\t\t\t\t\tlet toggle = document.getElementById("autoscroll");\n\t\t\t\t\t\tif (toggle.checked) {\n\t\t\t\t\t\t\tlet position = word.offsetTop - 20;\n\t\t\t\t\t\t\twindow.scrollTo({\n\t\t\t\t\t\t\t\ttop: position,\n\t\t\t\t\t\t\t\tbehavior: "smooth"\n\t\t\t\t\t\t\t});\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}, 0.1);\n\t\t}\n\n\t\tfunction jumptoTime(timepoint, id) {\n\t\t\tvar player = document.getElementById("audio_player");\n\t\t\thistory.pushState(null, null, "#" + id);\n\t\t\tplayer.pause();\n\t\t\tplayer.currentTime = timepoint;\n\t\t\tplayer.play();\n\t\t}\n\t\t</script>\n\t</head>';
    preS += '\n\n<body>\n\t<h2>' + audio_title + '</h2>\n\t<i>Click on a part of the transcription, to jump to its portion of audio, and get an anchor to it in the address\n\t\tbar<br><br></i>\n\t<div id="player-div">\n\t\t<div id="player">\n\t\t\t<audio controls="controls" id="audio_player">\n\t\t\t\t<source src="input.wav" />\n\t\t\t</audio>\n\t\t</div>\n\t\t<div><label for="autoscroll">auto-scroll: </label>\n\t\t\t<input type="checkbox" id="autoscroll" checked>\n\t\t</div>\n\t</div>\n';

    postS = '\t</body>\n</html>'

    html = list(preS)
    txt = list("")
    gidx = -1
    for g in groups:  
        shift = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0]
        shift = millisec(shift) - spacermilli #the start time in the original video
        shift=max(shift, 0)
        
        gidx += 1
        
        captions = json.load(open(str(gidx) + '.json'))['segments']

        if captions:
            speaker = g[0].split()[-1]
            boxclr = def_boxclr
            spkrclr = def_spkrclr
            if speaker in speakers:
                speaker, boxclr, spkrclr = speakers[speaker] 
            
            html.append(f'<div class="e" style="background-color: {boxclr}">\n');
            html.append('<p  style="margin:0;padding: 5px 10px 10px 10px;word-wrap:normal;white-space:normal;">\n')
            html.append(f'<span style="color:{spkrclr};font-weight: bold;">{speaker}</span><br>\n\t\t\t\t')
        
        for c in captions:
            start = shift + c['start'] * 1000.0 
            start = start / 1000.0   #time resolution ot youtube is Second.            
            end = (shift + c['end'] * 1000.0) / 1000.0      
            txt.append(f'[{timeStr(start)} --> {timeStr(end)}] [{speaker}] {c["text"]}\n')

            for i, w in enumerate(c['words']):
                if w == "":
                    continue
                start = (shift + w['start']*1000.0) / 1000.0        
                #end = (shift + w['end']) / 1000.0   #time resolution ot youtube is Second.  
                html.append(f'<a href="#{timeStr(start)}" id="{"{:.1f}".format(round(start*5)/5)}" class="lt" onclick="jumptoTime({int(start)}, this.id)">{w["word"]}</a><!--\n\t\t\t\t-->')
        #html.append('\n')      
        html.append('</p>\n')
        html.append(f'</div>\n')

    html.append(postS)


    with open(f"capspeaker.txt", "w", encoding='utf-8') as file:
        s = "".join(txt)
        file.write(s)
        print('captions saved to capspeaker.txt:')
        print(s+'\n')

    with open(f"capspeaker.html", "w", encoding='utf-8') as file:    #TODO: proper html embed tag when video/audio from file
        s = "".join(html)
        file.write(s)
        print('captions saved to capspeaker.html:')
        print(s+'\n')
    pass
