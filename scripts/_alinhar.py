"""Ajudante do voz.py — roda no Python do inemavox (faster-whisper + soundfile).
Uso: python _align.py <pedido.json> <saida.json>
pedido = {"lang": "pt", "segs": [{"wav": ..., "text": ...}, ...]}
Para cada frase: corta o silêncio da ponta, transcreve com tempo por palavra e mede a semelhança com o texto.
Saída = {"segs": [{"wav": <cortado>, "dur": s, "words": [[w, a, b]], "heard": "...", "sim": 0..1, "num_ok": bool, "nums": [...]}]}
Números: 0–999 escritos em algarismo viram palavra nos dois lados ("20" = "vinte"), e um número ouvido como OUTRO número
(ou que sumiu) reprova a frase mesmo com semelhança alta (num_ok = false). Frase curta (< 1,5 s) ganha 0,6 s de silêncio
nas pontas antes do Whisper — sem isso ele erra mais. (Ideias do asr_check do lemo-opuscar, MIT; código nosso, em PT.)"""
import sys, json, re, difflib, unicodedata, fcntl
import numpy as np, soundfile as sf

req = json.load(open(sys.argv[1]))


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9%]", "", w)


UN = "zero um dois tres quatro cinco seis sete oito nove dez onze doze treze quatorze quinze dezesseis dezessete dezoito dezenove".split()
DEZ = "x x vinte trinta quarenta cinquenta sessenta setenta oitenta noventa".split()
CEM = "x cento duzentos trezentos quatrocentos quinhentos seiscentos setecentos oitocentos novecentos".split()
NUMS = set(UN + DEZ[2:] + CEM[1:] + ["cem", "catorze", "mil"]) - {"um"}   # "um/uma" é quase sempre artigo


def num_pt(n):
    """0–999 → palavras: 25 → vinte e cinco, 100 → cem, 105 → cento e cinco"""
    if n == 100: return ["cem"]
    out = []
    if n >= 100: out.append(CEM[n // 100]); n %= 100
    if n >= 20: out += (["e"] if out else []) + [DEZ[n // 10]]; n %= 10
    if n or not out: out += (["e"] if out else []) + [UN[n]]
    return out


def tokens(texto):
    """Palavras para comparar: minúsculas sem acento; inteiros 0–999 viram palavra; uma/duas = um/dois; catorze = quatorze."""
    out = []
    texto = re.sub(r"(?<=\d)\s*[x×:/]\s*(?=\d)", " por ", texto)   # 16x9, 16:9, 9/16 = "dezesseis por nove"
    for raw in texto.split():
        core = raw.strip('.,;:!?"()[]«»…')
        if re.fullmatch(r"0|[1-9]\d{0,2}", core): out += num_pt(int(core)); continue
        w = norm(raw)
        if w: out.append({"uma": "um", "duas": "dois", "catorze": "quatorze"}.get(w, w))
    return out


def trim(path):
    a, sr = sf.read(path, dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    thr = 10 ** (-38 / 20) * max(1e-6, float(np.abs(a).max()))
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx):
        pad = int(sr * 0.06)
        a = a[max(0, idx[0] - pad): min(len(a), idx[-1] + pad)]
    out = path.replace(".wav", "_t.wav")
    sf.write(out, a, sr)
    return out, len(a) / sr


# Um Whisper por vez na máquina (mesmo lock do explicavideos: GPU dividida).
with open("/tmp/explicavideos-whisper.lock", "w") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    from faster_whisper import WhisperModel
    try:
        model = WhisperModel(req.get("model", "large-v3"), device="cuda", compute_type="float16")
    except Exception:
        model = WhisperModel(req.get("model", "large-v3"), device="cpu", compute_type="int8")
    res = []
    for sg in req["segs"]:
        wav, dur = trim(sg["wav"])
        pad = 0.6 if dur < 1.5 else 0.0
        src = wav
        if pad:   # frase curta: silêncio nas pontas só para o Whisper ouvir
            a, sr = sf.read(wav, dtype="float32")
            src = wav.replace(".wav", "_p.wav"); z = np.zeros(int(sr * pad), dtype="float32")
            sf.write(src, np.concatenate([z, a, z]), sr)
        segs, _ = model.transcribe(src, language=req.get("lang", "pt"), word_timestamps=True,
                                   condition_on_previous_text=False, initial_prompt=req.get("prompt", "INEMA, Nei Maldaner."))
        heard = [(w.word.strip(), max(0.0, float(w.start) - pad), max(0.0, float(w.end) - pad)) for s in segs for w in (s.words or []) if w.word.strip()]
        want = sg["text"].split()
        a, b = [norm(w) for w in want], [norm(h[0]) for h in heard]
        ta, tb = tokens(sg["text"]), tokens(" ".join(h[0] for h in heard))
        sim = difflib.SequenceMatcher(None, ta, tb).ratio() if ta else 0.0
        na, nb = [w for w in ta if w in NUMS], [w for w in tb if w in NUMS]
        # tempo de cada palavra do ROTEIRO (grafia certa na legenda); sem par = interpolado
        times = [None] * len(want)
        for blk in difflib.SequenceMatcher(None, a, b).get_matching_blocks():
            for k in range(blk.size):
                h = heard[blk.b + k]; times[blk.a + k] = [h[1], h[2]]
        known = [i for i, t in enumerate(times) if t]
        for i in range(len(want)):
            if times[i]: continue
            lo = max([k for k in known if k < i], default=None); hi = min([k for k in known if k > i], default=None)
            t0 = times[lo][1] if lo is not None else 0.0
            t1 = times[hi][0] if hi is not None else dur
            n0 = lo if lo is not None else -1; n1 = hi if hi is not None else len(want)
            step = (t1 - t0) / max(1, n1 - n0 - 1)
            times[i] = [t0 + step * (i - n0 - 1) + 0.01, t0 + step * (i - n0) - 0.01]
        res.append({"wav": wav, "dur": dur, "sim": round(sim, 3), "heard": " ".join(h[0] for h in heard), "num_ok": na == nb, "nums": [na, nb],
                    "words": [[w, max(0.0, t[0]), min(dur, max(t[1], t[0] + 0.08))] for w, t in zip(want, times)]})
json.dump({"segs": res}, open(sys.argv[2], "w"), ensure_ascii=False)
