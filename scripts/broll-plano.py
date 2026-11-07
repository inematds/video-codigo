"""b-roll automático: vídeo de pessoa falando + transcrição com tempo por palavra → plano frase a frase + projeto pronto
para renderizar no molde assets/broll/. Sem API: só heurística local (o agente revisa e edita o plano depois).

Uso:
  python3 broll-plano.py --fala aula.mp4 --transcricao transcricao/transcript.json --projeto P [--rosto 0.58,0.42,0.30]
  python3 broll-plano.py --projeto P --replanejar        (refaz plano.js depois de editar P/plano.json à mão)

Transcrição aceita (o inemavox gera as duas primeiras com `transcrever_v1.py --words`):
  transcript.json [{start, end, text, words:[{word, start, end}]}] · words.json [{word, start, end}] ·
  tempos.json do voz.py ({palabras:[{texto, inicio, fin}]}) · tempos.json do r7ex ([{palavras:[{w, t, f}]}]) ·
  .srt (só tempo por legenda: as palavras são repartidas — prefira os formatos com palavra).

Três tratamentos, um por frase:
  rosto   a pessoa inteira, nada por cima — abertura, opinião, história, chamada final, fechamento.
  pip     a pessoa vai para um círculo no canto e a tela mostra o CONCEITO desenhado em traço (ícone + palavra).
  cheio   gráfico em tela cheia (número, comparação, lista/passos) e a voz continua — quando mostrar explica melhor.
Ritmo conferido: abre e fecha em rosto · rosto ≤ 8 s seguidos · cheio de 3 a 8 s · nunca dois cheios colados.
Cada visual tem uma âncora: o número cai NA palavra do número; o desenho do conceito começa ~0,25 s antes da palavra.

Saída em P/: plano.json (edite), plano.js (window.PLANO, o molde lê), plano.md (tabela para revisar), index.html +
broll.mjs + inema/ (o molde), quadros/ (os quadros do vídeo em JPG) e audio/fala.wav.
Depois: node scripts/checar-leitura.mjs --project P · node scripts/render-video.mjs --project P --output P/renders/x.mp4 --audio P/audio/fala.wav
Ideia da skill talking-head-b-roll (motion-skills, MIT) e do prompt "talking head → lineart"; código nosso.
"""
import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys
import unicodedata

AQUI = pathlib.Path(__file__).resolve().parent
KIT = AQUI.parent

PARADA = set("""a o as os um uma uns umas de da do das dos e é em no na nos nas por para pra com sem que se ser
foi era são está esta este isso isto essa esse aqui ali lá mais menos muito muita pouco já não sim ou mas como quando
onde também só tudo nada você vocês eu ele ela eles elas nós me te lhe seu sua meu minha teu tua ao aos à às pelo pela
pode podem precisa precisam vai vão ter tem tinha fazer faz depois antes então porque qual quais quem até sobre entre
cada todo toda todos todas outro outra mesmo mesma bem ainda agora hoje vem""".split())
NUM_PAL = {"zero": 0, "um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "tres": 3, "quatro": 4, "cinco": 5, "seis": 6,
           "sete": 7, "oito": 8, "nove": 9, "dez": 10, "onze": 11, "doze": 12, "quinze": 15, "vinte": 20, "trinta": 30,
           "quarenta": 40, "cinquenta": 50, "sessenta": 60, "setenta": 70, "oitenta": 80, "noventa": 90, "cem": 100,
           "cento": 100, "mil": 1000, "metade": 0.5, "dobro": 2, "triplo": 3}
