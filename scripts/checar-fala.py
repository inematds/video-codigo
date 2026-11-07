"""Confere uma fala com o Whisper local: o que foi dito bate com o texto? Sem API.

Uso:
  python3 checar-fala.py --wav frase.wav --texto "o que devia ter sido dito"      (pode repetir --wav/--texto)
  python3 checar-fala.py --projeto DIR DIR/roteiro.json                           (ouve de novo cada frase do cache do voz.py)
Opções: --sim-min 0.80 (VC_SIM_MIN) · --json relatorio.json
Reprova a frase com semelhança abaixo do mínimo ou com um número ouvido como outro número (ver _alinhar.py).
O voz.py já faz isto em cada geração e refaz a frase ruim; este script é para conferir depois, ou um wav qualquer.
Saída: 0 tudo bate · 1 alguma frase não bate · 2 não deu para conferir.
"""
import argparse
import json
import pathlib
import shutil
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import voz  # noqa: E402  (falado, alinhar, IDIOMA)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("roteiro", nargs="?")
    ap.add_argument("--projeto", "--proyecto", dest="projeto")
    ap.add_argument("--wav", action="append", default=[])
    ap.add_argument("--texto", action="append", default=[])
    ap.add_argument("--sim-min", type=float, default=voz.SIM_MIN)
    ap.add_argument("--json")
    a = ap.parse_args()
    voz.SIM_MIN = a.sim_min

    itens = {}   # chave → (wav, texto)
    if a.wav or a.texto:
        if len(a.wav) != len(a.texto):
            sys.exit("Cada --wav precisa do seu --texto.")
        for i, (w, t) in enumerate(zip(a.wav, a.texto)):
            if not pathlib.Path(w).exists():
                print(f"Falta o arquivo: {w}"); sys.exit(2)
            itens[f"{i + 1:02d}-{pathlib.Path(w).stem}"] = (str(pathlib.Path(w).resolve()), t)
    elif a.projeto and a.roteiro:
        rot = json.loads(pathlib.Path(a.roteiro).read_text())
        extra = [tuple(x) for x in rot.get("dicionario", rot.get("diccionario", []))]
        cache = pathlib.Path(a.projeto).resolve() / "voz" / rot["id"] / "cache"
        for b in rot.get("blocos") or rot.get("bloques"):
            for f in b["frases"]:
                fala = voz.falado(f["texto"], extra)
                achado = [j for j in cache.glob(f"{f['id']}-*.json") if json.loads(j.read_text()).get("texto") == fala]
                if not achado:
                    print(f"  · {f['id']}: sem voz gerada para o texto atual (rode o voz.py)"); continue
                itens[f["id"]] = (str(cache / json.loads(achado[0].read_text())["wav"]), fala)
    else:
        ap.print_help(); sys.exit(2)
    if not itens:
        print("Nada para conferir."); sys.exit(2)

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="checar-fala-"))
    try:
        # o _alinhar.py grava um _t.wav ao lado do original: trabalha numa cópia
        wavs = {}
        for k, (w, _) in itens.items():
            wavs[k] = str(tmp / f"{k}.wav"); shutil.copy(w, wavs[k])
        res = voz.alinhar(wavs, {k: t for k, (_, t) in itens.items()}, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ruins = 0
    saida = {}
    for k, (w, t) in itens.items():
        r = res[k]
        ok = voz.boa(r)
        ruins += not ok
        num = "" if r.get("num_ok", True) else f" · número diferente: esperado {r['nums'][0]}, ouvido {r['nums'][1]}"
        print(f"{'OK  ' if ok else 'RUIM'} {k}: semelhança {r['sim']:.2f}{num}\n       texto  «{t}»\n       ouvido «{r['heard']}»")
        saida[k] = {"wav": w, "texto": t, "ouvido": r["heard"], "sim": r["sim"], "num_ok": r.get("num_ok", True), "ok": ok}
    print(f"\n{len(itens)} frases · {ruins} não batem (mínimo {voz.SIM_MIN})")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(saida, ensure_ascii=False, indent=1))
    sys.exit(1 if ruins else 0)


if __name__ == "__main__":
    main()
