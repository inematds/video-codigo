// Original deterministic helpers. Frequencies in Hz; damping is a dimensionless ratio.
export const clamp = (v, lo=0, hi=1) => Math.max(lo, Math.min(hi,v));
export const mix = (a,b,p) => a+(b-a)*p;
export function spring(t,{frequency=2.4,damping=1}={}) {
  if(!Number.isFinite(t)||!Number.isFinite(frequency)||frequency<=0||!Number.isFinite(damping)||damping<=0)
    throw new Error('spring requires finite time and positive frequency/damping');
  if(t<=0)return 0;
  const w=2*Math.PI*frequency,z=damping;
  if(Math.abs(z-1)<1e-5)return 1-(1+w*t)*Math.exp(-w*t);
  if(z<1){const v=w*Math.sqrt(1-z*z);return 1-Math.exp(-z*w*t)*(Math.cos(v*t)+z*w/v*Math.sin(v*t));}
  const root=Math.sqrt(z*z-1),a=-w/(z+root),b=-w*(z+root);
  return 1-(-b*Math.exp(a*t)+a*Math.exp(b*t))/(a-b);
}
export function track(t,keys,settings={}) {
  if(!Number.isFinite(t)||!Array.isArray(keys)||!keys.length)throw new Error('track requires time and nonempty keys');
  keys.forEach((k,i)=>{if(k.length!==2||!k.every(Number.isFinite)||(i&&k[0]<=keys[i-1][0]))throw new Error('keys must have strictly increasing times and finite values');});
  let value=keys[0][1];
  for(let i=1;i<keys.length;i++)value+=(keys[i][1]-keys[i-1][1])*spring(t-keys[i][0],settings);
  return value;
}
export function morphBox(t,states,settings={}) {
  const b={};for(const key of ['x','y','w','h','r'])b[key]=track(t,states.map(s=>[s.t,s[key]]),settings);
  b.w=Math.max(0,b.w);b.h=Math.max(0,b.h);b.r=clamp(b.r,0,Math.min(b.w,b.h)/2);return b;
}
export function camera(ctx,{x=0,y=0,zoom=1,rotation=0},width,height) {
  if(!(zoom>0))throw new Error('camera zoom must be positive');
  ctx.translate(width/2,height/2);ctx.rotate(rotation);ctx.scale(zoom,zoom);ctx.translate(-x,-y);
}
export function noise(index,seed=1) {
  let v=(Math.imul(index|0,0x45d9f3b)^(seed|0))>>>0;
  v=Math.imul(v^(v>>>16),0x45d9f3b)>>>0;v=Math.imul(v^(v>>>16),0x45d9f3b)>>>0;
  return ((v^(v>>>16))>>>0)/4294967296;
}