PESSOAL = re.compile(r"\b(eu|meu|minha|acho|comenta\w*|coment[aá]rios?|link|inema|imagine|lembr\w+|confesso)\b", re.I)
PASSOS = re.compile(r"\b(passos?|etapas?|primeiro|segundo|terceiro|depois|por fim|fases?)\b", re.I)
COMPARA = re.compile(r"\b(contra|versus|mais que|menos que|vezes|em vez de|antes|depois)\b", re.I)
# conceito → ícone do molde (assets/broll/broll.mjs, ICONES). O mais específico primeiro.
ICONE = [
    (r"ferrament", "ferramenta"), (r"tarefa|atividade|lista|checklist", "lista"), (r"m[eé]todo|processo|sistema|automat", "engrenagem"),
    (r"tempo|hora|minuto|r[aá]pid|demor", "relogio"), (r"err|falh|problema|risco", "alerta"), (r"respost|pergunt|pedido|prompt|convers", "balao"),
    (r"intelig|\bia\b|modelo|chip|computador|m[aá]quina", "chip"), (r"c[oó]digo|program|software|app", "codigo"),
    (r"result|meta|objetiv|foco|alvo", "alvo"), (r"confer|revis|verific|med[ei]|analis", "lupa"), (r"dinheiro|custo|pre[cç]o|pag|venda|lucro", "cifrao"),
    (r"ideia|criat|descobr|aprend", "lampada"), (r"pequen|come[cç]|semente|cresc", "semente"), (r"esfor[cç]|trabalh|energia", "raio"),
    (r"pessoa|cliente|equipe|gente|aluno", "pessoa"), (r"livro|curso|aula|estud", "livro"), (r"lan[cç]|acelera|escal", "foguete"),
    (r"dado|n[uú]mero|gr[aá]fico|cresce", "grafico"), (r"nuvem|internet|online|site", "nuvem"),
]


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def ler_palavras(arq):
    p = pathlib.Path(arq)
    if p.suffix.lower() == ".srt":
        out = []
        for bloco in re.split(r"\n\s*\n", p.read_text(encoding="utf-8").strip()):
            ls = bloco.strip().splitlines()
            m = next((re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", l) for l in ls if "-->" in l), None)
            if not m:
                continue
            g = [int(x) for x in m.groups()]
            a, b = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000, g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
            ws = " ".join(ls[[i for i, l in enumerate(ls) if "-->" in l][0] + 1:]).split()
            for i, w in enumerate(ws):   # SRT não tem tempo por palavra: reparte
                out.append({"w": w, "t": a + (b - a) * i / len(ws), "f": a + (b - a) * (i + 1) / len(ws)})
        return out
    d = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(d, dict) and "palabras" in d:
        return [{"w": x["texto"], "t": x["inicio"], "f": x["fin"]} for x in d["palabras"]]
    if isinstance(d, dict) and "segments" in d:
        d = d["segments"]
    if isinstance(d, list) and d and "palavras" in d[0]:
        return [{"w": x["w"], "t": x["t"], "f": x["f"]} for s in d for x in s["palavras"]]
    if isinstance(d, list) and d and "words" in d[0]:
        return [{"w": x["word"], "t": x["start"], "f": x["end"]} for s in d for x in s["words"]]
    if isinstance(d, list) and d and "word" in d[0]:
        return [{"w": x["word"], "t": x["start"], "f": x["end"]} for x in d]
    sys.exit(f"Formato de transcrição não reconhecido: {arq} (precisa de tempo por palavra; ver --help)")


def frases(pal, max_dur=9.0):
    """Corta no fim de frase (. ? !) ou em pausa ≥ 0,6 s; frase longa (> max_dur) corta também na vírgula."""
    out, cur = [], []
    for i, w in enumerate(pal):
        cur.append(w)
        prox = pal[i + 1] if i + 1 < len(pal) else None
        fim = re.search(r"[.?!…]$", w["w"]) or prox is None or prox["t"] - w["f"] >= 0.6
        virg = w["w"].endswith((",", ";", ":")) and cur[-1]["f"] - cur[0]["t"] > max_dur * 0.55
        if fim or virg:
            out.append(cur); cur = []
    return [x for x in out if x]


def numeros(ws):
    """[(valor, índice da palavra)] — algarismos (com %, mil, mi) e números por extenso."""
    out = []
    for i, w in enumerate(ws):
        s = sem_acento(w["w"]).strip(".,;:!?\"()")
        m = re.fullmatch(r"(\d+(?:[.,]\d+)?)(%|x|mil|mi)?", s)
        if m:
            v = float(m.group(1).replace(",", "."))
            out.append((v, i, m.group(2) or "")); continue
        if s in NUM_PAL and s not in ("um", "uma"):
            out.append((NUM_PAL[s], i, ""))
    # "por cento" logo depois
    return [(v, i, u or ("%" if i + 2 < len(ws) and sem_acento(ws[i + 1]["w"]) == "por" and sem_acento(ws[i + 2]["w"]).startswith("cento") else ""))
            for v, i, u in out]


def conceito(ws):
    """A palavra que carrega a frase (substantivo comprido, não comum) e o ícone que a desenha."""
    cands = []
    for i, w in enumerate(ws):
        s = re.sub(r"[^\wà-ú]", "", w["w"].lower())
        if len(s) < 4 or sem_acento(s) in {sem_acento(x) for x in PARADA} or s.isdigit():
            continue
        icone = next((ic for rx, ic in ICONE if re.search(rx, sem_acento(s))), None)
        cands.append((bool(icone), len(s), -i, i, s, icone))
    if not cands:
        return None, "lampada", 0
    cands.sort(reverse=True)
    _, _, _, i, s, icone = cands[0]
    return s, icone or "lampada", i


def classificar(ws, idx, total):
    txt = " ".join(w["w"] for w in ws)
    dur = ws[-1]["f"] - ws[0]["t"]
    nums = numeros(ws)
    if idx == 0:
        return "rosto", "abertura: o público conhece quem fala", None
    if idx == total - 1:
        return "rosto", "fechamento: termina na pessoa", None
    if PESSOAL.search(txt) and not nums:
        return "rosto", "fala pessoal / chamada: a pessoa é o assunto", None
    itens = [x.strip() for x in re.split(r"[,:;]| e ", txt) if len(x.strip().split()) >= 1]
    if PASSOS.search(txt) and len(itens) >= 3:
        return "cheio", "sequência de passos: mostrar ordena melhor que falar", "passos"
    if len(nums) >= 2 and (COMPARA.search(txt) or len(nums) == 2):
        return "cheio", "dois números: comparação em barras", "comparacao"
    if nums and dur >= 2.0:
        return "cheio", "número na fala: ele aparece cheio, na palavra", "numero"
    return "pip", "um conceito: desenhado em traço, pessoa no canto", None


def visual(ws, trat, tipo):
    s, icone, i = conceito(ws)
    base = {"titulo": (s or "").upper(), "icone": icone, "ancora": round(max(ws[0]["t"], ws[i]["t"] - 0.25), 3),
            "palavra": ws[i]["w"] if s else ""}
    if trat == "pip":
        return {"tipo": "traco", **base}
    if trat == "rosto":   # o título só aparece no modo meia tela (a outra metade)
        return {"tipo": "nenhum", "titulo": base["titulo"], "entra": round(ws[0]["t"] + 0.2, 3)}
    nums = numeros(ws)
    if tipo == "numero":
        v, j, u = nums[0]
        return {"tipo": "numero", "numero": v, "unidade": u, "rotulo": base["titulo"], "icone": icone, "ancora": ws[j]["t"],
                "palavra": ws[j]["w"]}
    if tipo == "comparacao":
        (v1, j1, u1), (v2, j2, u2) = nums[:2]
        return {"tipo": "comparacao", "itens": [{"valor": v1, "unidade": u1, "t": ws[j1]["t"], "rotulo": ws[max(0, j1 - 1)]["w"] if j1 else ""},
                                                {"valor": v2, "unidade": u2, "t": ws[j2]["t"], "rotulo": ws[max(0, j2 - 1)]["w"] if j2 else ""}],
                "titulo": base["titulo"], "ancora": ws[j1]["t"]}
    # passos: cada pedaço (entre vírgulas / "e") vira um item que entra quando começa a ser dito
    itens, cur = [], []
    for w in ws:
        if sem_acento(w["w"]) == "e" and len(cur) >= 2:   # "testar X e conferir Y" = dois itens
            itens.append(cur); cur = []; continue
        cur.append(w)
        if w["w"].endswith((",", ":", ";", ".")):
            itens.append(cur); cur = []
    if cur:
        itens.append(cur)
    itens = [x for x in itens if x]
    cab = None
    if len(itens) > 2 and len(itens[0]) <= 5 and PASSOS.search(" ".join(w["w"] for w in itens[0])):
        cab = itens.pop(0)   # "São três passos:" vira o título
    return {"tipo": "passos", "titulo": " ".join(w["w"] for w in cab).strip(":,. ").upper() if cab else base["titulo"],
            "itens": [{"texto": " ".join(w["w"] for w in it).strip(",:;. ").removeprefix("e ").strip(), "t": it[0]["t"]} for it in itens[:5]],
            "ancora": itens[0][0]["t"] if itens else ws[0]["t"]}


def leitura(txt):
    """Tempo de ler um texto na tela — a mesma regra do scripts/checar-leitura.mjs."""
    txt = str(txt or "")
    pal = len([w for w in txt.split() if re.search(r"\w", w)])
    letras = len(re.sub(r"\s", "", txt))
    return max(1.5, 1.0 + 0.3 * pal, 1.0 + letras / 15) if txt else 0.0


def segurar(plano, avisos):
    """Cada texto do visual precisa ficar o tempo de ser lido: se a frase acaba antes, o visual segura ('fim_visual')
    sobre a frase seguinte; se engolir a seguinte quase toda, ela vira 'segue'."""
    for i, p in enumerate(plano):
        v = p["visual"]
        if p["tratamento"] == "rosto" and v.get("titulo") and p["fim"] - p["inicio"] < leitura(v["titulo"]) + 0.7:
            v.pop("titulo")   # frase curta demais para ler a palavra na meia tela: a metade fica limpa
        if p["tratamento"] not in ("pip", "cheio"):
            continue
        if v["tipo"] == "traco":
            v["entra"] = round(p["inicio"] + 0.2, 3)
            req = [v["entra"] + leitura(v.get("titulo"))]
        elif v["tipo"] == "numero":
            req = [v["ancora"] + 0.05 + leitura(v.get("rotulo")), v["ancora"] + leitura(str(v.get("numero")))]
        elif v["tipo"] == "comparacao":
            req = [it["t"] + leitura(str(it["valor"])) for it in v.get("itens", [])] + [v["ancora"] - .6 + leitura(v.get("titulo"))]
        else:
            req = [it["t"] - 0.2 + leitura(it["texto"]) for it in v.get("itens", [])] + [v["ancora"] - .5 + leitura(v.get("titulo"))]
        fim_v = round(max([p["fim"]] + req) + 0.25, 3)
        prox = plano[i + 1] if i + 1 < len(plano) else None
        if prox is None or fim_v <= prox["inicio"]:
            continue
        p["fim_visual"] = fim_v
        if prox["fim"] - fim_v < 1.0 and i + 1 < len(plano) - 1:
            prox["tratamento"], prox["motivo"], prox["visual"] = "segue", "o visual anterior ainda está sendo lido", {"tipo": "nenhum"}
        elif i + 1 == len(plano) - 1 and prox["fim"] - fim_v < 1.0:
            avisos.append(f"{p['id']}: o texto não cabe antes do fechamento — encurte o texto na tela")


def ritmo(plano):
    """Aplica as regras de ritmo e devolve os avisos que sobraram."""
    avisos = []
    # traço curto (< 1,8 s) não dá tempo de ler o conceito: volta ao rosto (uma volta curta à pessoa também dá ritmo)
    for i, p in enumerate(plano):
        if p["tratamento"] == "pip" and p["fim"] - p["inicio"] < 1.8:
            p["tratamento"], p["motivo"], p["visual"] = "rosto", f"frase curta ({p['fim'] - p['inicio']:.1f} s) para desenhar um conceito", {"tipo": "nenhum"}
    # nunca dois cheios colados: o segundo vira pip
    for a, b in zip(plano, plano[1:]):
        if a["tratamento"] == b["tratamento"] == "cheio":
            b["tratamento"], b["motivo"] = "pip", "ia ser cheio colado no anterior: virou traço (volta ao rosto no canto)"
            b["visual"] = {"tipo": "traco", **{k: v for k, v in b["visual"].items() if k in ("titulo", "icone", "ancora", "palavra")}}
            b["visual"].setdefault("titulo", ""); b["visual"].setdefault("icone", "lampada")
    # cheio curto (< 3 s) estica sobre a frase seguinte se ela não for rosto de abertura/fecho; senão vira pip
    for i, p in enumerate(plano):
        if p["tratamento"] == "cheio" and p["fim"] - p["inicio"] < 3.0:
            if i + 1 < len(plano) - 1 and plano[i + 1]["tratamento"] == "pip":
                p["fim_visual"] = plano[i + 1]["fim"]; plano[i + 1]["tratamento"] = "segue"
                plano[i + 1]["motivo"] = "continua o gráfico da frase anterior (cheio precisa de ≥ 3 s)"
            else:
                avisos.append(f"{p['id']}: cheio de {p['fim'] - p['inicio']:.1f} s (< 3 s) — considere juntar com a vizinha")
        if p["tratamento"] == "cheio" and p["fim"] - p["inicio"] > 8.0:
            avisos.append(f"{p['id']}: cheio de {p['fim'] - p['inicio']:.1f} s (> 8 s) — volte ao rosto no meio")
    # rosto seguido > 8 s: a frase do meio do trecho vira pip
    i = 0
    while i < len(plano):
        j = i
        while j + 1 < len(plano) and plano[j + 1]["tratamento"] == "rosto":
            j += 1
        if plano[i]["tratamento"] == "rosto" and plano[j]["fim"] - plano[i]["inicio"] > 8.0 and j > i:
            meio = [k for k in range(i, j + 1) if 0 < k < len(plano) - 1]
            if meio:
                k = meio[len(meio) // 2]
                plano[k]["tratamento"], plano[k]["motivo"] = "pip", "quebra um trecho de rosto com mais de 8 s"
                s, ic, a = conceito(plano[k]["_ws"])
                plano[k]["visual"] = {"tipo": "traco", "titulo": (s or "").upper(), "icone": ic,
                                      "ancora": round(max(plano[k]["_ws"][0]["t"], plano[k]["_ws"][a]["t"] - .25), 3), "palavra": plano[k]["_ws"][a]["w"]}
                continue
            avisos.append(f"{plano[i]['id']}–{plano[j]['id']}: rosto por {plano[j]['fim'] - plano[i]['inicio']:.1f} s (> 8 s)")
        i = j + 1
    segurar(plano, avisos)
    if plano[0]["tratamento"] != "rosto": avisos.append("não abre no rosto")
    if plano[-1]["tratamento"] != "rosto": avisos.append("não fecha no rosto")
    return avisos


def sonda(video):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate:format=duration",
                        "-of", "json", str(video)], capture_output=True, text=True, check=True)
    d = json.loads(r.stdout); s = d["streams"][0]
    n, m = s["r_frame_rate"].split("/")
    return int(s["width"]), int(s["height"]), round(int(n) / int(m)), float(d["format"]["duration"])


def gravar(P, cfg, plano, avisos):
    limpo = [{k: v for k, v in p.items() if not k.startswith("_")} for p in plano]
    dados = {**cfg, "frases": limpo, "avisos": avisos}
    (P / "plano.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1))
    (P / "plano.js").write_text("window.PLANO=" + json.dumps(dados, ensure_ascii=False) + ";\n")
    linhas = ["# Plano de b-roll — revise e edite plano.json, depois `broll-plano.py --projeto P --replanejar`\n",
              "| # | tempo | tratamento | o que é dito | na tela | por quê |", "|---|---|---|---|---|---|"]
    for p in limpo:
        v = p["visual"]
        tipo = v["tipo"]
        if tipo == "traco": tela = f"traço: {v.get('icone')} + «{v.get('titulo')}»"
        elif tipo == "numero": tela = f"número {v.get('numero')}{v.get('unidade', '')} em «{v.get('palavra')}»"
        elif tipo == "comparacao": tela = "barras " + " × ".join(str(x["valor"]) for x in v.get("itens", []))
        elif tipo == "passos": tela = f"«{v.get('titulo')}»: " + " / ".join(x["texto"] for x in v.get("itens", []))
        else: tela = "—"
        if p["tratamento"] == "segue": tela = "(continua o gráfico anterior)"
        linhas.append(f"| {p['id']} | {p['inicio']:.1f}–{p['fim']:.1f} | {p['tratamento']} | {p['texto']} | {tela} | {p['motivo']} |")
    if avisos:
        linhas += ["", "Avisos:"] + [f"- {a}" for a in avisos]
    (P / "plano.md").write_text("\n".join(linhas) + "\n")
    return limpo


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fala", help="vídeo da pessoa falando (mp4)")
    ap.add_argument("--transcricao", help="transcript.json / words.json / tempos.json / .srt")
    ap.add_argument("--projeto", required=True, help="pasta do projeto b-roll (é criada)")
    ap.add_argument("--rosto", default="0.5,0.42,0.30", help="centro x, centro y e raio do rosto, em fração da ALTURA p/ o raio (padrão 0.5,0.42,0.30)")
    ap.add_argument("--rosto-tamanho", default="inteiro", choices=["inteiro", "meia"],
                    help="tratamento rosto: tela inteira (padrão) ou meia tela (regra INEMA de avatar: no máximo meia tela)")
    ap.add_argument("--replanejar", action="store_true", help="só refaz plano.js/plano.md a partir do plano.json editado")
    ap.add_argument("--sem-quadros", action="store_true", help="não extrai os quadros (já extraídos)")
    a = ap.parse_args()
    P = pathlib.Path(a.projeto).resolve()

    if a.replanejar:
        d = json.loads((P / "plano.json").read_text())
        frs = d.pop("frases"); d.pop("avisos", None)
        gravar(P, d, frs, [])
        print(f"plano.js refeito ({len(frs)} frases) → {P}")
        return
    if not (a.fala and a.transcricao):
        sys.exit("Precisa de --fala e --transcricao (ou --replanejar).")
    P.mkdir(parents=True, exist_ok=True)
    W, H, fps, dur = sonda(a.fala)
    pal = ler_palavras(a.transcricao)
    if not pal:
        sys.exit("Transcrição sem palavras.")
    grupos = []
    for g in frases(pal):
        if grupos and g[-1]["f"] - g[0]["t"] < 0.8:      # caco de < 0,8 s (palavra repetida pelo Whisper) junta na anterior
            grupos[-1] += g; continue
        if grupos and len(grupos[-1]) <= 5 and PASSOS.search(" ".join(w["w"] for w in grupos[-1])) and numeros(grupos[-1]):
            grupos[-1] += g; continue                    # "São três passos." + a frase com os passos = um gráfico só
        grupos.append(g)
    plano = []
    for i, ws in enumerate(grupos):
        trat, motivo, tipo = classificar(ws, i, len(grupos))
        plano.append({"id": f"f{i + 1:02d}", "inicio": round(ws[0]["t"], 3), "fim": round(ws[-1]["f"], 3),
                      "texto": " ".join(w["w"] for w in ws), "tratamento": trat, "motivo": motivo, "visual": visual(ws, trat, tipo),
                      "palavras": [[w["w"], round(w["t"], 3), round(w["f"], 3)] for w in ws], "_ws": ws})
    avisos = ritmo(plano)
    cx, cy, r = (float(x) for x in a.rosto.split(","))
    cfg = {"video": {"largura": W, "altura": H, "fps": fps, "duracao": round(dur, 3), "quadros": "quadros/%05d.jpg"},
           "rosto": {"cx": cx, "cy": cy, "r": r, "tamanho": a.rosto_tamanho}, "cores": {"amarelo": "#FACC15", "preto": "#0c0c10"}}

    # molde + tema + quadros + áudio
    for f in ("index.html", "broll.mjs"):
        shutil.copy(KIT / "assets/broll" / f, P / f)
    if not (P / "inema").exists():
        shutil.copytree(KIT / "assets/inema", P / "inema")
    (P / "audio").mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.fala, "-vn", "-ac", "2", "-ar", "48000", str(P / "audio/fala.wav")], check=True)
    if not a.sem_quadros:
        q = P / "quadros"
        q.mkdir(exist_ok=True)
        print(f"extraindo {int(dur * fps)} quadros ({W}×{H}, {fps} fps)…", flush=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.fala, "-vf", f"fps={fps}", "-q:v", "3", str(q / "%05d.jpg")], check=True)
    cfg["video"]["n_quadros"] = len(list((P / "quadros").glob("*.jpg")))
    if not cfg["video"]["n_quadros"]:
        sys.exit("Sem quadros em P/quadros (rode sem --sem-quadros).")
    limpo = gravar(P, cfg, plano, avisos)
    cont = {}
    for p in limpo:
        cont[p["tratamento"]] = cont.get(p["tratamento"], 0) + 1
    print(f"{len(limpo)} frases · " + " · ".join(f"{k} {v}" for k, v in cont.items()) + f" → {P}/plano.md")
    for x in avisos:
        print("  ⚠ " + x)


if __name__ == "__main__":
    main()
