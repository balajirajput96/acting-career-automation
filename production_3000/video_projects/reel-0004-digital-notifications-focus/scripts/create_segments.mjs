import { readFileSync, writeFileSync } from 'node:fs';

const source = readFileSync('index.html', 'utf8');
const sections = Object.fromEntries(
  [...source.matchAll(/<section id="(s[1-6])"[\s\S]*?<\/section>/g)].map((match) => [match[1], match[0]])
);
const prefix = source.slice(0, source.indexOf('<section id="s1"'));

function build({ output, ids, duration, audioTag, offsetMap, timeline, compositionId }) {
  const root = prefix
    .replace('data-duration="60"', `data-duration="${duration}"`)
    .replace('data-composition-id="reel-0004-digital-notifications-focus"', `data-composition-id="${compositionId}"`)
    .replace(/<audio id="narration"[\s\S]*?<\/audio>/, audioTag);
  const selected = ids.map((id) => {
    let section = sections[id];
    for (const [from, to] of Object.entries(offsetMap)) section = section.replace(from, to);
    return section;
  }).join('\n');
  writeFileSync(output, `${root}${selected}</div><script>${timeline}</script></body></html>`);
}

const introTimeline = `window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});const I=(s,t)=>tl.from(\`${'${s}'}>*\`,{opacity:0,y:44,duration:.58,stagger:.1,ease:'power3.out'},t);I('#s1',.2);I('#s2',9.1);I('#s3',20.1);tl.to('#s1 .pulse',{scale:1.85,opacity:0,duration:1.1,repeat:4,ease:'sine.out'},1);tl.from('#s2 .alert',{scale:.75,opacity:0,duration:.5,ease:'back.out(1.25)'},10);tl.to('#s2 .arrow',{scaleX:.2,transformOrigin:'left',duration:.9,ease:'power3.out'},11);window.__timelines['reel-0004-segment-01']=tl;`;
const outroTimeline = `window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});const I=(s,t)=>tl.from(\`${'${s}'}>*\`,{opacity:0,y:44,duration:.58,stagger:.1,ease:'power3.out'},t);I('#s4',.1);I('#s5',11.1);I('#s6',21.1);tl.from('#s4 .day',{scale:.4,opacity:0,duration:.34,stagger:.06,ease:'back.out(1.2)'},1);tl.from('#s6 .step',{x:-80,opacity:0,duration:.4,stagger:.17,ease:'power3.out'},22);window.__timelines['reel-0004-segment-02']=tl;`;

build({
  output: 'index-segment-01.html', ids: ['s1', 's2', 's3'], duration: 29,
  audioTag: '<audio id="narration" data-start="0" data-duration="29" data-track-index="3" src="assets/voice/reel-0004-segment-01.wav" data-volume="1"></audio>',
  offsetMap: {}, timeline: introTimeline, compositionId: 'reel-0004-segment-01'
});
build({
  output: 'index-segment-02.html', ids: ['s4', 's5', 's6'], duration: 31,
  audioTag: '<audio id="narration" data-start="0" data-duration="19.88" data-track-index="3" src="assets/voice/reel-0004-segment-02.wav" data-volume="1"></audio>',
  offsetMap: {'data-start="29"': 'data-start="0"', 'data-start="40"': 'data-start="11"', 'data-start="50"': 'data-start="21"'},
  timeline: outroTimeline, compositionId: 'reel-0004-segment-02'
});
