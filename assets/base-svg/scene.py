"""Mechanism study: connected forms assemble, become a chart, then resolve to a result."""
import math
VIDEO_SPEC={'width':1080,'height':1920,'fps':60,'duration':6}
def clamp(v):return max(0,min(1,v))
def spring(t):
    t=max(0,t);w=2*math.pi*2.8
    return 1-(1+w*t)*math.exp(-w*t)
def track(t,keys):
    return keys[0][1]+sum((v-keys[i-1][1])*spring(t-at) for i,(at,v) in enumerate(keys) if i)
def frame(t,width,height):
    portrait=height>=width
    unit=min(width/(720 if portrait else 1200),height/(1000 if portrait else 720))
    zoom=track(t,[(0,1),(.85,1.12),(3.4,1),(4.55,.93)])
    x=track(t,[(0,-90),(.65,-250),(3.4,-190)])
    y=track(t,[(0,-40),(.65,-170),(3.4,-105)])
    w=track(t,[(0,180),(.65,500),(3.4,380)])
    h=track(t,[(0,80),(.65,340),(3.4,210)])
    r=track(t,[(0,40),(.65,30),(3.4,32)])
    box=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>'
    out=f'<defs><clipPath id="box">{box}</clipPath></defs><g fill="#203d31">{box}</g>'
    alpha=clamp((t-1)/.25)*clamp((3.4-t)/.22)
    out+=f'<g clip-path="url(#box)" opacity="{alpha}">'
    for i,value in enumerate([.34,.7,.5,.95]):
        bh=value*190*spring(t-1-i*.18);color='#e8efac' if i==3 else '#8cad94'
        out+=f'<rect x="{-178+i*99}" y="{104-bh}" width="58" height="{bh}" rx="12" fill="{color}"/>'
    out+='</g>'
    out+=f'<g clip-path="url(#box)" opacity="{clamp((t-3.75)/.3)}"><path d="M-115,0 L-93,23 L-53,-27" stroke="#e8efac" stroke-width="10" stroke-linecap="round" fill="none"/><text x="-23" y="12" font-size="35" fill="white" font-weight="bold">Conectado</text></g>'
    headline='De partes a una idea.' if t<3.5 else 'Una acción. Un resultado.'
    out+=f'<text x="0" y="-280" text-anchor="middle" font-size="44" font-weight="bold" fill="#203d31">{headline}</text>'
    out+=f'<text x="0" y="230" text-anchor="middle" font-size="25" fill="#203d31" opacity="{clamp((t-4.5)/.3)}">Transformación ilustrativa</text>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><rect width="{width}" height="{height}" fill="#f1eee6"/><g font-family="DejaVu Sans" transform="translate({width/2},{height/2}) scale({unit*zoom})">{out}</g></svg>'
