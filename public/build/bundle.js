var app=function(){"use strict";function t(){}function e(t){return t()}function n(){return Object.create(null)}function o(t){t.forEach(e)}function r(t){return"function"==typeof t}function c(t,e){return t!=t?e==e:t!==e||t&&"object"==typeof t||"function"==typeof t}function l(t,e){t.appendChild(e)}function u(t,e,n){t.insertBefore(e,n||null)}function i(t){t.parentNode.removeChild(t)}function s(t,e){for(let n=0;n<t.length;n+=1)t[n]&&t[n].d(e)}function a(t){return document.createElement(t)}function d(t){return document.createTextNode(t)}function f(){return d(" ")}function p(){return d("")}function m(t,e,n,o){return t.addEventListener(e,n,o),()=>t.removeEventListener(e,n,o)}function g(t,e,n){null==n?t.removeAttribute(e):t.getAttribute(e)!==n&&t.setAttribute(e,n)}function h(t){return""===t?null:+t}function b(t,e){e=""+e,t.wholeText!==e&&(t.data=e)}function y(t,e){t.value=null==e?"":e}function x(t,e,n,o){null===n?t.style.removeProperty(e):t.style.setProperty(e,n,o?"important":"")}let k;function v(t){k=t}function C(){if(!k)throw new Error("Function called outside component initialization");return k}const w=[],_=[],$=[],S=[],N=Promise.resolve();let T=!1;function z(t){$.push(t)}const E=new Set;let R=0;function I(){const t=k;do{for(;R<w.length;){const t=w[R];R++,v(t),B(t.$$)}for(v(null),w.length=0,R=0;_.length;)_.pop()();for(let t=0;t<$.length;t+=1){const e=$[t];E.has(e)||(E.add(e),e())}$.length=0}while(w.length);for(;S.length;)S.pop()();T=!1,E.clear(),v(t)}function B(t){if(null!==t.fragment){t.update(),o(t.before_update);const e=t.dirty;t.dirty=[-1],t.fragment&&t.fragment.p(t.ctx,e),t.after_update.forEach(z)}}const A=new Set;let L;function P(t,e){t&&t.i&&(A.delete(t),t.i(e))}function O(t,e){const n=e.token={};function r(t,r,c,l){if(e.token!==n)return;e.resolved=l;let u=e.ctx;void 0!==c&&(u=u.slice(),u[c]=l);const i=t&&(e.current=t)(u);let s=!1;e.block&&(e.blocks?e.blocks.forEach(((t,n)=>{n!==r&&t&&(L={r:0,c:[],p:L},function(t,e,n,o){if(t&&t.o){if(A.has(t))return;A.add(t),L.c.push((()=>{A.delete(t),o&&(n&&t.d(1),o())})),t.o(e)}}(t,1,1,(()=>{e.blocks[n]===t&&(e.blocks[n]=null)})),L.r||o(L.c),L=L.p)})):e.block.d(1),i.c(),P(i,1),i.m(e.mount(),e.anchor),s=!0),e.block=i,e.blocks&&(e.blocks[r]=i),s&&I()}if((c=t)&&"object"==typeof c&&"function"==typeof c.then){const n=C();if(t.then((t=>{v(n),r(e.then,1,e.value,t),v(null)}),(t=>{if(v(n),r(e.catch,2,e.error,t),v(null),!e.hasCatch)throw t})),e.current!==e.pending)return r(e.pending,0),!0}else{if(e.current!==e.then)return r(e.then,1,e.value,t),!0;e.resolved=t}var c}function D(t,e,n){const o=e.slice(),{resolved:r}=t;t.current===t.then&&(o[t.value]=r),t.current===t.catch&&(o[t.error]=r),t.block.p(o,n)}function F(t,e){-1===t.$$.dirty[0]&&(w.push(t),T||(T=!0,N.then(I)),t.$$.dirty.fill(0)),t.$$.dirty[e/31|0]|=1<<e%31}function M(c,l,u,s,a,d,f,p=[-1]){const m=k;v(c);const g=c.$$={fragment:null,ctx:null,props:d,update:t,not_equal:a,bound:n(),on_mount:[],on_destroy:[],on_disconnect:[],before_update:[],after_update:[],context:new Map(l.context||(m?m.$$.context:[])),callbacks:n(),dirty:p,skip_bound:!1,root:l.target||m.$$.root};f&&f(g.root);let h=!1;if(g.ctx=u?u(c,l.props||{},((t,e,...n)=>{const o=n.length?n[0]:e;return g.ctx&&a(g.ctx[t],g.ctx[t]=o)&&(!g.skip_bound&&g.bound[t]&&g.bound[t](o),h&&F(c,t)),e})):[],g.update(),h=!0,o(g.before_update),g.fragment=!!s&&s(g.ctx),l.target){if(l.hydrate){const t=function(t){return Array.from(t.childNodes)}(l.target);g.fragment&&g.fragment.l(t),t.forEach(i)}else g.fragment&&g.fragment.c();l.intro&&P(c.$$.fragment),function(t,n,c,l){const{fragment:u,on_mount:i,on_destroy:s,after_update:a}=t.$$;u&&u.m(n,c),l||z((()=>{const n=i.map(e).filter(r);s?s.push(...n):o(n),t.$$.on_mount=[]})),a.forEach(z)}(c,l.target,l.anchor,l.customElement),I()}v(m)}function j(t,e,n){const o=t.slice();return o[51]=e[n],o[53]=n,o}function U(t,e,n){const o=t.slice();return o[51]=e[n],o[55]=e,o[53]=n,o}function Y(t,e,n){const o=t.slice();return o[57]=e[n],o}function H(t,e,n){const o=t.slice();return o[61]=e[n][0],o[62]=e[n][1],o}function G(e){let n;return{c(){n=a("div"),n.innerHTML='<h1>Loading...</h1> \n\t\t<br/> \n\t\t<br/> \n\t\t<div class="lds-ripple svelte-10eyuz"><div class="svelte-10eyuz"></div> \n\t\t\t<div class="svelte-10eyuz"></div></div>',g(n,"class","center_mid svelte-10eyuz")},m(t,e){u(t,n,e)},p:t,d(t){t&&i(n)}}}function J(t){let e,n,r,c,s,p,h,y,k,v,C,w,_,$,S,N,T,z,E,R,I,B,A,L,P,F,M,j,U,Y,H,G,J,et,nt,ot,rt,ct,lt,ut,pt,mt,yt,xt,kt,vt,Ct,wt,St,Nt,Tt,zt,Et,Rt,It,Bt,At,Lt,Pt,Ot,Dt,Ft,Mt,jt,Ut,Yt,Ht,Gt,Jt,Vt,Wt,Kt,Xt,Qt,Zt,te,ee,ne,oe,re,ce,le,ue,ie,se,ae,de,fe,pe,me,ge,he,be,ye,xe,ke,ve,Ce,we,_e,$e,Se,Ne,Te,ze,Ee,Re,Ie,Be,Ae,Le,Pe,Oe,De=!t[18].includes("127.0.0.1")&&!t[18].includes("localhost"),Fe=t[5].networks[t[6]].name+"",Me=t[5].dexes[t[6]][t[7]].name+"",je=t[5].dexes[t[6]][t[7]].router+"",Ue=t[9]?"Yes":"No",Ye=1==t[17]?"":"s";function He(t,e){return t[9]?t[9]&&t[8]>2e3?K:t[9]&&t[8]>1e3?q:t[9]&&t[8]>500?W:V:X}let Ge=He(t),Je=Ge(t),Ve=De&&function(t){let e,n,o;return{c(){e=a("br"),n=f(),o=a("strong"),o.textContent="Remote connections are not tested and are unsafe. Use at your own risk.",x(o,"color","orangered")},m(t,r){u(t,e,r),u(t,n,r),u(t,o,r)},d(t){t&&i(e),t&&i(n),t&&i(o)}}}();function We(t,e){return t[2]&&t[3]?tt:!t[2]&&t[3]?Z:t[3]?void 0:Q}let qe=We(t),Ke=qe&&qe(t),Xe=t[12]&&it();function Qe(t,e){return t[4]?at:st}let Ze=Qe(t),tn=Ze(t),en={ctx:t,current:null,token:null,hasCatch:!1,pending:gt,then:ft,catch:dt,value:65};function nn(t,e){return 1024&e[0]&&(Ft=null),null==Ft&&(Ft=!(0!==Object.keys(t[10]).length)),Ft?bt:ht}O(Lt=t[16],en);let on=nn(t,[-1,-1,-1]),rn=on(t),cn=0===t[11].buy.length&&0===t[11].sell.length&&_t(),ln=t[11].buy.length>0&&$t(t),un=t[11].sell.length>0&&qt(t);return{c(){e=a("div"),n=a("button"),n.textContent="Home",r=f(),c=a("button"),c.textContent="Get Started",s=f(),p=a("button"),p.textContent="Buy&Snipe",h=f(),y=a("button"),y.textContent="Trades",k=f(),v=a("button"),v.textContent="Settings",C=f(),w=a("button"),w.textContent="Information",_=f(),$=a("button"),$.textContent="Stop Bot",S=f(),N=a("br"),T=f(),Je.c(),z=f(),Ve&&Ve.c(),E=f(),R=a("div"),R.innerHTML="<h1>👋 Welcome to Sniper!</h1> \n\t<br/>\n\tThis tool was made for better shitcoins trading, for everyone, without a hefty 4-digit price tag.\n\t<br/>\n\tTo get started at your first use, get all set by setting your desired config up at the Settings tab, then go to Get Started to set up your contracts.",I=f(),B=a("div"),A=a("h1"),A.textContent="🏁 Get Started",L=f(),Ke&&Ke.c(),P=f(),F=a("div"),M=a("div"),j=a("h1"),j.textContent="🔫 Buy&Snipe",U=f(),Y=a("br"),H=f(),G=a("label"),G.innerHTML="<h3>Schedule a buy here that will trigger when the token is tradable:</h3>",J=f(),et=a("input"),nt=f(),ot=a("button"),ot.textContent="Start",rt=f(),ct=a("br"),lt=f(),ut=a("i"),ut.textContent="If the token is already tradable, it will be bought instantly.",pt=f(),mt=a("br"),yt=f(),xt=a("i"),xt.textContent="To sell, go to the Trades tab.",kt=f(),vt=a("br"),Ct=f(),wt=a("i"),wt.textContent="Only one session is allowed per token.",St=f(),Xe&&Xe.c(),Nt=f(),Tt=a("br"),zt=f(),Et=a("h1"),Et.textContent="or",Rt=f(),It=a("h3"),It.textContent="Start scrapers[EXPERIMENTAL]:",Bt=f(),tn.c(),At=f(),en.block.c(),Pt=f(),Ot=a("strong"),Ot.innerHTML="<h3>Running sessions</h3>",Dt=f(),rn.c(),Mt=f(),jt=a("div"),Ut=a("h1"),Ut.textContent="💲 Trades&Transactions",Yt=f(),Ht=a("button"),Ht.textContent="Refresh Balances and PNL",Gt=f(),Jt=a("br"),Vt=f(),Wt=a("br"),Kt=f(),cn&&cn.c(),Xt=f(),ln&&ln.c(),Qt=f(),un&&un.c(),Zt=f(),te=a("div"),te.innerHTML='<h1 class="center svelte-10eyuz">⚙️ Settings and Configuration</h1> \n\t<h2>...Soon ™️</h2> \n\t<h3>For now, you need to edit the config file directly.</h3>',ee=f(),ne=a("div"),oe=a("h1"),oe.textContent="📊 Information and Stats",re=f(),ce=a("strong"),le=d("Network: "),ue=d(Fe),ie=f(),se=a("br"),ae=d("\n\tDEx: "),de=d(Me),fe=f(),pe=a("br"),me=d("\n\tDEx Router: "),ge=d(je),he=f(),be=a("br"),ye=d("\n\tConnected: "),xe=d(Ue),ke=f(),ve=a("br"),Ce=d("\n\tPing: "),we=d(t[8]),_e=d("ms\n\t"),$e=a("br"),Se=d("\n\tActive session count: "),Ne=d(t[13]),Te=f(),ze=a("br"),Ee=d("\n\tLast updated "),Re=a("strong"),Ie=d(t[17]),Be=d(" second"),Ae=d(Ye),Le=d(" ago"),g(n,"class","button_primary svelte-10eyuz"),g(n,"id","b1"),g(c,"class","button_primary svelte-10eyuz"),g(c,"id","b2"),g(p,"class","button_primary svelte-10eyuz"),g(p,"id","b3"),g(y,"class","button_primary svelte-10eyuz"),g(y,"id","b4"),g(v,"class","button_primary svelte-10eyuz"),g(v,"id","b5"),g(w,"class","button_primary svelte-10eyuz"),g(w,"id","b6"),g($,"class","button_stop svelte-10eyuz"),g(e,"class","loader center bottom_drawer svelte-10eyuz"),g(R,"class","center fade svelte-10eyuz"),g(R,"id","home"),g(B,"id","get_started"),x(B,"display","none"),g(B,"class","center fade svelte-10eyuz"),g(G,"for","start_sniping_address"),g(et,"id","start_sniping_address"),g(ot,"class","button_primary svelte-10eyuz"),x(wt,"color","orangered"),g(M,"class","center svelte-10eyuz"),g(F,"id","snipe"),x(F,"display","none"),g(F,"class","fade svelte-10eyuz"),g(Ut,"class","center svelte-10eyuz"),g(Ht,"class","button_primary center svelte-10eyuz"),g(jt,"id","trades"),x(jt,"display","none"),g(jt,"class","fade svelte-10eyuz"),g(te,"id","settings"),x(te,"display","none"),g(te,"class","fade svelte-10eyuz"),g(ne,"id","info"),x(ne,"display","none"),g(ne,"class","center fade svelte-10eyuz")},m(o,i){u(o,e,i),l(e,n),l(e,r),l(e,c),l(e,s),l(e,p),l(e,h),l(e,y),l(e,k),l(e,v),l(e,C),l(e,w),l(e,_),l(e,$),l(e,S),l(e,N),l(e,T),Je.m(e,null),l(e,z),Ve&&Ve.m(e,null),u(o,E,i),u(o,R,i),u(o,I,i),u(o,B,i),l(B,A),l(B,L),Ke&&Ke.m(B,null),u(o,P,i),u(o,F,i),l(F,M),l(M,j),l(M,U),l(M,Y),l(M,H),l(M,G),l(M,J),l(M,et),l(M,nt),l(M,ot),l(M,rt),l(M,ct),l(M,lt),l(M,ut),l(M,pt),l(M,mt),l(M,yt),l(M,xt),l(M,kt),l(M,vt),l(M,Ct),l(M,wt),l(M,St),Xe&&Xe.m(M,null),l(M,Nt),l(M,Tt),l(M,zt),l(M,Et),l(M,Rt),l(M,It),l(M,Bt),tn.m(M,null),l(M,At),en.block.m(M,en.anchor=null),en.mount=()=>M,en.anchor=null,l(F,Pt),l(F,Ot),l(F,Dt),rn.m(F,null),u(o,Mt,i),u(o,jt,i),l(jt,Ut),l(jt,Yt),l(jt,Ht),l(jt,Gt),l(jt,Jt),l(jt,Vt),l(jt,Wt),l(jt,Kt),cn&&cn.m(jt,null),l(jt,Xt),ln&&ln.m(jt,null),l(jt,Qt),un&&un.m(jt,null),u(o,Zt,i),u(o,te,i),u(o,ee,i),u(o,ne,i),l(ne,oe),l(ne,re),l(ne,ce),l(ce,le),l(ce,ue),l(ce,ie),l(ce,se),l(ce,ae),l(ce,de),l(ce,fe),l(ce,pe),l(ce,me),l(ce,ge),l(ce,he),l(ce,be),l(ce,ye),l(ce,xe),l(ce,ke),l(ce,ve),l(ce,Ce),l(ce,we),l(ce,_e),l(ce,$e),l(ce,Se),l(ce,Ne),l(ne,Te),l(ne,ze),l(ne,Ee),l(ne,Re),l(Re,Ie),l(ne,Be),l(ne,Ae),l(ne,Le),Pe||(Oe=[m(n,"click",t[26]),m(c,"click",t[27]),m(p,"click",t[28]),m(y,"click",t[29]),m(v,"click",t[30]),m(w,"click",t[31]),m($,"click",t[32]),m(ot,"click",t[33]),m(Ht,"click",t[39])],Pe=!0)},p(n,o){Ge!==(Ge=He(t=n))&&(Je.d(1),Je=Ge(t),Je&&(Je.c(),Je.m(e,z))),qe===(qe=We(t))&&Ke?Ke.p(t,o):(Ke&&Ke.d(1),Ke=qe&&qe(t),Ke&&(Ke.c(),Ke.m(B,null))),t[12]?Xe||(Xe=it(),Xe.c(),Xe.m(M,Nt)):Xe&&(Xe.d(1),Xe=null),Ze!==(Ze=Qe(t))&&(tn.d(1),tn=Ze(t),tn&&(tn.c(),tn.m(M,At))),en.ctx=t,65536&o[0]&&Lt!==(Lt=t[16])&&O(Lt,en)||D(en,t,o),on===(on=nn(t,o))&&rn?rn.p(t,o):(rn.d(1),rn=on(t),rn&&(rn.c(),rn.m(F,null))),0===t[11].buy.length&&0===t[11].sell.length?cn||(cn=_t(),cn.c(),cn.m(jt,Xt)):cn&&(cn.d(1),cn=null),t[11].buy.length>0?ln?ln.p(t,o):(ln=$t(t),ln.c(),ln.m(jt,Qt)):ln&&(ln.d(1),ln=null),t[11].sell.length>0?un?un.p(t,o):(un=qt(t),un.c(),un.m(jt,null)):un&&(un.d(1),un=null),96&o[0]&&Fe!==(Fe=t[5].networks[t[6]].name+"")&&b(ue,Fe),224&o[0]&&Me!==(Me=t[5].dexes[t[6]][t[7]].name+"")&&b(de,Me),224&o[0]&&je!==(je=t[5].dexes[t[6]][t[7]].router+"")&&b(ge,je),512&o[0]&&Ue!==(Ue=t[9]?"Yes":"No")&&b(xe,Ue),256&o[0]&&b(we,t[8]),8192&o[0]&&b(Ne,t[13]),131072&o[0]&&b(Ie,t[17]),131072&o[0]&&Ye!==(Ye=1==t[17]?"":"s")&&b(Ae,Ye)},d(t){t&&i(e),Je.d(),Ve&&Ve.d(),t&&i(E),t&&i(R),t&&i(I),t&&i(B),Ke&&Ke.d(),t&&i(P),t&&i(F),Xe&&Xe.d(),tn.d(),en.block.d(),en.token=null,en=null,rn.d(),t&&i(Mt),t&&i(jt),cn&&cn.d(),ln&&ln.d(),un&&un.d(),t&&i(Zt),t&&i(te),t&&i(ee),t&&i(ne),Pe=!1,o(Oe)}}}function V(t){let e;return{c(){e=a("strong"),e.textContent="Connected!",x(e,"color","green")},m(t,n){u(t,e,n)},d(t){t&&i(e)}}}function W(t){let e;return{c(){e=a("strong"),e.textContent="Connected(high latency!)",x(e,"color","orange")},m(t,n){u(t,e,n)},d(t){t&&i(e)}}}function q(t){let e;return{c(){e=a("strong"),e.textContent="Connected(poor latency!)",x(e,"color","orangered")},m(t,n){u(t,e,n)},d(t){t&&i(e)}}}function K(t){let e,n,o;return{c(){e=a("strong"),e.textContent="Connected(unusable latency!)",n=f(),o=a("p"),o.textContent="The bot might break or do something unintended. You can wait and hope it fixes itself, but a restart is recommended.",x(e,"color","red"),x(o,"color","red")},m(t,r){u(t,e,r),u(t,n,r),u(t,o,r)},d(t){t&&i(e),t&&i(n),t&&i(o)}}}function X(t){let e,n,o;return{c(){e=a("strong"),e.textContent="Not Connected!",n=f(),o=a("p"),o.textContent="The bot WILL break or do something unintended. You can wait and hope it connects again, but a restart is recommended.",x(e,"color","red"),x(o,"color","red")},m(t,r){u(t,e,r),u(t,n,r),u(t,o,r)},d(t){t&&i(e),t&&i(n),t&&i(o)}}}function Q(e){let n;return{c(){n=a("h2"),n.textContent="🤔 Your configuration is incomplete or invalid. To complete it, navigate over to Settings."},m(t,e){u(t,n,e)},p:t,d(t){t&&i(n)}}}function Z(t){let e,n,o,r,c,l,s,d,h,b,y=void 0!==t[5]&&et(t);function x(t,e){return"awaiting"===t[1]?ut:"errored"===t[1]?lt:"pending"===t[1]?ct:"ok"===t[1]?rt:"notok"===t[1]?ot:void 0}let k=x(t),v=k&&k(t);return{c(){e=a("h2"),e.textContent="Your setup is not completed yet, as you need to deploy your contracts.",n=f(),o=a("h3"),o.textContent="To do so, hit the button below.",r=f(),c=a("button"),c.textContent="Deploy!",l=f(),y&&y.c(),s=f(),v&&v.c(),d=p(),g(c,"class","button_primary svelte-10eyuz"),g(c,"id","deployer")},m(i,a){u(i,e,a),u(i,n,a),u(i,o,a),u(i,r,a),u(i,c,a),u(i,l,a),y&&y.m(i,a),u(i,s,a),v&&v.m(i,a),u(i,d,a),h||(b=m(c,"click",t[20]),h=!0)},p(t,e){void 0!==t[5]?y?y.p(t,e):(y=et(t),y.c(),y.m(s.parentNode,s)):y&&(y.d(1),y=null),k!==(k=x(t))&&(v&&v.d(1),v=k&&k(t),v&&(v.c(),v.m(d.parentNode,d)))},d(t){t&&i(e),t&&i(n),t&&i(o),t&&i(r),t&&i(c),t&&i(l),y&&y.d(t),t&&i(s),v&&v.d(t),t&&i(d),h=!1,b()}}}function tt(e){let n;return{c(){n=a("h2"),n.textContent="👍 Good news, you are all set."},m(t,e){u(t,n,e)},p:t,d(t){t&&i(n)}}}function et(t){let e,n=void 0!==t[5].networks[t[6]]&&nt(t);return{c(){n&&n.c(),e=p()},m(t,o){n&&n.m(t,o),u(t,e,o)},p(t,o){void 0!==t[5].networks[t[6]]?n?n.p(t,o):(n=nt(t),n.c(),n.m(e.parentNode,e)):n&&(n.d(1),n=null)},d(t){n&&n.d(t),t&&i(e)}}}function nt(t){let e,n,o,r;return{c(){e=a("h3"),n=a("a"),o=d("View Deployment Transaction In Explorer"),g(n,"href",r=t[5].networks[t[6]].explorer+"/tx/"+t[0]),g(n,"target","_blank")},m(t,r){u(t,e,r),l(e,n),l(n,o)},p(t,e){97&e[0]&&r!==(r=t[5].networks[t[6]].explorer+"/tx/"+t[0])&&g(n,"href",r)},d(t){t&&i(e)}}}function ot(t){let e;return{c(){e=a("h3"),e.textContent="❌ Your transaction was submitted but it failed. Try again, and if it persists, report it as a bug."},m(t,n){u(t,e,n)},d(t){t&&i(e)}}}function rt(t){let e;return{c(){e=a("h3"),e.textContent="✔️ Transaction OK! Restart the sniper in the tab for changes to take effect."},m(t,n){u(t,e,n)},d(t){t&&i(e)}}}function ct(t){let e;return{c(){e=a("h3"),e.textContent="⏳ Waiting for tx confirmation..."},m(t,n){u(t,e,n)},d(t){t&&i(e)}}}function lt(t){let e;return{c(){e=a("h3"),e.textContent="❌ An error occurred during deployment. Try again, and if it persists, report it as a bug."},m(t,n){u(t,e,n)},d(t){t&&i(e)}}}function ut(t){let e;return{c(){e=a("h3"),e.textContent="⏳ Awaiting tx..."},m(t,n){u(t,e,n)},d(t){t&&i(e)}}}function it(t){let e,n,o;return{c(){e=a("br"),n=f(),o=a("strong"),o.textContent="Failed to start session: address is likely invalid",x(o,"color","orangered")},m(t,r){u(t,e,r),u(t,n,r),u(t,o,r)},d(t){t&&i(e),t&&i(n),t&&i(o)}}}function st(t){let e,n,o,r,c;return{c(){e=a("strong"),e.textContent="⚠️ Telegram API details missing&Telegram not supported yet!",n=f(),o=a("br"),r=f(),c=a("button"),c.textContent="Start Telegram Scraper",g(c,"class","button_primary svelte-10eyuz"),c.disabled=!0},m(t,l){u(t,e,l),u(t,n,l),u(t,o,l),u(t,r,l),u(t,c,l)},d(t){t&&i(e),t&&i(n),t&&i(o),t&&i(r),t&&i(c)}}}function at(t){let e,n,o,r,c;return{c(){e=a("strong"),e.textContent="⚠️ Telegram not supported yet!",n=f(),o=a("br"),r=f(),c=a("button"),c.textContent="Start Telegram Scraper",g(c,"class","button_primary svelte-10eyuz"),c.disabled=!0},m(t,l){u(t,e,l),u(t,n,l),u(t,o,l),u(t,r,l),u(t,c,l)},d(t){t&&i(e),t&&i(n),t&&i(o),t&&i(r),t&&i(c)}}}function dt(e){return{c:t,m:t,p:t,d:t}}function ft(t){let e;function n(t,e){return t[65]?mt:pt}let o=n(t),r=o(t);return{c(){r.c(),e=p()},m(t,n){r.m(t,n),u(t,e,n)},p(t,c){o===(o=n(t))&&r?r.p(t,c):(r.d(1),r=o(t),r&&(r.c(),r.m(e.parentNode,e)))},d(t){r.d(t),t&&i(e)}}}function pt(e){let n,o,r;return{c(){n=a("button"),n.textContent="Start Clipboard Scraper",g(n,"class","button_primary svelte-10eyuz")},m(t,c){u(t,n,c),o||(r=m(n,"click",e[35]),o=!0)},p:t,d(t){t&&i(n),o=!1,r()}}}function mt(e){let n,o,r;return{c(){n=a("button"),n.textContent="Stop Clipboard Scraper",g(n,"class","button_stop svelte-10eyuz")},m(t,c){u(t,n,c),o||(r=m(n,"click",e[34]),o=!0)},p:t,d(t){t&&i(n),o=!1,r()}}}function gt(e){return{c:t,m:t,p:t,d:t}}function ht(t){let e,n,o=t[13]>=5&&yt(),r=Object.entries(t[10]),c=[];for(let e=0;e<r.length;e+=1)c[e]=wt(H(t,r,e));return{c(){o&&o.c(),e=f();for(let t=0;t<c.length;t+=1)c[t].c();n=p()},m(t,r){o&&o.m(t,r),u(t,e,r);for(let e=0;e<c.length;e+=1)c[e].m(t,r);u(t,n,r)},p(t,l){if(t[13]>=5?o||(o=yt(),o.c(),o.m(e.parentNode,e)):o&&(o.d(1),o=null),4195328&l[0]){let e;for(r=Object.entries(t[10]),e=0;e<r.length;e+=1){const o=H(t,r,e);c[e]?c[e].p(o,l):(c[e]=wt(o),c[e].c(),c[e].m(n.parentNode,n))}for(;e<c.length;e+=1)c[e].d(1);c.length=r.length}},d(t){o&&o.d(t),t&&i(e),s(c,t),t&&i(n)}}}function bt(e){let n;return{c(){n=a("b"),n.textContent="Nothing yet!"},m(t,e){u(t,n,e)},p:t,d(t){t&&i(n)}}}function yt(t){let e,n,o;return{c(){e=a("b"),e.textContent="Session limit reached(5)!",n=f(),o=a("br"),x(e,"color","orangered"),g(e,"class","font_transition svelte-10eyuz"),g(e,"id","limit_warning")},m(t,r){u(t,e,r),u(t,n,r),u(t,o,r)},d(t){t&&i(e),t&&i(n),t&&i(o)}}}function xt(t){let e,n,o=t[61]+"";return{c(){e=a("b"),n=d(o)},m(t,o){u(t,e,o),l(e,n)},p(t,e){1024&e[0]&&o!==(o=t[61]+"")&&b(n,o)},d(t){t&&i(e)}}}function kt(t){let e,n,o,r,c,l,s;function d(){return t[38](t[61])}return{c(){e=a("i"),e.textContent="Running",n=f(),o=a("br"),r=f(),c=a("button"),c.textContent="Stop Session",g(c,"class","button_stop svelte-10eyuz")},m(t,i){u(t,e,i),u(t,n,i),u(t,o,i),u(t,r,i),u(t,c,i),l||(s=m(c,"click",d),l=!0)},p(e,n){t=e},d(t){t&&i(e),t&&i(n),t&&i(o),t&&i(r),t&&i(c),l=!1,s()}}}function vt(t){let e,n,o,r,c,s,p,h,y=t[62]+"";function k(){return t[37](t[61])}return{c(){e=a("i"),n=d(y),o=f(),r=a("br"),c=f(),s=a("button"),s.textContent="Delete Session",x(e,"color","green"),g(s,"class","button_primary svelte-10eyuz")},m(t,i){u(t,e,i),l(e,n),u(t,o,i),u(t,r,i),u(t,c,i),u(t,s,i),p||(h=m(s,"click",k),p=!0)},p(e,o){t=e,1024&o[0]&&y!==(y=t[62]+"")&&b(n,y)},d(t){t&&i(e),t&&i(o),t&&i(r),t&&i(c),t&&i(s),p=!1,h()}}}function Ct(t){let e,n,o,r,c,l,s,d,p,h,b;function y(){return t[36](t[61])}return{c(){e=a("i"),e.textContent="Errored!",n=f(),o=a("br"),r=f(),c=a("p"),c.textContent="To try and restart, re-enter the address.",l=f(),s=a("br"),d=f(),p=a("button"),p.textContent="Delete Session",x(e,"color","red"),x(c,"color","red"),x(c,"display","inline"),g(p,"class","button_primary svelte-10eyuz")},m(t,i){u(t,e,i),u(t,n,i),u(t,o,i),u(t,r,i),u(t,c,i),u(t,l,i),u(t,s,i),u(t,d,i),u(t,p,i),h||(b=m(p,"click",y),h=!0)},p(e,n){t=e},d(t){t&&i(e),t&&i(n),t&&i(o),t&&i(r),t&&i(c),t&&i(l),t&&i(s),t&&i(d),t&&i(p),h=!1,b()}}}function wt(t){let e,n,o,r,c,l=("Errored"==t[62]||"Succeeded!"==t[62]||"Running"==t[62])&&xt(t);function s(t,e){return"Errored"==t[62]?Ct:"Succeeded!"==t[62]?vt:"Running"==t[62]?kt:void 0}let d=s(t),p=d&&d(t);return{c(){l&&l.c(),e=f(),p&&p.c(),n=f(),o=a("br"),r=f(),c=a("br")},m(t,i){l&&l.m(t,i),u(t,e,i),p&&p.m(t,i),u(t,n,i),u(t,o,i),u(t,r,i),u(t,c,i)},p(t,o){"Errored"==t[62]||"Succeeded!"==t[62]||"Running"==t[62]?l?l.p(t,o):(l=xt(t),l.c(),l.m(e.parentNode,e)):l&&(l.d(1),l=null),d===(d=s(t))&&p?p.p(t,o):(p&&p.d(1),p=d&&d(t),p&&(p.c(),p.m(n.parentNode,n)))},d(t){l&&l.d(t),t&&i(e),p&&p.d(t),t&&i(n),t&&i(o),t&&i(r),t&&i(c)}}}function _t(t){let e;return{c(){e=a("b"),e.textContent="Nothing yet!"},m(t,n){u(t,e,n)},d(t){t&&i(e)}}}function $t(t){let e,n,o,r=t[11].buy,c=[];for(let e=0;e<r.length;e+=1)c[e]=Wt(U(t,r,e));return{c(){e=a("div"),n=a("h2"),n.textContent="Buys",o=f();for(let t=0;t<c.length;t+=1)c[t].c();x(n,"color","green"),x(e,"float","left")},m(t,r){u(t,e,r),l(e,n),l(e,o);for(let t=0;t<c.length;t+=1)c[t].m(e,null)},p(t,n){if(575584&n[0]){let o;for(r=t[11].buy,o=0;o<r.length;o+=1){const l=U(t,r,o);c[o]?c[o].p(l,n):(c[o]=Wt(l),c[o].c(),c[o].m(e,null))}for(;o<c.length;o+=1)c[o].d(1);c.length=r.length}},d(t){t&&i(e),s(c,t)}}}function St(e){let n;return{c(){n=a("i"),n.textContent="Successful!",x(n,"color","green")},m(t,e){u(t,n,e)},p:t,d(t){t&&i(n)}}}function Nt(e){let n;return{c(){n=a("i"),n.textContent="Failed!",x(n,"color","red")},m(t,e){u(t,n,e)},p:t,d(t){t&&i(n)}}}function Tt(t){let e,n,o=t[51].status+"";return{c(){e=a("i"),n=d(o)},m(t,o){u(t,e,o),l(e,n)},p(t,e){2048&e[0]&&o!==(o=t[51].status+"")&&b(n,o)},d(t){t&&i(e)}}}function zt(t){let e,n,r,c,l,d,b,x,k,v,C,w,_,$={ctx:t,current:null,token:null,hasCatch:!0,pending:Lt,then:Rt,catch:Et,value:54};O(e=t[19](`/decs/${t[51].address}`,!1),$);let S=t[15],N=[];for(let e=0;e<S.length;e+=1)N[e]=jt(Y(t,S,e));function T(){t[40].call(d,t[51])}function z(){return t[41](t[51])}let E={ctx:t,current:null,token:null,hasCatch:!1,pending:Vt,then:Yt,catch:Ut,value:56};return O(C=t[19](`/getBalance/${t[51].address}`,!1),E),{c(){$.block.c(),n=f();for(let t=0;t<N.length;t+=1)N[t].c();r=f(),c=a("label"),c.textContent="Sell a percentage of your total holdings:",l=f(),d=a("input"),b=f(),x=a("button"),x.textContent="Sell",k=f(),v=p(),E.block.c(),g(c,"for","seller"),g(d,"id","seller"),g(d,"type","number"),g(x,"class","button_stop svelte-10eyuz")},m(e,o){$.block.m(e,$.anchor=o),$.mount=()=>n.parentNode,$.anchor=n,u(e,n,o);for(let t=0;t<N.length;t+=1)N[t].m(e,o);u(e,r,o),u(e,c,o),u(e,l,o),u(e,d,o),y(d,t[14][t[51].address]),u(e,b,o),u(e,x,o),u(e,k,o),u(e,v,o),E.block.m(e,E.anchor=o),E.mount=()=>v.parentNode,E.anchor=v,w||(_=[m(d,"input",T),m(x,"click",z)],w=!0)},p(n,o){if(t=n,$.ctx=t,2048&o[0]&&e!==(e=t[19](`/decs/${t[51].address}`,!1))&&O(e,$)||D($,t,o),559200&o[0]){let e;for(S=t[15],e=0;e<S.length;e+=1){const n=Y(t,S,e);N[e]?N[e].p(n,o):(N[e]=jt(n),N[e].c(),N[e].m(r.parentNode,r))}for(;e<N.length;e+=1)N[e].d(1);N.length=S.length}18432&o[0]&&h(d.value)!==t[14][t[51].address]&&y(d,t[14][t[51].address]),E.ctx=t,2048&o[0]&&C!==(C=t[19](`/getBalance/${t[51].address}`,!1))&&O(C,E)||D(E,t,o)},d(t){$.block.d(t),$.token=null,$=null,t&&i(n),s(N,t),t&&i(r),t&&i(c),t&&i(l),t&&i(d),t&&i(b),t&&i(x),t&&i(k),t&&i(v),E.block.d(t),E.token=null,E=null,w=!1,o(_)}}}function Et(e){let n;return{c(){n=a("strong"),n.textContent="Balance reloading failed!",x(n,"color","red")},m(t,e){u(t,n,e)},p:t,d(t){t&&i(n)}}}function Rt(t){let e,n,o,r,c,l,s=t[51].amount_out/10**t[54]+"",f={ctx:t,current:null,token:null,hasCatch:!1,pending:At,then:Bt,catch:It,value:56};return O(l=t[19](`/getBalance/${t[51].address}`,!1),f),{c(){e=a("strong"),e.textContent="Amount Received",n=d(": "),o=d(s),r=d(" tokens\n\t\t\t\t\t"),c=p(),f.block.c()},m(t,l){u(t,e,l),u(t,n,l),u(t,o,l),u(t,r,l),u(t,c,l),f.block.m(t,f.anchor=l),f.mount=()=>c.parentNode,f.anchor=c},p(e,n){t=e,2048&n[0]&&s!==(s=t[51].amount_out/10**t[54]+"")&&b(o,s),f.ctx=t,2048&n[0]&&l!==(l=t[19](`/getBalance/${t[51].address}`,!1))&&O(l,f)||D(f,t,n)},d(t){t&&i(e),t&&i(n),t&&i(o),t&&i(r),t&&i(c),f.block.d(t),f.token=null,f=null}}}function It(e){return{c:t,m:t,p:t,d:t}}function Bt(t){let e,n,o,r,c,l=t[56]/10**t[54]+"";return{c(){e=a("br"),n=f(),o=a("strong"),o.textContent="Balance Now",r=d(": "),c=d(l)},m(t,l){u(t,e,l),u(t,n,l),u(t,o,l),u(t,r,l),u(t,c,l)},p(t,e){2048&e[0]&&l!==(l=t[56]/10**t[54]+"")&&b(c,l)},d(t){t&&i(e),t&&i(n),t&&i(o),t&&i(r),t&&i(c)}}}function At(e){let n,o,r,c,l;return{c(){n=a("br"),o=f(),r=a("strong"),r.textContent="Balance Now",c=d(": "),l=a("i"),l.textContent="Updating..."},m(t,e){u(t,n,e),u(t,o,e),u(t,r,e),u(t,c,e),u(t,l,e)},p:t,d(t){t&&i(n),t&&i(o),t&&i(r),t&&i(c),t&&i(l)}}}function Lt(e){let n,o,r;return{c(){n=a("strong"),n.textContent="Amount Received",o=d(": "),r=a("i"),r.textContent="Updating..."},m(t,e){u(t,n,e),u(t,o,e),u(t,r,e)},p:t,d(t){t&&i(n),t&&i(o),t&&i(r)}}}function Pt(e){let n,o,r,c,l,s;return{c(){n=a("strong"),n.textContent="PNL",o=d(": Failed to get!\n\t\t\t\t\t\t"),r=a("br"),c=f(),l=a("strong"),l.textContent="Return if sold now",s=d(": Updating..."),x(n,"color","green")},m(t,e){u(t,n,e),u(t,o,e),u(t,r,e),u(t,c,e),u(t,l,e),u(t,s,e)},p:t,d(t){t&&i(n),t&&i(o),t&&i(r),t&&i(c),t&&i(l),t&&i(s)}}}function Ot(t){let e;function n(t,e){return t[60].multiplier>1?Ft:Dt}let o=n(t),r=o(t);return{c(){r.c(),e=p()},m(t,n){r.m(t,n),u(t,e,n)},p(t,c){o===(o=n(t))&&r?r.p(t,c):(r.d(1),r=o(t),r&&(r.c(),r.m(e.parentNode,e)))},d(t){r.d(t),t&&i(e)}}}function Dt(t){let e,n,o,r,c,l,s,p,m,g,h,y,k,v=t[60].multiplier+"",C=t[60].percentage_string+"",w=t[60].if_sold_now/10**18+"",_=t[5].networks[t[6]].tick+"";return{c(){e=a("strong"),e.textContent="PNL",n=d(": "),o=d(v),r=d("x / "),c=d(C),l=f(),s=a("br"),p=f(),m=a("strong"),m.textContent="Return if sold now",g=d(": "),h=d(w),y=f(),k=d(_),x(e,"color","red"),x(m,"color","red")},m(t,i){u(t,e,i),u(t,n,i),u(t,o,i),u(t,r,i),u(t,c,i),u(t,l,i),u(t,s,i),u(t,p,i),u(t,m,i),u(t,g,i),u(t,h,i),u(t,y,i),u(t,k,i)},p(t,e){34816&e[0]&&v!==(v=t[60].multiplier+"")&&b(o,v),34816&e[0]&&C!==(C=t[60].percentage_string+"")&&b(c,C),34816&e[0]&&w!==(w=t[60].if_sold_now/10**18+"")&&b(h,w),96&e[0]&&_!==(_=t[5].networks[t[6]].tick+"")&&b(k,_)},d(t){t&&i(e),t&&i(n),t&&i(o),t&&i(r),t&&i(c),t&&i(l),t&&i(s),t&&i(p),t&&i(m),t&&i(g),t&&i(h),t&&i(y),t&&i(k)}}}function Ft(t){let e,n,o,r,c,l,s,p,m,g,h,y,k,v=t[60].multiplier+"",C=t[60].percentage_string+"",w=t[60].if_sold_now/10**18+"",_=t[5].networks[t[6]].tick+"";return{c(){e=a("strong"),e.textContent="PNL",n=d(": "),o=d(v),r=d("x / "),c=d(C),l=f(),s=a("br"),p=f(),m=a("strong"),m.textContent="Return if sold now",g=d(": "),h=d(w),y=f(),k=d(_),x(e,"color","green"),x(m,"color","green")},m(t,i){u(t,e,i),u(t,n,i),u(t,o,i),u(t,r,i),u(t,c,i),u(t,l,i),u(t,s,i),u(t,p,i),u(t,m,i),u(t,g,i),u(t,h,i),u(t,y,i),u(t,k,i)},p(t,e){34816&e[0]&&v!==(v=t[60].multiplier+"")&&b(o,v),34816&e[0]&&C!==(C=t[60].percentage_string+"")&&b(c,C),34816&e[0]&&w!==(w=t[60].if_sold_now/10**18+"")&&b(h,w),96&e[0]&&_!==(_=t[5].networks[t[6]].tick+"")&&b(k,_)},d(t){t&&i(e),t&&i(n),t&&i(o),t&&i(r),t&&i(c),t&&i(l),t&&i(s),t&&i(p),t&&i(m),t&&i(g),t&&i(h),t&&i(y),t&&i(k)}}}function Mt(e){let n,o,r,c,l,s;return{c(){n=a("strong"),n.textContent="PNL",o=d(": Updating...\n\t\t\t\t\t\t"),r=a("br"),c=f(),l=a("strong"),l.textContent="Return if sold now",s=d(": Updating...")},m(t,e){u(t,n,e),u(t,o,e),u(t,r,e),u(t,c,e),u(t,l,e),u(t,s,e)},p:t,d(t){t&&i(n),t&&i(o),t&&i(r),t&&i(c),t&&i(l),t&&i(s)}}}function jt(t){let e,n,o,r,c={ctx:t,current:null,token:null,hasCatch:!0,pending:Mt,then:Ot,catch:Pt,value:60};return O(r=t[19](`/pnl?address=${t[51].address}&in=${t[51].amount_in}&out=${t[51].amount_out}`,!t[57]),c),{c(){e=a("br"),n=f(),o=p(),c.block.c()},m(t,r){u(t,e,r),u(t,n,r),u(t,o,r),c.block.m(t,c.anchor=r),c.mount=()=>o.parentNode,c.anchor=o},p(e,n){t=e,c.ctx=t,34816&n[0]&&r!==(r=t[19](`/pnl?address=${t[51].address}&in=${t[51].amount_in}&out=${t[51].amount_out}`,!t[57]))&&O(r,c)||D(c,t,n)},d(t){t&&i(e),t&&i(n),t&&i(o),c.block.d(t),c.token=null,c=null}}}function Ut(e){return{c:t,m:t,p:t,d:t}}function Yt(t){let e,n,o={ctx:t,current:null,token:null,hasCatch:!1,pending:Jt,then:Gt,catch:Ht,value:54};return O(n=t[19](`/decs/${t[51].address}`,!1),o),{c(){e=p(),o.block.c()},m(t,n){u(t,e,n),o.block.m(t,o.anchor=n),o.mount=()=>e.parentNode,o.anchor=e},p(e,r){t=e,o.ctx=t,2048&r[0]&&n!==(n=t[19](`/decs/${t[51].address}`,!1))&&O(n,o)||D(o,t,r)},d(t){t&&i(e),o.block.d(t),o.token=null,o=null}}}function Ht(e){return{c:t,m:t,p:t,d:t}}function Gt(t){let e,n,o,r,c=(Number.isNaN(t[14][t[51].address]/100*t[56]/10**t[54])?0:t[14][t[51].address]/100*t[56]/10**t[54])+"";return{c(){e=a("i"),n=d("("),o=d(c),r=d(" tokens)")},m(t,c){u(t,e,c),l(e,n),l(e,o),l(e,r)},p(t,e){18432&e[0]&&c!==(c=(Number.isNaN(t[14][t[51].address]/100*t[56]/10**t[54])?0:t[14][t[51].address]/100*t[56]/10**t[54])+"")&&b(o,c)},d(t){t&&i(e)}}}function Jt(e){return{c:t,m:t,p:t,d:t}}function Vt(e){return{c:t,m:t,p:t,d:t}}function Wt(t){let e,n,o,r,c,s,p,h,y,k,v,C,w,_,$,S,N,T,z,E,R,I,B,A,L,P,O,D,F,M,j,U,Y=t[51].address+"",H=t[51].amount_in/10**18+"",G=t[5].networks[t[6]].tick+"";function J(t,e){return"Pending"==t[51].status?Tt:"Failed"==t[51].status?Nt:"Successful"==t[51].status?St:void 0}let V=J(t),W=V&&V(t),q="Successful"==t[51].status&&zt(t);function K(){return t[42](t[53])}return{c(){e=a("b"),n=d(Y),o=f(),W&&W.c(),r=f(),c=a("br"),s=f(),p=a("a"),h=a("b"),h.textContent="View Transaction In Explorer",k=f(),v=a("br"),C=f(),w=a("strong"),w.textContent="Amount Inputted",_=d(": "),$=d(H),S=f(),N=d(G),T=f(),z=a("br"),E=f(),q&&q.c(),R=f(),I=a("br"),B=f(),A=a("button"),A.textContent="Delete this log",L=f(),P=a("br"),O=f(),D=a("br"),F=f(),M=a("br"),g(p,"href",y=t[5].networks[t[6]].explorer+"/tx/"+t[51].tx),g(p,"target","_blank"),x(p,"color","green"),g(A,"class","button_stop svelte-10eyuz")},m(t,i){u(t,e,i),l(e,n),u(t,o,i),W&&W.m(t,i),u(t,r,i),u(t,c,i),u(t,s,i),u(t,p,i),l(p,h),u(t,k,i),u(t,v,i),u(t,C,i),u(t,w,i),u(t,_,i),u(t,$,i),u(t,S,i),u(t,N,i),u(t,T,i),u(t,z,i),u(t,E,i),q&&q.m(t,i),u(t,R,i),u(t,I,i),u(t,B,i),u(t,A,i),u(t,L,i),u(t,P,i),u(t,O,i),u(t,D,i),u(t,F,i),u(t,M,i),j||(U=m(A,"click",K),j=!0)},p(e,o){t=e,2048&o[0]&&Y!==(Y=t[51].address+"")&&b(n,Y),V===(V=J(t))&&W?W.p(t,o):(W&&W.d(1),W=V&&V(t),W&&(W.c(),W.m(r.parentNode,r))),2144&o[0]&&y!==(y=t[5].networks[t[6]].explorer+"/tx/"+t[51].tx)&&g(p,"href",y),2048&o[0]&&H!==(H=t[51].amount_in/10**18+"")&&b($,H),96&o[0]&&G!==(G=t[5].networks[t[6]].tick+"")&&b(N,G),"Successful"==t[51].status?q?q.p(t,o):(q=zt(t),q.c(),q.m(R.parentNode,R)):q&&(q.d(1),q=null)},d(t){t&&i(e),t&&i(o),W&&W.d(t),t&&i(r),t&&i(c),t&&i(s),t&&i(p),t&&i(k),t&&i(v),t&&i(C),t&&i(w),t&&i(_),t&&i($),t&&i(S),t&&i(N),t&&i(T),t&&i(z),t&&i(E),q&&q.d(t),t&&i(R),t&&i(I),t&&i(B),t&&i(A),t&&i(L),t&&i(P),t&&i(O),t&&i(D),t&&i(F),t&&i(M),j=!1,U()}}}function qt(t){let e,n,o,r=t[11].sell,c=[];for(let e=0;e<r.length;e+=1)c[e]=re(j(t,r,e));return{c(){e=a("div"),n=a("h2"),n.textContent="Sells",o=f();for(let t=0;t<c.length;t+=1)c[t].c();x(n,"color","red"),g(e,"class","float-r svelte-10eyuz")},m(t,r){u(t,e,r),l(e,n),l(e,o);for(let t=0;t<c.length;t+=1)c[t].m(e,null)},p(t,n){if(526432&n[0]){let o;for(r=t[11].sell,o=0;o<r.length;o+=1){const l=j(t,r,o);c[o]?c[o].p(l,n):(c[o]=re(l),c[o].c(),c[o].m(e,null))}for(;o<c.length;o+=1)c[o].d(1);c.length=r.length}},d(t){t&&i(e),s(c,t)}}}function Kt(e){let n;return{c(){n=a("i"),n.textContent="Successful!",x(n,"color","green")},m(t,e){u(t,n,e)},p:t,d(t){t&&i(n)}}}function Xt(e){let n;return{c(){n=a("i"),n.textContent="Failed!",x(n,"color","red")},m(t,e){u(t,n,e)},p:t,d(t){t&&i(n)}}}function Qt(t){let e,n,o=t[51].status+"";return{c(){e=a("i"),n=d(o)},m(t,o){u(t,e,o),l(e,n)},p(t,e){2048&e[0]&&o!==(o=t[51].status+"")&&b(n,o)},d(t){t&&i(e)}}}function Zt(t){let e,n,o={ctx:t,current:null,token:null,hasCatch:!1,pending:oe,then:ne,catch:ee,value:54};return O(n=t[19](`/decs/${t[5].networks[t[6]].weth}`,!1),o),{c(){e=p(),o.block.c()},m(t,n){u(t,e,n),o.block.m(t,o.anchor=n),o.mount=()=>e.parentNode,o.anchor=e},p(e,r){t=e,o.ctx=t,96&r[0]&&n!==(n=t[19](`/decs/${t[5].networks[t[6]].weth}`,!1))&&O(n,o)||D(o,t,r)},d(t){t&&i(e),o.block.d(t),o.token=null,o=null}}}function te(e){let n,o;return{c(){n=a("strong"),n.textContent="Amount Received",o=d(": Pending or Failed")},m(t,e){u(t,n,e),u(t,o,e)},p:t,d(t){t&&i(n),t&&i(o)}}}function ee(e){return{c:t,m:t,p:t,d:t}}function ne(t){let e,n,o,r,c,l=t[51].amount_out/10**t[54]+"",s=t[5].networks[t[6]].tick+"";return{c(){e=a("strong"),e.textContent="Amount Received",n=d(": "),o=d(l),r=f(),c=d(s)},m(t,l){u(t,e,l),u(t,n,l),u(t,o,l),u(t,r,l),u(t,c,l)},p(t,e){2144&e[0]&&l!==(l=t[51].amount_out/10**t[54]+"")&&b(o,l),96&e[0]&&s!==(s=t[5].networks[t[6]].tick+"")&&b(c,s)},d(t){t&&i(e),t&&i(n),t&&i(o),t&&i(r),t&&i(c)}}}function oe(e){let n,o,r;return{c(){n=a("strong"),n.textContent="Amount Received",o=d(": "),r=a("i"),r.textContent="Updating..."},m(t,e){u(t,n,e),u(t,o,e),u(t,r,e)},p:t,d(t){t&&i(n),t&&i(o),t&&i(r)}}}function re(t){let e,n,o,r,c,s,p,h,y,k,v,C,w,_,$,S,N,T,z,E,R,I,B,A,L,P,O,D,F,M,j=t[51].address+"",U=t[51].amount_in/10**18+"";function Y(t,e){return"Pending"==t[51].status?Qt:"Failed"==t[51].status?Xt:"Successful"==t[51].status?Kt:void 0}let H=Y(t),G=H&&H(t);function J(t,e){return"Successful"!=t[51].status?te:Zt}let V=J(t),W=V(t);function q(){return t[43](t[53])}return{c(){e=a("b"),n=d(j),o=f(),G&&G.c(),r=f(),c=a("br"),s=f(),p=a("a"),h=a("b"),h.textContent="View Transaction In Explorer",k=f(),v=a("br"),C=f(),w=a("strong"),w.textContent="Amount Inputted",_=d(": "),$=d(U),S=d(" tokens\n\t\t\t\t"),N=a("br"),T=f(),W.c(),z=f(),E=a("br"),R=f(),I=a("button"),I.textContent="Delete this log",B=f(),A=a("br"),L=f(),P=a("br"),O=f(),D=a("br"),g(p,"href",y=t[5].networks[t[6]].explorer+"/tx/"+t[51].tx),g(p,"target","_blank"),x(p,"color","red"),g(I,"class","button_stop svelte-10eyuz")},m(t,i){u(t,e,i),l(e,n),u(t,o,i),G&&G.m(t,i),u(t,r,i),u(t,c,i),u(t,s,i),u(t,p,i),l(p,h),u(t,k,i),u(t,v,i),u(t,C,i),u(t,w,i),u(t,_,i),u(t,$,i),u(t,S,i),u(t,N,i),u(t,T,i),W.m(t,i),u(t,z,i),u(t,E,i),u(t,R,i),u(t,I,i),u(t,B,i),u(t,A,i),u(t,L,i),u(t,P,i),u(t,O,i),u(t,D,i),F||(M=m(I,"click",q),F=!0)},p(e,o){t=e,2048&o[0]&&j!==(j=t[51].address+"")&&b(n,j),H===(H=Y(t))&&G?G.p(t,o):(G&&G.d(1),G=H&&H(t),G&&(G.c(),G.m(r.parentNode,r))),2144&o[0]&&y!==(y=t[5].networks[t[6]].explorer+"/tx/"+t[51].tx)&&g(p,"href",y),2048&o[0]&&U!==(U=t[51].amount_in/10**18+"")&&b($,U),V===(V=J(t))&&W?W.p(t,o):(W.d(1),W=V(t),W&&(W.c(),W.m(z.parentNode,z)))},d(t){t&&i(e),t&&i(o),G&&G.d(t),t&&i(r),t&&i(c),t&&i(s),t&&i(p),t&&i(k),t&&i(v),t&&i(C),t&&i(w),t&&i(_),t&&i($),t&&i(S),t&&i(N),t&&i(T),W.d(t),t&&i(z),t&&i(E),t&&i(R),t&&i(I),t&&i(B),t&&i(A),t&&i(L),t&&i(P),t&&i(O),t&&i(D),F=!1,M()}}}function ce(e){let n;function o(t,e){return void 0!==t[9]&&void 0!==t[8]?J:G}let r=o(e),c=r(e);return{c(){n=a("main"),c.c()},m(t,e){u(t,n,e),c.m(n,null)},p(t,e){r===(r=o(t))&&c?c.p(t,e):(c.d(1),c=r(t),c&&(c.c(),c.m(n,null)))},i:t,o:t,d(t){t&&i(n),c.d()}}}function le(t){for(let e=1;e<7;e++)document.getElementById(`b${e}`).disabled=!t}function ue(t){return new Promise((e=>setTimeout(e,t)))}function ie(t,e,n){let o;const r=location.protocol+"//"+location.host,c=async(t,e)=>{let n=e?fetch(r+t,{method:"POST"}):fetch(r+t),o=JSON.parse(await(await n).text()),c=await(await n).status;if(c>=400)throw URIError(c.toString());return o},l=["home","get_started","snipe","trades","settings","info"];let u,i,s,a,d,f,p,m,g,b,y,x,k="0x0000000000000000000000000000000000000000000000000000000000000000",v="notStarted",C=!1,w=0,_={},$=[1],S=c("/getScrapeState/c");async function N(){try{void 0===p&&await ue(2500);let t=Date.now();await c("/ping",!1);let e=Date.now();n(8,p=Math.round(e-t)),n(9,m=!0)}catch(t){n(8,p=0),n(9,m=!1)}n(24,g=Date.now())}async function T(t){n(12,C=!1);try{await c(`/startSimulating/${t}`,!0)}catch{n(12,C=!0)}}async function z(t){await c(`/stopSimulating/${t}`,!0)}function E(t){for(let e=0;e<l.length;e++)l[e]!=t?document.getElementById(l[e]).style.display="none":document.getElementById(t).style.display="block"}!async function(){n(2,u=await c("/isDeployed",!1)),n(3,i=await c("/isCoreConfigured",!1)),n(5,a=await c("/allNetworks",!1)),n(6,d=await c("/network",!1)),n(7,f=await c("/dex",!1)),await c("/getConfig",!1),n(4,s=await c("/isTGConfigured",!1))}(),N(),setInterval(N,2e4),setInterval((function(){n(25,b=Date.now())}),100),setTimeout((async function(){for(;void 0===x;)await ue(100);for(;void 0!==x;)n(15,$[0]=1,$),await ue(1500*x.buy.length)}),0),setTimeout((async function(){for(;;){try{let t=await c("/getSimulationsAndTrades",!1);JSON.stringify(t.simulations)!==JSON.stringify(y)&&n(10,y=t.simulations),JSON.stringify(t.trades)!==JSON.stringify(x)&&n(11,x=t.trades)}catch{}let t=0;for(const[e,n]of Object.entries(y))"Running"==n&&(t+=1);n(13,w=t),await ue(250)}}),0);return t.$$.update=()=>{50331648&t.$$.dirty[0]&&n(17,o=Math.round((b-g)/1e3))},[k,v,u,i,s,a,d,f,p,m,y,x,C,w,_,$,S,o,r,c,async function(){let t;n(1,v="awaiting"),le(!1),document.getElementById("deployer").disabled=!0;try{for(n(0,k=await c("/deploy",!0));;){if(n(1,v="pending"),t=await c(`/txReceipt/${k}`,!1),t[0]){t[1]?n(1,v="ok"):n(1,v="notok");break}await ue(1e3)}le(!0)}catch(t){n(1,v="errored"),document.getElementById("deployer").disabled=!1,le(!0)}},T,z,E,g,b,function(){E("home")},function(){E("get_started")},function(){E("snipe")},function(){E("trades")},function(){E("settings")},function(){E("info")},()=>{c("/kill",!0),le(!1),ue(500).then((t=>window.close()))},function(){T(document.getElementById("start_sniping_address").value)},()=>{c("/toggleScrape/c",!0),n(16,S=c("/getScrapeState/c",!1))},()=>{c("/toggleScrape/c",!0),n(16,S=c("/getScrapeState/c",!1))},function(t){z(t)},function(t){z(t)},function(t){z(t)},()=>{n(10,y),n(11,x)},function(t){_[t.address]=h(this.value),n(14,_)},t=>{c(`/sell?address=${t.address}&amount_in=${document.getElementById("seller").value}`,!0)},t=>c(`/deleteTrade/buy/${t}`,!0),t=>c(`/deleteTrade/sell/${t}`,!0)]}return new class extends class{$destroy(){!function(t,e){const n=t.$$;null!==n.fragment&&(o(n.on_destroy),n.fragment&&n.fragment.d(e),n.on_destroy=n.fragment=null,n.ctx=[])}(this,1),this.$destroy=t}$on(t,e){const n=this.$$.callbacks[t]||(this.$$.callbacks[t]=[]);return n.push(e),()=>{const t=n.indexOf(e);-1!==t&&n.splice(t,1)}}$set(t){var e;this.$$set&&(e=t,0!==Object.keys(e).length)&&(this.$$.skip_bound=!0,this.$$set(t),this.$$.skip_bound=!1)}}{constructor(t){super(),M(this,t,ie,ce,c,{},null,[-1,-1,-1])}}({target:document.body,props:{name:"world"}})}();
//# sourceMappingURL=bundle.js.map