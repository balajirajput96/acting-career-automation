import { readFileSync, writeFileSync } from 'node:fs';

const source = readFileSync('index.html', 'utf8');
const sections = Object.fromEntries(
  [...source.matchAll(/<section id="(c[1-6])"[\s\S]*?<\/section>/g)].map((match) => [match[1], match[0]])
);
const prefix = source.slice(0, source.indexOf('<section id="c1"'));

function build({ output, ids, duration, audioTag, offsetMap, timeline, compositionId }) {
  const root = prefix
    .replace('data-duration="60"', `data-duration="${duration}"`)
    .replace('data-composition-id="reel-0003-home-attention-reset"', `data-composition-id="${compositionId}"`)
    .replace(/<audio id="narration"[\s\S]*?<\/audio>/, audioTag);
  const selected = ids.map((id) => {
    let section = sections[id];
    for (const [from, to] of Object.entries(offsetMap)) section = section.replace(from, to);
    return section;
  }).join('\n');
  writeFileSync(output, `${root}${selected}</div><script>${timeline}</script></body></html>`);
}

const introTimeline = `window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});const I=(s,t)=>tl.from(\`${'${s}'} .scene>*\`,{opacity:0,y:44,duration:.58,stagger:.1,ease:'power3.out'},t);I('#c1',.2);I('#c2',9.1);I('#c3',20.1);tl.to('#c1 .ripple',{scale:1.65,opacity:0,duration:1.15,repeat:4,ease:'sine.out'},1.5);tl.from('#c1 .note',{scale:.78,rotation:-11,opacity:0,duration:.75,ease:'back.out(1.25)'},.9);tl.from('#c2 .signal',{scale:.7,opacity:0,duration:.42,stagger:.26,ease:'back.out(1.2)'},10);tl.to('#c3 .main .token',{x:168,duration:5,ease:'none'},21);tl.to('#c3 .side .token',{x:120,duration:7.1,ease:'steps(3)'},21);window.__timelines['reel-0003-segment-01']=tl;`;
const outroTimeline = `window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});const I=(s,t)=>tl.from(\`${'${s}'} .scene>*\`,{opacity:0,y:44,duration:.58,stagger:.1,ease:'power3.out'},t);I('#c4',.1);I('#c5',10.1);I('#c6',22.1);tl.from('#c4 .tile',{height:0,duration:.65,stagger:.12,ease:'power3.out'},1);tl.from('#c5 .prompt,#c5 .paper',{x:-86,opacity:0,duration:.46,stagger:.18,ease:'power3.out'},11);window.__timelines['reel-0003-segment-02']=tl;`;

build({
  output: 'index-segment-01.html',
  ids: ['c1', 'c2', 'c3'],
  duration: 31,
  audioTag: '<audio id="narration" data-start="0" data-duration="31" data-track-index="3" src="assets/voice/reel-0003-segment-01.wav" data-volume="1"></audio>',
  offsetMap: {},
  timeline: introTimeline,
  compositionId: 'reel-0003-segment-01'
});

build({
  output: 'index-segment-02.html',
  ids: ['c4', 'c5', 'c6'],
  duration: 29,
  audioTag: '<audio id="narration" data-start="0" data-duration="21.68" data-track-index="3" src="assets/voice/reel-0003-segment-02.wav" data-volume="1"></audio>',
  offsetMap: {'data-start="31"': 'data-start="0"', 'data-start="41"': 'data-start="10"', 'data-start="53"': 'data-start="22"'},
  timeline: outroTimeline,
  compositionId: 'reel-0003-segment-02'
});
