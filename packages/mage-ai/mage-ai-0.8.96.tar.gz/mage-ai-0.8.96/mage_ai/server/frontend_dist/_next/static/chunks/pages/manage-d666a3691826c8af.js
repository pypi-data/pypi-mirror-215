(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[8867],{59739:function(e,n,t){"use strict";var r=t(56669);function o(){}function i(){}i.resetWarningCache=o,e.exports=function(){function e(e,n,t,o,i,c){if(c!==r){var a=new Error("Calling PropTypes validators directly is not supported by the `prop-types` package. Use PropTypes.checkPropTypes() to call them. Read more at http://fb.me/use-check-prop-types");throw a.name="Invariant Violation",a}}function n(){return e}e.isRequired=e;var t={array:e,bigint:e,bool:e,func:e,number:e,object:e,string:e,symbol:e,any:e,arrayOf:n,element:e,elementType:e,instanceOf:n,node:e,objectOf:n,oneOf:n,oneOfType:n,shape:n,exact:n,checkPropTypes:i,resetWarningCache:o};return t.PropTypes=t,t}},47329:function(e,n,t){e.exports=t(59739)()},56669:function(e){"use strict";e.exports="SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED"},1210:function(e,n,t){"use strict";t.d(n,{Z:function(){return A}});var r=t(82394),o=t(21831),i=t(82684),c=t(47999),a=t(49894),u=t(93461),s=t(57384),l=t(41424),d=t(72454),f=t(28598);function p(e,n){var t=e.children;return(0,f.jsx)(d.HS,{ref:n,children:t})}var h=i.forwardRef(p),m=t(32063),b=t(85019),g=t(82531),x=t(66166),O=t(3055),v=t(49125),y=t(91427),S=t(24141);function w(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function _(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?w(Object(t),!0).forEach((function(n){(0,r.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):w(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var A=function(e){var n,t=e.after,r=e.afterHidden,p=e.afterWidth,w=e.afterWidthOverride,A=e.before,j=e.beforeWidth,Z=e.breadcrumbs,R=e.children,C=e.errors,E=e.headerMenuItems,N=e.headerOffset,k=e.mainContainerHeader,T=e.navigationItems,P=e.setErrors,D=e.subheaderChildren,I=e.title,H=e.uuid,M=(0,S.i)().width,L="dashboard_after_width_".concat(H),W="dashboard_before_width_".concat(H),z=(0,i.useRef)(null),F=(0,i.useState)(w?p:(0,y.U2)(L,p)),U=F[0],X=F[1],B=(0,i.useState)(!1),K=B[0],Y=B[1],Q=(0,i.useState)(A?Math.max((0,y.U2)(W,j),13*v.iI):null),G=Q[0],V=Q[1],q=(0,i.useState)(!1),$=q[0],J=q[1],ee=(0,i.useState)(null)[1],ne=g.ZP.projects.list({},{revalidateOnFocus:!1}).data,te=null===ne||void 0===ne?void 0:ne.projects,re=[];Z?re.push.apply(re,(0,o.Z)(Z)):(null===te||void 0===te?void 0:te.length)>=1&&re.push.apply(re,[{label:function(){var e;return null===(e=te[0])||void 0===e?void 0:e.name},linkProps:{href:"/"}},{bold:!0,label:function(){return I}}]),(0,i.useEffect)((function(){null===z||void 0===z||!z.current||K||$||null===ee||void 0===ee||ee(z.current.getBoundingClientRect().width)}),[K,U,$,G,z,ee,M]),(0,i.useEffect)((function(){K||(0,y.t8)(L,U)}),[r,K,U,L]),(0,i.useEffect)((function(){$||(0,y.t8)(W,G)}),[$,G,W]);var oe=(0,x.Z)(p);return(0,i.useEffect)((function(){w&&oe!==p&&X(p)}),[w,p,oe]),(0,f.jsxs)(f.Fragment,{children:[(0,f.jsx)(s.Z,{title:I}),(0,f.jsx)(l.Z,{breadcrumbs:re,menuItems:E,project:null===te||void 0===te?void 0:te[0],version:null===te||void 0===te||null===(n=te[0])||void 0===n?void 0:n.version}),(0,f.jsxs)(d.Nk,{children:[0!==(null===T||void 0===T?void 0:T.length)&&(0,f.jsx)(d.lm,{showMore:!0,children:(0,f.jsx)(b.Z,{navigationItems:T,showMore:!0})}),(0,f.jsx)(u.Z,{flex:1,flexDirection:"column",children:(0,f.jsxs)(m.Z,{after:t,afterHeightOffset:O.Mz,afterHidden:r,afterMousedownActive:K,afterWidth:U,before:A,beforeHeightOffset:O.Mz,beforeMousedownActive:$,beforeWidth:d.k1+(A?G:0),headerOffset:N,hideAfterCompletely:!0,leftOffset:A?d.k1:null,mainContainerHeader:k,mainContainerRef:z,setAfterMousedownActive:Y,setAfterWidth:X,setBeforeMousedownActive:J,setBeforeWidth:V,children:[D&&(0,f.jsx)(h,{children:D}),R]})})]}),C&&(0,f.jsx)(c.Z,{disableClickOutside:!0,isOpen:!0,onClickOutside:function(){return null===P||void 0===P?void 0:P(null)},children:(0,f.jsx)(a.Z,_(_({},C),{},{onClose:function(){return null===P||void 0===P?void 0:P(null)}}))})]})}},85307:function(e,n,t){"use strict";t.d(n,{$W:function(){return s},cl:function(){return l},cv:function(){return d},dE:function(){return u}});var r=t(38626),o=t(23831),i=t(73942),c=t(49125),a=t(37391),u=r.default.div.withConfig({displayName:"indexstyle__SectionStyle",componentId:"sc-7a1uhf-0"})(["border-radius:","px;padding:","px;",""],i.n_,c.cd*c.iI,(function(e){return"\n    background-color: ".concat((e.theme.background||o.Z.background).popup,";\n  ")})),s=r.default.div.withConfig({displayName:"indexstyle__CodeEditorStyle",componentId:"sc-7a1uhf-1"})(["padding-top:","px;",""],c.cd*c.iI,(function(e){return"\n    background-color: ".concat((e.theme.background||o.Z.background).codeTextarea,";\n  ")})),l=r.default.div.withConfig({displayName:"indexstyle__TableContainerStyle",componentId:"sc-7a1uhf-2"})(["overflow:auto;max-height:90vh;width:100%;"," "," "," "," ",""],a.w5,(function(e){return e.hideHorizontalScrollbar&&"\n    overflow-x: hidden;\n  "}),(function(e){return e.width&&"\n    width: ".concat(e.width,";\n  ")}),(function(e){return e.height&&"\n    height: ".concat(e.height,";\n  ")}),(function(e){return e.maxHeight&&"\n    max-height: ".concat(e.maxHeight,";\n  ")})),d=r.default.div.withConfig({displayName:"indexstyle__HeaderRowStyle",componentId:"sc-7a1uhf-3"})(["padding:","px;"," "," ",""],2*c.iI,(function(e){return"\n    background-color: ".concat((e.theme||o.Z).interactive.defaultBackground,";\n    border-bottom: ").concat(i.YF,"px ").concat(i.M8," ").concat((e.theme||o.Z).borders.medium,";\n  ")}),(function(e){return e.padding&&"\n    padding: ".concat(e.padding,"px;\n  ")}),(function(e){return e.rounded&&"\n    border-top-left-radius: ".concat(i.n_,"px;\n    border-top-right-radius: ").concat(i.n_,"px;\n  ")}))},65597:function(e,n,t){"use strict";t.d(n,{f:function(){return a}});var r=t(38626),o=t(23831),i=t(49125),c=t(73942),a=r.default.div.withConfig({displayName:"Tablestyle__PopupContainerStyle",componentId:"sc-8ammqd-0"})(["position:absolute;max-height:","px;z-index:10;border-radius:","px;padding:","px;"," "," "," ",""],58*i.iI,c.TR,2*i.iI,(function(e){return"\n    box-shadow: ".concat((e.theme.shadow||o.Z.shadow).popup,";\n    background-color: ").concat((e.theme.interactive||o.Z.interactive).defaultBackground,";\n  ")}),(function(e){return e.leftOffset&&"\n    left: ".concat(e.leftOffset,"px;\n  ")}),(function(e){return e.topOffset&&"\n    top: ".concat(e.topOffset,"px;\n  ")}),(function(e){return e.width&&"\n    width: ".concat(e.width,"px;\n  ")}))},84392:function(e,n,t){"use strict";t.d(n,{HF:function(){return c},L6:function(){return r}});var r,o=t(81132),i=t(10503);function c(e,n){var t=e.owner,c=e.roles,a=[{Icon:i.Vz,id:r.WORKSPACES,isSelected:function(){return r.WORKSPACES===n},label:function(){return"Workspaces"},linkProps:{href:"/manage"}}];return(t||c===o.No.ADMIN)&&a.push({Icon:i.NO,id:r.USERS,isSelected:function(){return r.USERS===n},label:function(){return"Users"},linkProps:{href:"/manage/users"}}),a}!function(e){e.WORKSPACES="workspaces",e.USERS="users",e.SETTINGS="settings"}(r||(r={}))},3849:function(e,n,t){"use strict";t(82684);var r=t(1210),o=t(49125),i=t(84392),c=t(9736),a=t(28598);n.Z=function(e){var n=e.before,t=e.breadcrumbs,u=void 0===t?[]:t,s=e.children,l=e.errors,d=e.pageName,f=e.subheaderChildren,p=(0,c.PR)()||{};return(0,a.jsx)(r.Z,{before:n,beforeWidth:n?50*o.iI:0,breadcrumbs:u,errors:l,navigationItems:(0,i.HF)(p,d),subheaderChildren:f,title:"Workspaces",uuid:"workspaces/index",children:s})}},86422:function(e,n,t){"use strict";t.d(n,{$W:function(){return h},DA:function(){return p},HX:function(){return g},J8:function(){return b},L8:function(){return c},Lq:function(){return d},M5:function(){return f},Qj:function(){return x},Ut:function(){return S},V4:function(){return y},VZ:function(){return m},dO:function(){return l},f2:function(){return v},iZ:function(){return O},t6:function(){return a},tf:function(){return s}});var r,o,i,c,a,u=t(82394);!function(e){e.CONDITION="condition",e.DBT_SNAPSHOT="snapshot",e.DYNAMIC="dynamic",e.DYNAMIC_CHILD="dynamic_child",e.REDUCE_OUTPUT="reduce_output",e.REPLICA="replica"}(c||(c={})),function(e){e.MARKDOWN="markdown",e.PYTHON="python",e.R="r",e.SQL="sql",e.YAML="yaml"}(a||(a={}));var s,l=(r={},(0,u.Z)(r,a.MARKDOWN,"MD"),(0,u.Z)(r,a.PYTHON,"PY"),(0,u.Z)(r,a.R,"R"),(0,u.Z)(r,a.SQL,"SQL"),(0,u.Z)(r,a.YAML,"YAML"),r);!function(e){e.CALLBACK="callback",e.CHART="chart",e.CONDITIONAL="conditional",e.CUSTOM="custom",e.DATA_EXPORTER="data_exporter",e.DATA_LOADER="data_loader",e.DBT="dbt",e.EXTENSION="extension",e.SCRATCHPAD="scratchpad",e.SENSOR="sensor",e.MARKDOWN="markdown",e.TRANSFORMER="transformer"}(s||(s={}));var d,f=[s.CALLBACK,s.CONDITIONAL,s.EXTENSION];!function(e){e.BLUE="blue",e.GREY="grey",e.PINK="pink",e.PURPLE="purple",e.TEAL="teal",e.YELLOW="yellow"}(d||(d={}));var p,h=[s.CHART,s.CUSTOM,s.DATA_EXPORTER,s.DATA_LOADER,s.SCRATCHPAD,s.SENSOR,s.MARKDOWN,s.TRANSFORMER],m=[s.DATA_EXPORTER,s.DATA_LOADER],b=[s.DATA_EXPORTER,s.DATA_LOADER,s.TRANSFORMER],g=[s.DATA_EXPORTER,s.DATA_LOADER,s.DBT,s.TRANSFORMER],x=[s.CHART,s.SCRATCHPAD,s.SENSOR,s.MARKDOWN],O=[s.CALLBACK,s.CHART,s.EXTENSION,s.SCRATCHPAD,s.MARKDOWN];!function(e){e.EXECUTED="executed",e.FAILED="failed",e.NOT_EXECUTED="not_executed",e.UPDATED="updated"}(p||(p={}));var v=[s.CUSTOM,s.DATA_EXPORTER,s.DATA_LOADER,s.TRANSFORMER],y=(o={},(0,u.Z)(o,s.EXTENSION,"Callback"),(0,u.Z)(o,s.CUSTOM,"Custom"),(0,u.Z)(o,s.DATA_EXPORTER,"Data exporter"),(0,u.Z)(o,s.DATA_LOADER,"Data loader"),(0,u.Z)(o,s.EXTENSION,"Extension"),(0,u.Z)(o,s.SCRATCHPAD,"Scratchpad"),(0,u.Z)(o,s.SENSOR,"Sensor"),(0,u.Z)(o,s.MARKDOWN,"Markdown"),(0,u.Z)(o,s.TRANSFORMER,"Transformer"),o),S=[s.DATA_LOADER,s.TRANSFORMER,s.DATA_EXPORTER,s.SENSOR];i={},(0,u.Z)(i,s.DATA_EXPORTER,"DE"),(0,u.Z)(i,s.DATA_LOADER,"DL"),(0,u.Z)(i,s.SCRATCHPAD,"SP"),(0,u.Z)(i,s.SENSOR,"SR"),(0,u.Z)(i,s.MARKDOWN,"MD"),(0,u.Z)(i,s.TRANSFORMER,"TF")},87372:function(e,n,t){"use strict";var r,o,i,c,a,u,s,l,d=t(82394),f=t(26304),p=t(26653),h=t(38626),m=t(33591),b=t(23831),g=t(2005),x=t(31012),O=t(19711),v=t(49125),y=t(86673),S=t(28598),w=["children","condensed","inline","level","marketing","spacingBelow"];function _(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function A(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?_(Object(t),!0).forEach((function(n){(0,d.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):_(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var j=(0,h.css)([""," margin:0;"," "," "," "," "," "," "," "," "," "," "," "," ",""],O.IH,(function(e){return e.color&&"\n    color: ".concat(e.color,"\n  ")}),(function(e){return e.yellow&&"\n    color: ".concat((e.theme.accent||b.Z.accent).yellow,";\n  ")}),(function(e){return e.center&&"\n    text-align: center;\n  "}),(function(e){return!e.monospace&&0===Number(e.weightStyle)&&"\n    font-family: ".concat(g.iI,";\n  ")}),(function(e){return!e.monospace&&1===Number(e.weightStyle)&&"\n    font-family: ".concat(g.LX,";\n  ")}),(function(e){return!e.monospace&&2===Number(e.weightStyle)&&"\n    font-family: ".concat(g.LX,";\n  ")}),(function(e){return!e.monospace&&3===Number(e.weightStyle)&&"\n    font-family: ".concat(g.ry,";\n  ")}),(function(e){return!e.monospace&&4===Number(e.weightStyle)&&"\n    font-family: ".concat(g.YC,";\n  ")}),(function(e){return!e.monospace&&5===Number(e.weightStyle)&&"\n    font-family: ".concat(g.nF,";\n  ")}),(function(e){return!e.monospace&&(6===Number(e.weightStyle)||e.bold)&&"\n    font-family: ".concat(g.nF,";\n  ")}),(function(e){return!e.monospace&&7===Number(e.weightStyle)&&"\n    font-family: ".concat(g.nF,";\n  ")}),(function(e){return!e.monospace&&8===Number(e.weightStyle)&&"\n    font-family: ".concat(g.nF,";\n  ")}),(function(e){return e.lineHeightAuto&&"\n    line-height: normal !important;\n  "})),Z=h.default.div.withConfig({displayName:"Headline__HeadlineContainerStyle",componentId:"sc-12jzt2e-0"})(["",""],(function(e){return"\n    color: ".concat((e.theme.content||b.Z.content).active,";\n  ")})),R=h.default.h1.withConfig({displayName:"Headline__H1HeroStyle",componentId:"sc-12jzt2e-1"})([""," font-size:42px;line-height:56px;"," "," ",""],j,m.media.md(r||(r=(0,p.Z)(["\n    ","\n  "])),x.aQ),m.media.lg(o||(o=(0,p.Z)(["\n    ","\n  "])),x.aQ),m.media.xl(i||(i=(0,p.Z)(["\n    ","\n  "])),x.aQ)),C=h.default.h1.withConfig({displayName:"Headline__H1Style",componentId:"sc-12jzt2e-2"})([""," ",""],j,x.MJ),E=h.default.h1.withConfig({displayName:"Headline__H1MarketingStyle",componentId:"sc-12jzt2e-3"})([""," "," "," "," "," ",""],j,m.media.xs(c||(c=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*v.iI,7*v.iI),m.media.sm(a||(a=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*v.iI,7*v.iI),m.media.md(u||(u=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*v.iI,7*v.iI),m.media.lg(s||(s=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*v.iI,7*v.iI),m.media.xl(l||(l=(0,p.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*v.iI,7*v.iI)),N=h.default.h2.withConfig({displayName:"Headline__H2Style",componentId:"sc-12jzt2e-4"})([""," ",""],j,x.BL),k=h.default.h3.withConfig({displayName:"Headline__H3Style",componentId:"sc-12jzt2e-5"})([""," font-size:24px;line-height:32px;"],j),T=h.default.h4.withConfig({displayName:"Headline__H4Style",componentId:"sc-12jzt2e-6"})([""," font-size:20px;line-height:28px;"],j),P=h.default.h5.withConfig({displayName:"Headline__H5Style",componentId:"sc-12jzt2e-7"})([""," font-size:18px;line-height:26px;"],j),D=h.default.span.withConfig({displayName:"Headline__SpanStyle",componentId:"sc-12jzt2e-8"})([""," "," "," "," ",""],j,(function(e){return 1===e.level&&"\n    ".concat(x.MJ,"\n  ")}),(function(e){return 2===e.level&&"\n    ".concat(x.BL,"\n  ")}),(function(e){return 3===e.level&&"\n    font-size: 24px;\n    line-height: 32px;\n  "}),(function(e){return 4===e.level&&"\n    font-size: 20px;\n    line-height: 28px;\n  "})),I=function(e){var n,t=e.children,r=e.condensed,o=e.inline,i=e.level,c=e.marketing,a=e.spacingBelow,u=(0,f.Z)(e,w);o?n=D:0===Number(i)?n=R:1===Number(i)?n=c?E:C:2===Number(i)?n=N:3===Number(i)?n=k:4===Number(i)?n=T:5===Number(i)&&(n=P);var s=(0,S.jsxs)(n,A(A({},u),{},{level:i,children:[a&&(0,S.jsx)(y.Z,{mb:r?2:3,children:t}),!a&&t]}));return o?s:(0,S.jsx)(Z,{children:s})};I.defaultProps={level:3,weightStyle:6},n.Z=I},46983:function(e,n,t){"use strict";t.r(n),t.d(n,{default:function(){return L}});var r=t(77837),o=t(75582),i=t(38860),c=t.n(i),a=t(82684),u=t(83455),s=t(60328),l=t(47999),d=t(57722),f=t(67971),p=t(87372),h=t(11135),m=t(86673),b=t(87815),g=t(19711),x=t(82944),O=t(70902),v=t(82531),y=t(10503),S=t(86422),w=t(73899),_=t(99994),A=t(85307),j=t(49125),Z=t(96510),R=t(90211),C=t(28598);var E=function(e){var n=e.clusterType,t=e.fetchWorkspaces,r=(0,a.useState)(),i=r[0],c=r[1],s=(0,a.useState)(),l=s[0],E=s[1],N=(0,a.useState)(),k=N[0],T=N[1],P=(0,a.useState)(null),D=P[0],I=P[1],H=(0,a.useState)(),M=H[0],L=H[1],W=(0,a.useState)(),z=W[0],F=W[1],U=(0,u.Db)(v.ZP.workspaces.useCreate(),{onSuccess:function(e){return(0,Z.wD)(e,{callback:function(e){e.error_message?E(e.error_message):(t(),c(!1))},onErrorCallback:function(e){var n=e.error,t=n.errors,r=n.message;E(r),console.log(t,r)}})}}),X=(0,o.Z)(U,2),B=X[0],K=X[1].isLoading,Y=[[(0,C.jsx)(g.ZP,{bold:!0,color:w.cM,children:"Workspace name"},"workspace_name_label"),(0,C.jsx)(x.Z,{label:"ecs"===n?"Spaces will be replaced by underscores":"Spaces will be replaced by hyphens",monospace:!0,onChange:function(e){e.preventDefault(),L(e.target.value)},placeholder:"Name your new workspace",value:M},"workspace_name_input")]];return"k8s"===n&&Y.push([(0,C.jsx)(g.ZP,{bold:!0,color:w.cM,children:"Service account name (optional)"},"service_account_name"),(0,C.jsx)(x.Z,{label:"Name of service account to be attached to stateful set",monospace:!0,onChange:function(e){e.preventDefault(),F(e.target.value)},placeholder:"Service account name",value:z},"service_account_name_label")]),(0,C.jsx)(C.Fragment,{children:i?(0,C.jsxs)(C.Fragment,{children:[(0,C.jsx)(p.Z,{default:!0,level:5,monospace:!0,children:"Configure your workspace"}),(0,C.jsx)(b.Z,{columnFlex:[null,3],rows:Y}),"k8s"===n&&(0,C.jsxs)(C.Fragment,{children:[(0,C.jsx)(m.Z,{mt:1,children:(0,C.jsxs)(f.Z,{alignItems:"center",children:[(0,C.jsx)(g.ZP,{default:!0,monospace:!0,children:"Configure container"}),(0,C.jsx)(m.Z,{ml:1}),(0,C.jsx)(O.Z,{checked:k,onCheck:function(){return T((function(e){return!e}))}})]})}),k&&(0,C.jsx)(m.Z,{mt:1,children:(0,C.jsx)(A.$W,{children:(0,C.jsx)(d.Z,{autoHeight:!0,language:S.t6.YAML,onChange:function(e){I(e)},tabSize:2,value:D||void 0,width:"100%"})})})]}),K&&(0,C.jsx)(m.Z,{mt:1,children:(0,C.jsx)(g.ZP,{small:!0,warning:!0,children:"This may take up to a few minutes... Once the service is created, it may take another 5-10 minutes for the service to be accessible."})}),!K&&l&&(0,C.jsxs)(C.Fragment,{children:[(0,C.jsx)(m.Z,{mt:1,children:(0,C.jsx)(g.ZP,{danger:!0,small:!0,children:"Failed to create instance, see error below."})}),(0,C.jsx)(m.Z,{mt:1,children:(0,C.jsx)(g.ZP,{danger:!0,small:!0,children:l})})]}),(0,C.jsx)(m.Z,{my:2,children:(0,C.jsxs)(f.Z,{children:[(0,C.jsx)(h.ZP,{background:w.a$,bold:!0,inline:!0,loading:K,onClick:function(){return B({workspace:{cluster_type:n,container_config:k&&D,name:(e=M,"ecs"===n?(0,R.We)(e,"_"):(0,R.We)(e,"-")),service_account_name:z}});var e},uuid:"workspaces/create",children:"Create"}),(0,C.jsx)(m.Z,{ml:1}),(0,C.jsx)(h.ZP,{bold:!0,inline:!0,onClick:function(){return c(!1)},uuid:"workspaces/cancel",children:"Cancel"})]})})]}):(0,C.jsx)(h.ZP,{background:_.eW,beforeElement:(0,C.jsx)(y.mm,{size:2.5*j.iI}),bold:!0,inline:!0,onClick:function(){L((0,R.Y6)()),c(!0)},uuid:"workspaces/new",children:"Create new workspace"})})},N=t(62084),k=t(41788),T=t(3849),P=t(73942),D=t(65597),I=t(84392);function H(e){var n=e.fetchWorkspaces,t=e.instance,r=e.clusterType,i=(0,a.useRef)(null),c=(0,a.useState)(),d=c[0],p=c[1],h=(0,a.useState)(),b=h[0],x=h[1],O=t.name,S=(t.task_arn,{cluster_type:r}),w=(0,u.Db)(v.ZP.workspaces.useUpdate(O,S),{onSuccess:function(e){return(0,Z.wD)(e,{callback:function(){n(),p(!1)},onErrorCallback:function(e){var n=e.error,t=n.errors,r=n.message;console.log(t,r)}})}}),_=(0,o.Z)(w,1)[0],A=(0,u.Db)(v.ZP.workspaces.useDelete(O,S),{onSuccess:function(e){return(0,Z.wD)(e,{callback:function(){n(),p(!1)},onErrorCallback:function(e){var n=e.error,t=n.errors,r=n.message;console.log(t,r)}})}}),R=(0,o.Z)(A,1)[0],E=(0,a.useMemo)((function(){var e=t.status,n=[{label:function(){return(0,C.jsx)(g.ZP,{children:"Delete workspace"})},onClick:function(){return x(!0)},uuid:"delete_workspace"}];return"STOPPED"===e?n.unshift({label:function(){return(0,C.jsx)(g.ZP,{children:"Resume instance"})},onClick:function(){return _({workspace:{action:"resume",cluster_type:r,name:t.name,task_arn:t.task_arn}})},uuid:"resume_instance"}):"RUNNING"===e&&n.unshift({label:function(){return(0,C.jsx)(g.ZP,{children:"Stop instance"})},onClick:function(){return _({workspace:{action:"stop",cluster_type:r,name:t.name,task_arn:t.task_arn}})},uuid:"stop_instance"}),n}),[r,t,_]);return(0,C.jsx)(C.Fragment,{children:"ecs"===r&&(0,C.jsxs)("div",{ref:i,style:{position:"relative",zIndex:"1"},children:[(0,C.jsx)(s.Z,{iconOnly:!0,onClick:function(){return p(!d)},children:(0,C.jsx)(y.mH,{size:2*j.iI})}),(0,C.jsx)(l.Z,{disableEscape:!0,onClickOutside:function(){p(!1),x(!1)},open:d,children:b?(0,C.jsxs)(D.f,{leftOffset:30*-j.iI,topOffset:3*-j.iI,width:30*j.iI,children:[(0,C.jsx)(g.ZP,{children:"Are you sure you want to delete"}),(0,C.jsx)(g.ZP,{children:"this instance? You may not be"}),(0,C.jsx)(g.ZP,{children:"able to recover your data."}),(0,C.jsx)(m.Z,{mt:1}),(0,C.jsxs)(f.Z,{children:[(0,C.jsx)(s.Z,{danger:!0,onClick:R,children:"Confirm"}),(0,C.jsx)(m.Z,{ml:1}),(0,C.jsx)(s.Z,{default:!0,onClick:function(){return x(!1)},children:"Cancel"})]})]}):(0,C.jsx)(N.Z,{items:E,left:25*-j.iI,open:d,parentRef:i,topOffset:3*-j.iI,uuid:"workspaces/more_actions",width:25*j.iI})})]})})}function M(){var e=v.ZP.statuses.list().data,n=(0,a.useMemo)((function(){var n,t;return(null===e||void 0===e||null===(n=e.statuses)||void 0===n||null===(t=n[0])||void 0===t?void 0:t.instance_type)||"ecs"}),[e]),t=v.ZP.workspaces.list({cluster_type:n},{refreshInterval:5e3,revalidateOnFocus:!0}),r=t.data,o=t.mutate,i=(0,a.useMemo)((function(){var e;return null===r||void 0===r||null===(e=r.workspaces)||void 0===e?void 0:e.filter((function(e){return e.name}))}),[r]);return(0,C.jsx)(T.Z,{breadcrumbs:[{bold:!0,label:function(){return"Workspaces"}}],pageName:I.L6.WORKSPACES,subheaderChildren:(0,C.jsx)(E,{clusterType:n,fetchWorkspaces:o}),children:(0,C.jsx)(b.Z,{columnFlex:[2,4,2,3,1,null],columns:[{uuid:"Status"},{uuid:"Instance Name"},{uuid:"Type"},{uuid:"Public IP address"},{uuid:"Open"},{label:function(){return""},uuid:"Actions"}],rows:null===i||void 0===i?void 0:i.map((function(e){var t=e.instance,r=t.ip,i=t.name,c=t.status,a=t.type,u="http://".concat(r);return"ecs"===n&&(u="http://".concat(r,":6789")),[(0,C.jsx)(s.Z,{borderRadius:P.D7,danger:"STOPPED"===c,default:"PROVISIONING"===c,notClickable:!0,padding:"6px",primary:"RUNNING"===c,warning:"PENDING"===c,children:(0,R.vg)(c)},"status"),(0,C.jsx)(g.ZP,{children:i},"name"),(0,C.jsx)(g.ZP,{children:(0,R.vg)(a)},"type"),(0,C.jsx)(g.ZP,{children:r},"ip"),(0,C.jsx)(s.Z,{iconOnly:!0,onClick:function(){return window.open(u)},children:(0,C.jsx)(y.M0,{size:2*j.iI})},"open_button"),(0,C.jsx)(H,{clusterType:n,fetchWorkspaces:o,instance:t},"more_actions")]}))})})}M.getInitialProps=(0,r.Z)(c().mark((function e(){return c().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",{});case 1:case"end":return e.stop()}}),e)})));var L=(0,k.Z)(M)},13157:function(e,n,t){(window.__NEXT_P=window.__NEXT_P||[]).push(["/manage",function(){return t(46983)}])}},function(e){e.O(0,[844,7607,8789,1424,1005,7815,7722,9774,2888,179],(function(){return n=13157,e(e.s=n);var n}));var n=e.O();_N_E=n}]);