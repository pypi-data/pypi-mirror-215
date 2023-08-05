"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[1286],{70001:function(t,n,e){var r=e(26304),o=e(21831),i=e(82394),a=e(82684),c=e(26226),u=e(84969),l=e(90948),s=e(65743),d=e(28108),f=e(79487),h=e(29989),p=e(38626),m=e(61655),g=e(16853),v=e(65376),x=e(48072),y=e(24903),b=e(84181),j=e(98677),w=e(19711),Z=e(31969),_=e(73899),O=e(31012),S=e(49125),E=e(2005),k=e(28598),I=["height","width"];function P(t,n){var e=Object.keys(t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(t);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(t,n).enumerable}))),e.push.apply(e,r)}return e}function D(t){for(var n=1;n<arguments.length;n++){var e=null!=arguments[n]?arguments[n]:{};n%2?P(Object(e),!0).forEach((function(n){(0,i.Z)(t,n,e[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(e)):P(Object(e)).forEach((function(n){Object.defineProperty(t,n,Object.getOwnPropertyDescriptor(e,n))}))}return t}var A={bottom:5*S.iI,left:3*S.iI,right:20*S.iI,top:0},T=function(t){return t.x},C=function(t){return t.y},M=(0,m.Z)((function(t){var n=t.data,e=t.height,r=t.hideTooltip,i=t.large,c=t.margin,m=void 0===c?{}:c,S=t.renderTooltipContent,I=t.showTooltip,P=t.tooltipData,M=t.tooltipLeft,L=t.tooltipOpen,R=t.tooltipTop,Y=t.width,N=t.xAxisLabel,F=t.xNumTicks,H=t.yLabelFormat,V=t.ySerialize,B=H;B||(B=function(t){return t.length>20?"".concat(t.substring(0,20),"..."):t});var z=i?O.iD:O.J5,U=(0,a.useContext)(p.ThemeContext),J=D(D({},A),m),X=n.slice(Math.max(0,n.length-50)),G=Object.keys(X[0]||[]).filter((function(t){return"x"===t})),K=(0,y.Z)({domain:G,range:[_.hM]}),Q=(0,b.Z)({domain:[0,Math.max.apply(Math,(0,o.Z)(X.map(T)))],nice:!0}),W=(0,j.Z)({domain:X.map(C),padding:.35}),q={active:(null===U||void 0===U?void 0:U.content.default)||Z.Z.content.default,backgroundPrimary:(null===U||void 0===U?void 0:U.chart.backgroundPrimary)||Z.Z.chart.backgroundPrimary,backgroundSecondary:(null===U||void 0===U?void 0:U.chart.backgroundSecondary)||Z.Z.chart.backgroundSecondary,muted:(null===U||void 0===U?void 0:U.content.muted)||Z.Z.content.muted,primary:(null===U||void 0===U?void 0:U.chart.primary)||Z.Z.chart.primary,tooltipBackground:(null===U||void 0===U?void 0:U.background.navigation)||Z.Z.background.navigation},$=X.map(V),tt=Math.min(Math.max.apply(Math,(0,o.Z)($.map((function(t){return String(t).length})))),20);6*tt>2*J.right?J.right+=5.5*tt:6*tt>=J.right&&(J.right+=3.75*tt);var nt=Y-J.left-J.right,et=e-J.top-J.bottom;J.left+=7*tt,Q.rangeRound([0,nt]),W.rangeRound([et,0]);var rt=X.map(T).length,ot=W($[rt-1]),it=(0,a.useCallback)((function(t){var n=(0,x.Z)(t)||{x:0,y:0},e=n.x,r=n.y,o=1-(r-ot/2)/(et-ot),i=Math.floor(o*rt),a=X[i];"undefined"===typeof a&&(a=X[i-1]),r>ot&&r<et-ot&&I({tooltipData:a,tooltipLeft:e,tooltipTop:r+J.top})}),[X,rt,J.top,I,ot,et]);return Y<10?null:(0,k.jsxs)("div",{children:[(0,k.jsxs)("svg",{height:e,width:Y,children:[(0,k.jsx)(s.Z,{fill:"transparent",height:e-(J.top+J.bottom),onMouseLeave:function(){return r()},onMouseMove:it,onTouchMove:it,onTouchStart:it,rx:14,width:Y-J.left,x:J.left,y:0}),(0,k.jsxs)(h.Z,{left:J.left,top:J.top,children:[(0,k.jsx)(d.Z,{color:K,data:X,height:et,keys:G,pointerEvents:"none",xScale:Q,y:V,yScale:W,children:function(t){return t.map((function(t){return t.bars.map((function(n){return(0,k.jsx)("g",{children:(0,k.jsx)(k.Fragment,{children:(0,k.jsx)("rect",{fill:q.backgroundPrimary,height:n.height,pointerEvents:"none",rx:4,width:n.width,x:n.x,y:n.y})})},"barstack-horizontal-".concat(t.index,"-").concat(n.index))}))}))}}),(0,k.jsx)(u.Z,{hideTicks:!0,scale:W,stroke:q.muted,tickFormat:function(t){return B(t)},tickLabelProps:function(){return{fill:q.active,fontFamily:E.ry,fontSize:z,style:{width:"10px"},textAnchor:"end"}},tickStroke:q.muted,tickValues:$,top:2}),(0,k.jsx)(l.Z,{label:N,labelProps:{fill:q.muted,fontFamily:E.ry,fontSize:z,textAnchor:"middle"},numTicks:F,scale:Q,stroke:q.muted,tickLabelProps:function(){return{fill:q.active,fontFamily:E.ry,fontSize:z,textAnchor:"middle"}},tickStroke:q.muted,top:et})]}),P&&(0,k.jsx)("g",{children:(0,k.jsx)(f.Z,{from:{x:J.left,y:R},pointerEvents:"none",stroke:_.Ej,strokeDasharray:"5,2",strokeWidth:1,to:{x:nt+J.left,y:R}})})]}),L&&P&&(0,k.jsx)(g.Z,{left:M,style:D(D({},v.j),{},{backgroundColor:q.tooltipBackground}),top:R,children:(0,k.jsxs)(w.ZP,{black:!0,small:!0,children:[null===S||void 0===S?void 0:S(P),!S&&T(P).toFixed(4)]})})]})}));n.Z=function(t){var n=t.height,e=t.width,o=(0,r.Z)(t,I);return(0,k.jsx)("div",{style:{height:n,width:"undefined"===typeof e?"100%":e},children:(0,k.jsx)(c.Z,{children:function(t){var n=t.width,e=t.height;return(0,k.jsx)(M,D(D({},o),{},{height:e,width:n}))}})})}},66872:function(t,n,e){e.d(n,{Z:function(){return H}});var r=e(26304),o=e(21831),i=e(82394),a=e(82684),c=e(26226),u=e(84969),l=e(90948),s=e(65743),d=e(29989),f=e(38626),h=e(61655),p=e(16853),m=e(65376),g=e(48072),v=e(98677),x=e(84181),y=e(67971),b=e(54283),j=e(19711),w=e(52359),Z=e(31969),_=e(73899),O=e(88560),S=e(2005),E=e(31012),k=e(49125),I=e(88543),P=e(6568),D=function(t){return t.slice(0,10)},A=function(t,n){var e=t.toISOString().slice(0,10),r=n.toISOString().slice(0,10);return"".concat(e,":").concat(r)},T=e(344),C=e(45739),M=e(28598),L=["height","loading","selected","width","xAxisLabel","yAxisLabel"];function R(t,n){var e=Object.keys(t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(t);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(t,n).enumerable}))),e.push.apply(e,r)}return e}function Y(t){for(var n=1;n<arguments.length;n++){var e=null!=arguments[n]?arguments[n]:{};n%2?R(Object(e),!0).forEach((function(n){(0,i.Z)(t,n,e[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(e)):R(Object(e)).forEach((function(n){Object.defineProperty(t,n,Object.getOwnPropertyDescriptor(e,n))}))}return t}var N={bottom:k.iI,left:3*k.iI,right:0,top:1*k.iI},F=(0,h.Z)((function(t){var n=t.columnType,e=t.data,r=void 0===e?[]:e,i=t.getBarColor,c=t.getXValue,h=t.getYValue,y=t.height,b=t.hideTooltip,w=t.large,L=t.margin,R=void 0===L?{}:L,F=t.muted,H=t.noPadding,V=t.numberOfXTicks,B=t.renderTooltipContent,z=t.selected,U=t.showAxisLabels,J=t.showTooltip,X=t.showYAxisLabels,G=t.showZeroes,K=t.sortData,Q=t.tooltipData,W=t.tooltipLeft,q=t.tooltipOpen,$=t.tooltipTop,tt=t.width,nt=t.xLabelFormat,et=t.yLabelFormat,rt=w?E.J5:E.VK,ot=(0,a.useCallback)((function(t){return c?c(t):t[0]}),[c]),it=(0,a.useCallback)((function(t){return h?h(t):t[1]}),[h]),at=(0,a.useContext)(f.ThemeContext),ct=n===O.RL.DATETIME,ut=Y(Y({},N),R);U&&(ut=Y(Y({},ut),{},{left:ut.left+k.iI}));var lt=K?K(r):r.sort((function(t,n){return n[1]-t[1]})),st=ct?r.sort((function(t,n){return new Date(t[0])-new Date(n[0])})).filter((function(t){return!!t[0]})):lt.slice(0,60),dt=tt-(ut.left+ut.right),ft=y-(ut.bottom+ut.top),ht=ct?function(t,n){var e,r=t.map((function(t){return new Date(t[0])})).sort((function(t,n){return t-n}));return(0,P.Z)({domain:(e=r,[(0,I.Z)(e[0]),(0,I.Z)(e[e.length-1])]),nice:!0,range:[0,n]})}(st,dt):null,pt=function(t,n){if(null===n)return{};var e=n.ticks().map((function(t){return t.toISOString()})),r={},o=0,i=1;return t.forEach((function(t){var n=new Date(t[0]),a=t[1],c=e[o],u=e[i];if(c&&u){var l=new Date(c),s=new Date(u),d=A(l,s);if(n>=l&&n<s)r[d]=(r[d]||0)+a;else for(;i<e.length||!r[d];)if(o+=1,i+=1,l=new Date(e[o]),s=new Date(e[i]),d=A(l,s),n>=l&&n<s)return void(r[d]=(r[d]||0)+a)}})),e.reduce((function(t,n,e,r){if(0===e)return t;var o=D(n),i=D(r[e-1]);return t.push("".concat(i,":").concat(o)),t}),[]).forEach((function(t){r[t]=r[t]||0})),r}(st,ht);st=ht?Object.entries(pt).sort((function(t,n){return new Date(D(t[0]))-new Date(D(n[0]))})):st;var mt=ht?Math.max.apply(Math,(0,o.Z)(Object.values(pt))):0,gt=st.reduce((function(t,n){return(0!==it(n)||ct||G)&&t.push(ot(n)),t}),[]),vt=gt.length,xt=function(t,n,e){return e?.05:t>=30&&n<300?.5:t>=15?.3:t>=5?.1:t>2?.05:2===t?.025:0}(vt,tt,ct),yt=(0,v.Z)({domain:gt,paddingInner:H?null:xt,range:[0,dt],round:!1}),bt=(0,x.Z)({domain:[0,Math.max.apply(Math,(0,o.Z)(st.map(it)))],range:[ft,0],round:!0}),jt=(0,C.K)(at),wt={active:((null===at||void 0===at?void 0:at.content)||Z.Z.content).active,default:jt[0],muted:((null===at||void 0===at?void 0:at.monotone)||Z.Z.monotone).gray,selected:((null===at||void 0===at?void 0:at.elevation)||Z.Z.elevation).visualizationAccent},Zt=wt.default;F?Zt=wt.muted:z&&(Zt=wt.selected);var _t=vt?ct?mt:Math.max.apply(Math,(0,o.Z)(st.map((function(t){return it(t)})))):0,Ot=Math.floor(_t/6),St=[0],Et=0;if(_t>6)for(;Et<_t;)St.push(Et+Ot),Et+=Ot;else for(;Et<=_t;)St.push(Et+1),Et+=1;_t>9999?ut=Y(Y({},ut),{},{left:w?8*k.iI:4.1*k.iI}):_t>999&&(ut=Y(Y({},ut),{},{left:w?5*k.iI:3.6*k.iI}));var kt=ct?2.25:0,It=vt<10||n===O.RL.NUMBER||n===O.RL.NUMBER_WITH_DECIMALS||ct||X,Pt=(0,a.useCallback)((function(t){var n=(0,g.Z)(t)||{x:0,y:0},e=n.x,r=n.y,o=(e-(U?ut.left:0))/dt,i=Math.floor(vt*o),a=st[i];"undefined"===typeof a&&(a=st[0]);var c=ot(a);c=c.length>15?"".concat(c.slice(0,21)):c;var u=B?B(a):"".concat(c," (").concat(it(a),")");J({tooltipData:u,tooltipLeft:e-ut.left,tooltipTop:r+ut.top})}),[st,vt,ot,it,ut.left,ut.top,B,U,J,tt]);return tt<10||!r.length?null:(0,M.jsxs)("div",{children:[(0,M.jsxs)("svg",{height:y+ut.bottom*(ct?7.5:3),width:tt,children:[(0,M.jsx)(d.Z,{left:U?ut.left:0,top:ut.top+kt,children:st.reduce((function(t,n){var e=ot(n),r=it(n);if(0!==r){var o,a=yt.bandwidth(),c=ft-(null!==(o=bt(r))&&void 0!==o?o:0),u=yt(e),l=ft-c;t.push((0,M.jsx)(s.Z,{fill:i?i(n):Zt,height:c,onMouseLeave:function(){return b()},onMouseMove:Pt,onTouchMove:Pt,onTouchStart:Pt,width:a,x:u,y:l},"bar-".concat(e)))}return t}),[])}),U&&(0,M.jsxs)(M.Fragment,{children:[(0,M.jsx)(u.Z,{left:ut.left,scale:bt,stroke:wt.muted,tickFormat:function(t){return et?et(t):(0,T.P5)(t)},tickLabelProps:function(){return{fill:wt.active,fontFamily:S.ry,fontSize:rt,textAnchor:"end",transform:"translate(-2,2.5)"}},tickStroke:wt.muted,tickValues:St,top:ut.top+kt}),(0,M.jsx)(l.Z,{left:ut.left,numTicks:ct?void 0:V||6,orientation:"top",scale:ht||yt,stroke:wt.muted,tickFormat:function(t){return nt?nt(String(t)):ct?t.toISOString().slice(0,10):String(t)},tickLabelProps:function(t){return{fill:It?wt.active:"transparent",fontFamily:S.ry,fontSize:rt,textAnchor:"middle",transform:ct?"rotate(-90,".concat(ht(t),",0) translate(-33,10)"):"translate(0, ".concat(3*ut.bottom,")")}},tickLineProps:{transform:"translate(0,".concat(k.iI,")")},tickStroke:It?wt.muted:"transparent",top:ft+ut.top+kt})]})]}),q&&Q&&(0,M.jsx)(p.Z,{left:W,style:m.j,top:$,children:(0,M.jsx)(j.ZP,{color:_.E5,small:!0,children:Q})})]})}));var H=function(t){var n=t.height,e=t.loading,o=t.selected,i=t.width,a=t.xAxisLabel,u=t.yAxisLabel,l=(0,r.Z)(t,L);return(0,M.jsxs)(M.Fragment,{children:[(0,M.jsxs)("div",{style:{display:"flex",height:n,marginBottom:k.iI,width:"100%"},children:[u&&(0,M.jsx)(y.Z,{alignItems:"center",fullHeight:!0,justifyContent:"center",width:28,children:(0,M.jsx)(w.Z,{children:(0,M.jsx)(j.ZP,{center:!0,muted:!0,small:!0,children:u})})}),(0,M.jsxs)("div",{style:{height:n,width:u?0===i?i:i-28:i},children:[e&&(0,M.jsx)(b.Z,{}),!e&&(0,M.jsx)(c.Z,{children:function(t){var n=t.height,e=t.width;return(0,M.jsx)(F,Y(Y({},l),{},{height:n,selected:o,width:e}))}})]})]}),a&&(0,M.jsx)("div",{style:{paddingLeft:u?36:0,paddingTop:4},children:(0,M.jsx)(j.ZP,{center:!0,muted:!0,small:!0,children:a})})]})}},320:function(t,n,e){e.d(n,{Z:function(){return k}});var r=e(26304),o=e(82394),i=e(75582),a=e(26226),c=e(28940),u=e(82684),l=e(29989),s=e(38626),d=e(11684),f=e(24903),h=e(19711),p=e(23831),m=e(2005),g=e(31012),v=e(49125),x=e(45739),y=e(28598),b=["height","width","xAxisLabel"];function j(t,n){var e=Object.keys(t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(t);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(t,n).enumerable}))),e.push.apply(e,r)}return e}function w(t){for(var n=1;n<arguments.length;n++){var e=null!=arguments[n]?arguments[n]:{};n%2?j(Object(e),!0).forEach((function(n){(0,o.Z)(t,n,e[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(e)):j(Object(e)).forEach((function(n){Object.defineProperty(t,n,Object.getOwnPropertyDescriptor(e,n))}))}return t}var Z={bottom:0,left:0,right:0,top:0},_=function(t){var n=t.endAngle;return{endAngle:n>Math.PI?2*Math.PI:0,opacity:0,startAngle:n>Math.PI?2*Math.PI:0}},O=function(t){var n=t.startAngle;return{endAngle:t.endAngle,opacity:1,startAngle:n}};function S(t){var n=t.animate,e=t.arcs,r=t.path,o=t.getKey,a=t.getColor,c=t.onClickDatum,u=t.textColor;return(0,d.useTransition)(e,{enter:O,from:n?_:O,keys:o,leave:n?_:O,update:O})((function(t,n,e){var l=e.key,s=r.centroid(n),f=(0,i.Z)(s,2),h=f[0],p=f[1],v=n.endAngle-n.startAngle>=.1;return(0,y.jsxs)("g",{children:[(0,y.jsx)(d.animated.path,{d:(0,d.to)([t.startAngle,t.endAngle],(function(t,e){return r(w(w({},n),{},{endAngle:e,startAngle:t}))})),fill:a(n),onClick:function(){return c(n)},onTouchStart:function(){return c(n)}}),v&&(0,y.jsx)(d.animated.g,{style:{opacity:t.opacity},children:(0,y.jsx)("text",{dy:".33em",fill:u,fontFamily:m.ry,fontSize:g.J5,pointerEvents:"none",textAnchor:"middle",x:h,y:p,children:o(n)})})]},l)}))}function E(t){var n=t.animate,e=void 0===n||n,r=t.data,o=t.getX,i=t.getY,a=t.height,d=t.margin,h=void 0===d?Z:d,m=t.textColor,g=t.width,b=(0,u.useState)(null),j=b[0],_=b[1],O=(0,u.useContext)(s.ThemeContext),E=m||(null===O||void 0===O?void 0:O.content.active)||p.Z.content.active;if(g<10)return null;var k=(0,f.Z)({domain:r.map((function(t){return o(t)})),range:(0,x.K)(O)}),I=g-h.left-h.right,P=a-h.top-h.bottom,D=Math.min(I,P)/2,A=P/2,T=I/2,C=Math.min(I/4,12*v.iI);return(0,y.jsx)("svg",{height:a,width:g,children:(0,y.jsx)(l.Z,{left:T+h.left,top:A+h.top,children:(0,y.jsx)(c.Z,{cornerRadius:v.iI/2,data:j?r.filter((function(t){return JSON.stringify(t)===JSON.stringify(j)})):r,innerRadius:Math.max(D-C,12.25),outerRadius:D,padAngle:.005,pieValue:i,children:function(t){return(0,y.jsx)(S,w(w({},t),{},{animate:e,getColor:function(t){var n=t.data;return k(o(n))},getKey:function(t){var n=t.data;return o(n)},onClickDatum:function(t){var n=t.data;return e&&_(j&&JSON.stringify(j)===JSON.stringify(n)?null:n)},textColor:E}))}})})})}function k(t){var n=t.height,e=t.width,o=t.xAxisLabel,i=(0,r.Z)(t,b),c={};return"undefined"!==typeof n&&(c.height=n),"undefined"!==typeof e&&(c.width=e),(0,y.jsxs)(y.Fragment,{children:[(0,y.jsx)("div",{style:c,children:(0,y.jsx)(a.Z,{children:function(t){var n=t.width,e=t.height;return(0,y.jsx)(E,w(w({},i),{},{height:e,width:n}))}})}),o&&(0,y.jsx)("div",{style:{paddingTop:4},children:(0,y.jsx)(h.ZP,{center:!0,muted:!0,small:!0,children:o})})]})}},45739:function(t,n,e){e.d(n,{K:function(){return o}});var r=e(31969),o=function(t){var n=t||r.Z,e=n.brand,o=e.earth200,i=e.earth300,a=e.earth400,c=e.energy200,u=e.energy300,l=e.energy400,s=e.fire200,d=e.fire300,f=e.fire400,h=e.water200,p=e.water300,m=e.water400,g=e.wind200,v=e.wind300,x=e.wind400,y=n.chart;return[y.backgroundPrimary,y.backgroundSecondary,y.backgroundTertiary].concat([x,m,f,l,a,v,p,d,u,i,g,h,s,c,o])}},52359:function(t,n,e){var r=e(38626).default.div.withConfig({displayName:"YAxisLabelContainer",componentId:"sc-qwp21x-0"})(["-webkit-transform:rotate(-90deg);-moz-transform:rotate(-90deg);-o-transform:rotate(-90deg);-ms-transform:rotate(-90deg);transform:rotate(-90deg);white-space:nowrap;"]);n.Z=r},344:function(t,n,e){e.d(n,{P5:function(){return o},Vs:function(){return i}});e(90211);var r=Intl.NumberFormat("en-US",{notation:"compact",maximumFractionDigits:2});function o(t){return"number"!==typeof t?t:t>=1e4?r.format(t):t.toString()}function i(t,n,e){var r,o;if("undefined"===typeof t||"undefined"===typeof n)return 0;var i=null===t||void 0===t||null===(r=t(n,e))||void 0===r||null===(o=r.props)||void 0===o?void 0:o.children;return(Array.isArray(i)?i:[i]).join("").length}},66607:function(t,n,e){e.d(n,{j:function(){return x},Z:function(){return O}});var r=e(82394),o=e(66176),i=e(82684),a=e(60328),c=e(67971),u=e(19711),l=e(10503),s=e(49125),d=e(84779),f=e(28598),h=2*s.iI,p=function(t){var n=t.danger,e=t.decrease,r=t.increase,o=t.percentage,s=t.success,p=e?(0,f.jsx)(l.K5,{}):r&&(0,f.jsx)(l.a2,{});return(0,f.jsx)(a.Z,{danger:n,notClickable:!0,padding:"2px 6px",success:s,children:(0,f.jsxs)(c.Z,{alignItems:"center",children:[(0,f.jsx)(u.ZP,{danger:n,success:s,children:(0,d.DU)(o)}),p&&i.cloneElement(p,{danger:n,size:h,success:s})]})})},m=e(86673),g=e(93461),v=e(70759);var x,y=function(t){var n=t.border,e=t.children,r=t.columnFlexNumbers,o=t.condensed,a=t.flexStart,u=t.last,l=t.noHorizontalPadding,s=t.secondary;return(0,f.jsx)(v.gI,{border:n,condensed:o,last:u,noHorizontalPadding:l,secondary:s,children:(0,f.jsx)(c.Z,{alignItems:a?"flex-start":"center",children:i.Children.map(e,(function(t,n){return t&&r?(0,f.jsx)(g.Z,{alignItems:"center",flex:r[n],children:t},"row-card-item-".concat(n)):t}))})})},b=e(11754),j=e(90211);function w(t,n){var e=Object.keys(t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(t);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(t,n).enumerable}))),e.push.apply(e,r)}return e}function Z(t){for(var n=1;n<arguments.length;n++){var e=null!=arguments[n]?arguments[n]:{};n%2?w(Object(e),!0).forEach((function(n){(0,r.Z)(t,n,e[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(e)):w(Object(e)).forEach((function(n){Object.defineProperty(t,n,Object.getOwnPropertyDescriptor(e,n))}))}return t}!function(t){t.INCREASE="increase",t.DECREASE="decrease"}(x||(x={}));var _=function(t,n){return t&&t.compare(n,t.val)};var O=function(t){var n=t.stats,e=t.title;return(0,f.jsx)(b.Z,{alternating:!0,headerTitle:e,children:null===n||void 0===n?void 0:n.map((function(t,n){var e=t.change,r=t.columnFlexNumbers,i=t.name,a=t.progress,c=t.rate,l=t.successDirection,s=void 0===l?x.INCREASE:l,d=t.value,h=t.warning,g={bold:_(h,c),danger:_(h,c)};return(0,f.jsxs)(y,{columnFlexNumbers:r||[1,1,1],condensed:!!e,children:[(0,f.jsx)(u.ZP,{default:!0,children:i}),(0,f.jsxs)(f.Fragment,{children:[void 0!==d&&(0,f.jsx)(m.Z,{pr:1,children:(0,f.jsx)(u.ZP,Z(Z({default:!0},g),{},{children:d}))}),void 0!==c&&(0,f.jsx)(m.Z,{pr:1,children:(0,f.jsx)(u.ZP,Z(Z({default:!0},g),{},{children:function(t,n){return void 0!==t?"(".concat((0,j.T3)(n),")"):(0,j.T3)(n)}(d,c)}))}),(e<0||e>0)&&(0,f.jsx)(m.Z,{pr:1,children:(0,f.jsx)(p,{danger:s===x.DECREASE?e>0:e<0,decrease:e<0,increase:e>0,percentage:Math.abs(e),success:s===x.INCREASE?e>0:e<0})})]}),a&&(0,f.jsx)(o.Z,Z({progress:100*c},g))]},"".concat(i,"_").concat(n))}))})}},43313:function(t,n,e){e.d(n,{CC:function(){return g},Dy:function(){return s},Iw:function(){return f},OD:function(){return b},Sq:function(){return x},Ub:function(){return v},Zu:function(){return d},bC:function(){return j},lb:function(){return h},mG:function(){return w},no:function(){return p},oH:function(){return y},y_:function(){return m}});var r,o,i=e(21831),a=e(82394),c=e(88560),u=e(66607),l=e(24224),s=["duplicate_row_count","completeness","total_invalid_value_count","total_null_value_count","validity"],d=["count","empty_column_count"],f=["category","category_high_cardinality","true_or_false"],h=["datetime"],p=["number","number_with_decimals"],m=["completeness","validity"],g={completeness:"Completeness",count:"Row count",duplicate_row_count:"Duplicate rows",empty_column_count:"Empty columns",total_invalid_value_count:"Invalid cells",total_null_value_count:"Missing cells",validity:"Validity"},v={completeness:1,duplicate_row_count:4,total_invalid_value_count:3,total_null_value_count:2,validity:0},x={duplicate_row_count:"duplicate_row_rate",total_invalid_value_count:"total_invalid_value_rate",total_null_value_count:"total_null_value_rate"},y={column_count:u.j.INCREASE,completeness:u.j.INCREASE,count:u.j.INCREASE,duplicate_row_count:u.j.DECREASE,empty_column_count:u.j.DECREASE,total_invalid_value_count:u.j.DECREASE,total_null_value_count:u.j.DECREASE,validity:u.j.INCREASE},b={completeness:{compare:l.Qj,val:.8},duplicate_row_count:{compare:l.tS,val:0},empty_column_count:{compare:l.tS,val:0},total_invalid_value_count:{compare:l.tS,val:0},total_null_value_count:{compare:l.tS,val:0},validity:{compare:l.Qj,val:.8}},j=(l.Qj,l.Qj,l.tS,l.tS,r={},(0,a.Z)(r,c.RL.EMAIL,"domain_distribution"),(0,a.Z)(r,c.RL.TEXT,"word_distribution"),(0,a.Z)(r,c.RL.LIST,"element_distribution"),(0,a.Z)(r,"default","value_counts"),r),w=[].concat((0,i.Z)(c.P_),[c.RL.TEXT,c.RL.EMAIL,c.RL.LIST]);o={},(0,a.Z)(o,c.RL.EMAIL,"Domain distribution"),(0,a.Z)(o,c.RL.TEXT,"Word distribution"),(0,a.Z)(o,c.RL.LIST,"Element distribution"),(0,a.Z)(o,"default","Distribution of values")},6753:function(t,n,e){e.d(n,{AE:function(){return o},H3:function(){return i},mW:function(){return a},oE:function(){return c},yg:function(){return r}});var r="tabs[]",o="show_columns",i="column",a="Reports",c="Visualizations"},1286:function(t,n,e){e.d(n,{O$:function(){return E},Fk:function(){return I},QO:function(){return k}});var r,o,i=e(75582),a=e(12691),c=e.n(a),u=e(70001),l=e(93461),s=e(66872),d=e(10919),f=e(320),h=e(19711),p=e(43313),m=e(86585);!function(t){t.RANGE="range"}(r||(r={})),function(t){t.BAR_HORIZONTAL="bar_horizontal",t.LINE_CHART="line_chart",t.HISTOGRAM="histogram"}(o||(o={}));var g=e(88560),v=e(6753),x=e(49125),y=e(21831),b=e(92083),j=e.n(b),w=e(90211),Z=e(24224);function _(t,n){var e,o=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{},i=o||{},a=i.calculateAnomaly,c=i.feature,u=i.getYValue,l=t.x,s=t.x_metadata,d=s.label,f=s.label_type,h=t.y,p=(null===h||void 0===h?void 0:h.map((function(t){return null===u||void 0===u?void 0:u(t)})))||[],m=Math.max.apply(Math,(0,y.Z)(p)),v=Math.max.apply(Math,(0,y.Z)(p)),x=(0,Z.Sm)(p),b=(0,Z.IN)(p),_=x/Math.max(1,p.length),O=n[d]||c,S=null===O||void 0===O?void 0:O.columnType,E=g.RL.DATETIME===S,k=[],I=[],P=l.length,D=l.map((function(t,n){var o,i,c,u,l=t.label,s=t.max,d=t.min,y=h[n];if(r.RANGE===f)if(e||(e=s-d),u=g.RL.NUMBER===S&&e<=P)o=Number(d);else if(o=e/2+d,E){var Z="M/D/YYYY",O="M/D/YYYY",D="M/D/YYYY";e<=1?(Z=e<=.1?"H:mm:ss.SSS":"H:mm:ss",O="H:mm:ss.SSS",D="H:mm:ss.SSS"):e<=60?(Z="H:mm",O="H:mm:ss",D="H:mm:ss"):e<=3600?(Z="H:mm",O="M/D/YYYY H:mm",D="H:mm"):e<=86400&&(O="M/D/YYYY H:mm",D="M/D/YYYY H:mm"),o=j().unix(o).format(Z),i=j().unix(d).format(O),c=j().unix(s).format(D)}else o=(0,w.QV)(o);else o=l;var A=n>=1?h[n-1]:null,T=!1;a&&(T=a({x:t,y:y,yPrevious:A,yValues:p,yValuesAverage:_,yValuesMax:m,yValuesMin:v,yValuesStandardDeviation:b,yValuesSum:x}));var C={hideRange:u,isUnusual:T,x:t,xLabel:o,xLabelMax:c,xLabelMin:i,y:y};return T&&(u?I.push(C):k.push(C)),C}));return{distribution:{data:D,featureUUID:d},rangedWithUnusualDistribution:(0,Z.YC)(k,(function(t){var n=t.y;return u(n)}),{ascending:!1}),unusualDistribution:(0,Z.YC)(I,(function(t){var n=t.y;return u(n)}),{ascending:!1})}}var O=e(20567),S=e(28598);var E=12*x.iI;function k(t){if("undefined"===typeof t)return{};var n=0,e=0,r=0;return t.forEach((function(t){p.Iw.includes(t)?n+=1:p.no.includes(t)?r+=1:p.lb.includes(t)&&(e+=1)})),{countCategory:n,countDatetime:e,countNumerical:r}}function I(t){var n=t.columnTypes,e=t.columns,r=t.insightsByFeatureUUID,a=t.insightsOverview,y=t.noColumnLinks,b=void 0!==y&&y,j=t.statistics;return function(t,y,k){var I=k.width,P=e[y],D=n[P],A=m.T5[D],T=(r[P]||{}).charts,C=a.time_series,M=e.filter((function(t){return n[t]===g.RL.DATETIME})),L=null===C||void 0===C?void 0:C.map((function(t){return _(t,{},{feature:{columnType:D,uuid:P}}).distribution})),R={};null===L||void 0===L||L.forEach((function(t,n){var e=t.data;R[M[n]]=(0,S.jsx)(s.Z,{data:e.map((function(t){var n=t.x,e=t.xLabel,r=t.xLabelMax,o=t.xLabelMin;return[e,t.y.count,o,r,n.min,n.max]})),height:E,large:!0,margin:{bottom:0,left:0,right:0,top:0},renderTooltipContent:function(t){var n=(0,i.Z)(t,4),e=n[1],r=n[2],o=n[3];return(0,S.jsxs)("p",{children:["Rows: ",e,(0,S.jsx)("br",{}),"Start: ",r,(0,S.jsx)("br",{}),"End: ",o]})},sortData:function(t){return(0,Z.YC)(t,"[4]")}},P)}));var Y,N=null===T||void 0===T?void 0:T.find((function(t){var n=t.type;return o.HISTOGRAM===n})),F=(N?_(N,{},{feature:{columnType:D,uuid:P},getYValue:function(t){return t.value}}):{}).distribution,H=void 0===F?null:F,V=p.bC[D]||p.bC.default,B=null===j||void 0===j?void 0:j["".concat(P,"/").concat(V)],z=Object.entries(B||{}).map((function(t){var n=(0,i.Z)(t,2),e=n[0];return{x:n[1],y:e}})),U=g.RL.TRUE_OR_FALSE===D;if(g.RL.DATETIME===D)Y=R[P];else if(H&&!U)Y=(0,S.jsx)(s.Z,{data:H.data.map((function(t){var n=t.hideRange,e=t.isUnusual,r=t.x;return[t.xLabel,t.y.value,r.min,r.max,e,n]})),height:E,margin:{bottom:0,left:0,right:0,top:0},renderTooltipContent:function(t){var n=(0,i.Z)(t,6),e=n[1],r=n[2],o=n[3],a=n[5];return(0,S.jsxs)("p",{children:[a&&(0,S.jsxs)(S.Fragment,{children:["Rows: ",e,(0,S.jsx)("br",{}),"Value: ",r]}),!a&&(0,S.jsxs)(S.Fragment,{children:["Rows: ",e,(0,S.jsx)("br",{}),"Range: ",r," - ",o]})]})},sortData:function(t){return(0,Z.YC)(t,"[2]")},width:I-2*x.iI});else if(p.mG.includes(D)){var J=(0,Z.YC)((0,Z.YC)(z,"x",{ascending:!1}).slice(0,5),"x");Y=(0,S.jsx)(u.Z,{data:J,height:E,margin:{bottom:0,left:0,right:20,top:0},renderTooltipContent:function(t){var n=t.x,e=t.y;return"".concat(e," appears ").concat((0,w.x6)(n)," times")},xNumTicks:2,ySerialize:function(t){return t.y}})}else U&&B&&(Y=(0,S.jsx)(f.Z,{data:Object.entries(B),getX:function(t){var n=(0,i.Z)(t,2),e=n[0],r=n[1];return"".concat(e," (").concat((0,w.x6)(r),")")},getY:function(t){return(0,i.Z)(t,2)[1]},height:E}));return(0,S.jsxs)("div",{style:{padding:x.iI},children:[(0,S.jsxs)("div",{style:{alignItems:"center",display:"flex",marginBottom:x.iI},children:[A&&(0,S.jsx)(l.Z,{title:g.Rp[D],children:(0,S.jsx)(A,{size:2*x.iI})}),(0,S.jsx)("div",{style:{marginLeft:.5*x.iI,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap",width:I-4.5*x.iI},children:b?(0,S.jsx)(h.ZP,{bold:!0,default:!0,title:e[y],children:e[y]}):(0,S.jsx)(c(),{as:(0,O.o_)(v.oE,y),href:"/datasets/[...slug]",passHref:!0,children:(0,S.jsx)(d.Z,{bold:!0,monospace:!0,secondary:!0,small:!0,title:e[y],children:e[y]})})})]}),Y,!Y&&(0,S.jsx)("div",{style:{height:E}})]})}}},20567:function(t,n,e){e.d(n,{o_:function(){return u}});var r=e(75582),o=e(34376),i=e(6753);e(82684),e(12691),e(60328),e(57639),e(93461),e(67971),e(10919),e(86673),e(19711),e(10503),e(28598);var a,c=e(59e3);!function(t){t.DATASETS="datasets",t.DATASET_DETAIL="dataset_detail",t.COLUMNS="features",t.COLUMN_DETAIL="feature_detail",t.EXPORT="export"}(a||(a={}));var u=function(t,n){var e=(0,o.useRouter)().query.slug,u=void 0===e?[]:e,l=(0,r.Z)(u,1)[0],s=(0,c.iV)(),d=s.show_columns,f=s.column,h="/".concat(a.DATASETS,"/").concat(l),p="".concat(i.H3,"=").concat(f||n),m="".concat(i.yg,"=").concat(t,"&").concat(p,"&").concat(i.AE,"=").concat(d||0);return"".concat(h,"?").concat(m)}},66176:function(t,n,e){var r=e(82394),o=e(91835),i=(e(82684),e(38626)),a=e(23831),c=e(73942),u=e(49125),l=e(28598);function s(t,n){var e=Object.keys(t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(t);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(t,n).enumerable}))),e.push.apply(e,r)}return e}function d(t){for(var n=1;n<arguments.length;n++){var e=null!=arguments[n]?arguments[n]:{};n%2?s(Object(e),!0).forEach((function(n){(0,r.Z)(t,n,e[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(e)):s(Object(e)).forEach((function(n){Object.defineProperty(t,n,Object.getOwnPropertyDescriptor(e,n))}))}return t}var f=i.default.div.withConfig({displayName:"ProgressBar__ProgressBarContainerStyle",componentId:"sc-10x9ojc-0"})(["border-radius:","px;height:","px;overflow:hidden;position:relative;width:100%;",""],c.BG,.75*u.iI,(function(t){return"\n    background-color: ".concat((t.theme.monotone||a.Z.monotone).grey200,";\n  ")})),h=i.default.div.withConfig({displayName:"ProgressBar__ProgressBarStyle",componentId:"sc-10x9ojc-1"})(["height:inherit;position:absolute;"," "," "," ",""],(function(t){return!t.danger&&"\n    background-color: ".concat((t.theme.progress||a.Z.progress).positive,";\n  ")}),(function(t){return t.progress&&"\n    width: ".concat(t.progress,"%;\n  ")}),(function(t){return t.danger&&"\n    background-color: ".concat((t.theme.progress||a.Z.progress).negative,";\n  ")}),(function(t){return t.animateProgress&&"\n    animation: animate-progress ".concat(t.animateProgress.duration,"ms linear forwards;\n\n    @keyframes animate-progress {\n      0% {\n        width: ").concat(t.animateProgress.start,"%;\n      }\n\n      100% {\n        width: ").concat(t.animateProgress.end,"%;\n      }\n    }\n  ")}));n.Z=function(t){var n=(0,o.Z)({},t);return(0,l.jsx)(f,d(d({},n),{},{children:(0,l.jsx)(h,d({},n))}))}},70759:function(t,n,e){e.d(n,{$B:function(){return s},VH:function(){return d},gI:function(){return f},kA:function(){return l}});var r=e(38626),o=e(31969),i=e(73942),a=e(49125),c=1.5*a.iI,u=1.5*a.iI,l=r.default.div.withConfig({displayName:"indexstyle__TableStyle",componentId:"sc-13p7y8j-0"})(["",""],(function(t){return t.width&&"\n    width: ".concat(t.width,"px;\n  ")})),s=r.default.div.withConfig({displayName:"indexstyle__RowContainerStyle",componentId:"sc-13p7y8j-1"})(["border-bottom-left-radius:","px;border-bottom-right-radius:","px;margin-bottom:","px;"," "," ",""],i.n_,i.n_,c,(function(t){return"\n    background-color: ".concat((t.theme.background||o.Z.background).page,";\n    border: ").concat(i.YF,"px ").concat(i.M8," ").concat((t.theme.interactive||o.Z.interactive).defaultBorder,";\n    border-top: none;\n  ")}),(function(t){return t.minHeight>0&&"\n    min-height: ".concat(t.minHeight,"px;\n  ")}),(function(t){return t.scrollable&&"\n    margin-bottom: ".concat(a.iI,"px;\n    overflow-y: auto;\n    padding-top: ").concat(3,"px;\n    padding-left: ").concat(3,"px;\n    padding-right: ").concat(3,"px;\n  ")})),d=r.default.div.withConfig({displayName:"indexstyle__TitleStyle",componentId:"sc-13p7y8j-2"})(["border-top-left-radius:","px;border-top-right-radius:","px;padding:","px ","px;",""],i.n_,i.n_,c,2*a.iI,(function(t){return"\n    background-color: ".concat((t.theme.background||o.Z.background).header,";\n    border: ").concat(i.YF,"px ").concat(i.M8," ").concat((t.theme.interactive||o.Z.interactive).defaultBorder,";\n  ")})),f=r.default.div.withConfig({displayName:"indexstyle__RowStyle",componentId:"sc-13p7y8j-3"})(["padding:","px ","px;"," "," "," "," "," ",""],u,2*a.iI,(function(t){return t.noHorizontalPadding&&"\n    padding-left: 0;\n    padding-right: 0;\n  "}),(function(t){return t.condensed&&"\n    padding-top: ".concat(9,"px;\n    padding-bottom: ").concat(9,"px;\n  ")}),(function(t){return!t.secondary&&"\n    background-color: ".concat((t.theme.background||o.Z.background).row,";\n  ")}),(function(t){return t.secondary&&"\n    background-color: ".concat((t.theme.background||o.Z.background).row2,";\n  ")}),(function(t){return t.last&&"\n    border-bottom-left-radius: ".concat(i.n_,"px;\n    border-bottom-right-radius: ").concat(i.n_,"px;\n  ")}),(function(t){return t.border&&"\n    border: 1px solid ".concat((t.theme.monotone||o.Z.monotone).grey200,";\n    border-radius: ").concat(i.n_,"px;\n  ")}))},11754:function(t,n,e){var r=e(82684),o=e(67971),i=e(19711),a=e(70759),c=e(28598);n.Z=function(t){var n=t.alternating,e=t.children,u=t.headerDetails,l=t.headerTitle,s=t.minHeight,d=t.scrollable,f=t.width;return(0,c.jsxs)(a.kA,{width:f,children:[(0,c.jsx)(a.VH,{children:(0,c.jsxs)(o.Z,{alignItems:"center",justifyContent:"space-between",children:[(0,c.jsx)(i.ZP,{bold:!0,default:!0,children:l}),u&&(0,c.jsx)(i.ZP,{children:u})]})}),(0,c.jsx)(a.$B,{minHeight:s,scrollable:d,children:r.Children.map(e,(function(t,o){return t&&r.cloneElement(t,{last:o===e.length-1,secondary:n&&o%2===1})}))})]})}},84779:function(t,n,e){e.d(n,{DU:function(){return a},JI:function(){return c},Jw:function(){return i}});var r=e(75582),o=function(t){var n=String(t).split("."),e=(0,r.Z)(n,2),o=e[0],i=e[1];return"".concat(o.replace(/\B(?=(\d{3})+(?!\d))/g,",")).concat(i?".".concat(i):"")},i=function(t){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:3,e=parseFloat(t).toFixed(n);return 0===t&&(e=parseFloat(t).toFixed(0)),o(e)};function a(t){if(void 0===t)return"";var n=1===t||0===t?100*t:(100*t).toFixed(2);return"".concat(n,"%")}function c(t){var n=Math.floor(Date.now()/1e3);return t>0?n-t:n}}}]);