import { readFileSync, writeFileSync } from 'node:fs';

const source = readFileSync('index.html', 'utf8');
const sections = Object.fromEntries(
  [...source.matchAll(/<section id="(s[1-8])"[\s\S]*?<\/section>/g)].map((match) => [match[1], match[0]])
);
const prefix = source.slice(0, source.indexOf('<section id="s1"'));

function build({ output, ids, duration, audioTag, offsetMap, timeline, compositionId }) {
  const root = prefix
    .replace('data-duration="60"', `data-duration="${duration}"`)
    .replace('data-composition-id="reel-0005-attention-transitions"', `data-composition-id="${compositionId}"`)
    .replace(/<audio id="narration"[\s\S]*?<\/audio>/, audioTag);
  const selected = ids.map((id) => {
    let section = sections[id];
    for (const [from, to] of Object.entries(offsetMap)) section = section.replace(from, to);
    return section;
  }).join('\n');
  writeFileSync(output, `${root}${selected}</div><script>${timeline}</script></body></html>`);
}

const segmentOneTimeline = `window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});const I=(s,t)=>tl.from(\`${'${s}'}>*\`,{opacity:0,y:42,duration:.54,stagger:.1,ease:'power3.out'},t);I('#s1',.15);I('#s2',8.1);I('#s3',15.1);I('#s4',22.1);tl.to('#s1 .question',{rotation:360,duration:4,ease:'none'},1);tl.from('#s2 .station',{scale:.7,opacity:0,duration:.42,stagger:.12,ease:'back.out(1.25)'},9);tl.to('#s3 .ring',{scale:1.26,opacity:0,duration:1.3,repeat:3,ease:'sine.out'},15.8);tl.from('#s4 .beam',{scaleX:.06,opacity:.05,duration:1.1,ease:'power3.out'},22.7);tl.from('#s4 .target',{scale:.4,opacity:0,duration:.65,ease:'back.out(1.2)'},23.4);window.__timelines['reel-0005-segment-01']=tl;`;
const segmentTwoTimeline = `window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});const I=(s,t)=>tl.from(\`${'${s}'}>*\`,{opacity:0,y:42,duration:.54,stagger:.1,ease:'power3.out'},t);I('#s5',.1);I('#s6',10.1);I('#s7',20.1);I('#s8',28.05);tl.from('#s5 .rule.old',{x:-120,opacity:0,duration:.6,ease:'power3.out'},.7);tl.from('#s5 .rule.new',{x:120,opacity:0,duration:.7,ease:'power3.out'},2);tl.from('#s6 .trial',{y:80,opacity:0,duration:.6,stagger:.16,ease:'power3.out'},10.6);tl.from('#s7 .limit-card',{scale:.88,opacity:0,duration:.58,ease:'back.out(1.1)'},20.7);tl.to('#s8 .next-card',{scale:1.025,duration:1.3,yoyo:true,repeat:1,ease:'sine.inOut'},28.3);window.__timelines['reel-0005-segment-02']=tl;`;

build({
  output: 'index-segment-01.html', ids: ['s1', 's2', 's3', 's4'], duration: 29,
  audioTag: '<audio id="narration" data-start="0" data-duration="29" data-track-index="3" src="assets/voice/reel-0005-segment-01.wav" data-volume="1"></audio>',
  offsetMap: {}, timeline: segmentOneTimeline, compositionId: 'reel-0005-segment-01'
});
build({
  output: 'index-segment-02.html', ids: ['s5', 's6', 's7', 's8'], duration: 31,
  audioTag: '<audio id="narration" data-start="0" data-duration="29.8" data-track-index="3" src="assets/voice/reel-0005-segment-02.wav" data-volume="1"></audio>',
  offsetMap: { 'data-start="29"': 'data-start="0"', 'data-start="39"': 'data-start="10"', 'data-start="49"': 'data-start="20"', 'data-start="57"': 'data-start="28"' },
  timeline: segmentTwoTimeline, compositionId: 'reel-0005-segment-02'
});
