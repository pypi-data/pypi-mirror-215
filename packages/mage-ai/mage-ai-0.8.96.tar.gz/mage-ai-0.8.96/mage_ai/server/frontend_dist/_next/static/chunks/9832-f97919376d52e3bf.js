"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[9832],{52136:function(t,n,e){e.d(n,{Z:function(){return p}});var i=e(47329),r=e.n(i),o=e(82684),u=e(63588),c=e.n(u),l=e(5237),s=e(29989),a=e(81352),h=e(46119),f=e(88543),d=e(12765),y=["top","left","scale","height","stroke","strokeWidth","strokeDasharray","className","numTicks","lineStyle","offset","tickValues","children"];function _(){return _=Object.assign||function(t){for(var n=1;n<arguments.length;n++){var e=arguments[n];for(var i in e)Object.prototype.hasOwnProperty.call(e,i)&&(t[i]=e[i])}return t},_.apply(this,arguments)}function p(t){var n=t.top,e=void 0===n?0:n,i=t.left,r=void 0===i?0:i,u=t.scale,p=t.height,v=t.stroke,x=void 0===v?"#eaf0f6":v,m=t.strokeWidth,Z=void 0===m?1:m,g=t.strokeDasharray,b=t.className,O=t.numTicks,E=void 0===O?10:O,k=t.lineStyle,w=t.offset,T=t.tickValues,N=t.children,j=function(t,n){if(null==t)return{};var e,i,r={},o=Object.keys(t);for(i=0;i<o.length;i++)e=o[i],n.indexOf(e)>=0||(r[e]=t[e]);return r}(t,y),M=null!=T?T:(0,h.Z)(u,E),P=(null!=w?w:0)+(0,d.Z)(u)/2,R=M.map((function(t,n){var e,i=(null!=(e=(0,f.Z)(u(t)))?e:0)+P;return{index:n,from:new a.Z({x:i,y:0}),to:new a.Z({x:i,y:p})}}));return o.createElement(s.Z,{className:c()("visx-columns",b),top:e,left:r},N?N({lines:R}):R.map((function(t){var n=t.from,e=t.to,i=t.index;return o.createElement(l.Z,_({key:"column-line-"+i,from:n,to:e,stroke:x,strokeWidth:Z,strokeDasharray:g,style:k},j))})))}p.propTypes={tickValues:r().array,height:r().number.isRequired}},85587:function(t,n,e){e.d(n,{Z:function(){return s}});var i=e(82684),r=e(63588),o=e.n(r),u=e(39309),c=["children","data","x","y","fill","className","curve","innerRef","defined"];function l(){return l=Object.assign||function(t){for(var n=1;n<arguments.length;n++){var e=arguments[n];for(var i in e)Object.prototype.hasOwnProperty.call(e,i)&&(t[i]=e[i])}return t},l.apply(this,arguments)}function s(t){var n=t.children,e=t.data,r=void 0===e?[]:e,s=t.x,a=t.y,h=t.fill,f=void 0===h?"transparent":h,d=t.className,y=t.curve,_=t.innerRef,p=t.defined,v=void 0===p?function(){return!0}:p,x=function(t,n){if(null==t)return{};var e,i,r={},o=Object.keys(t);for(i=0;i<o.length;i++)e=o[i],n.indexOf(e)>=0||(r[e]=t[e]);return r}(t,c),m=(0,u.jv)({x:s,y:a,defined:v,curve:y});return n?i.createElement(i.Fragment,null,n({path:m})):i.createElement("path",l({ref:_,className:o()("visx-linepath",d),d:m(r)||"",fill:f,strokeLinecap:"round"},x))}},39309:function(t,n,e){e.d(n,{SO:function(){return u},jv:function(){return c}});var i=e(48167),r=e(92201),o=e(13004);function u(t){var n=void 0===t?{}:t,e=n.x,r=n.x0,u=n.x1,c=n.y,l=n.y0,s=n.y1,a=n.defined,h=n.curve,f=(0,i.Z)();return e&&(0,o.Z)(f.x,e),r&&(0,o.Z)(f.x0,r),u&&(0,o.Z)(f.x1,u),c&&(0,o.Z)(f.y,c),l&&(0,o.Z)(f.y0,l),s&&(0,o.Z)(f.y1,s),a&&f.defined(a),h&&f.curve(h),f}function c(t){var n=void 0===t?{}:t,e=n.x,i=n.y,u=n.defined,c=n.curve,l=(0,r.Z)();return e&&(0,o.Z)(l.x,e),i&&(0,o.Z)(l.y,i),u&&l.defined(u),c&&l.curve(c),l}},98889:function(t,n,e){e.d(n,{Z:function(){return p}});var i=e(47329),r=e.n(i),o=e(82684),u=e(63588),c=e.n(u),l=e(39309),s=["children","x","x0","x1","y","y0","y1","data","defined","className","curve","innerRef"];function a(){return a=Object.assign||function(t){for(var n=1;n<arguments.length;n++){var e=arguments[n];for(var i in e)Object.prototype.hasOwnProperty.call(e,i)&&(t[i]=e[i])}return t},a.apply(this,arguments)}function h(t){var n=t.children,e=t.x,i=t.x0,r=t.x1,u=t.y,h=t.y0,f=t.y1,d=t.data,y=void 0===d?[]:d,_=t.defined,p=void 0===_?function(){return!0}:_,v=t.className,x=t.curve,m=t.innerRef,Z=function(t,n){if(null==t)return{};var e,i,r={},o=Object.keys(t);for(i=0;i<o.length;i++)e=o[i],n.indexOf(e)>=0||(r[e]=t[e]);return r}(t,s),g=(0,l.SO)({x:e,x0:i,x1:r,y:u,y0:h,y1:f,defined:p,curve:x});return n?o.createElement(o.Fragment,null,n({path:g})):o.createElement("path",a({ref:m,className:c()("visx-area",v),d:g(y)||""},Z))}var f=["id","children"];function d(){return d=Object.assign||function(t){for(var n=1;n<arguments.length;n++){var e=arguments[n];for(var i in e)Object.prototype.hasOwnProperty.call(e,i)&&(t[i]=e[i])}return t},d.apply(this,arguments)}function y(t){var n=t.id,e=t.children,i=function(t,n){if(null==t)return{};var e,i,r={},o=Object.keys(t);for(i=0;i<o.length;i++)e=o[i],n.indexOf(e)>=0||(r[e]=t[e]);return r}(t,f);return o.createElement("defs",null,o.createElement("clipPath",d({id:n},i),e))}function _(){return _=Object.assign||function(t){for(var n=1;n<arguments.length;n++){var e=arguments[n];for(var i in e)Object.prototype.hasOwnProperty.call(e,i)&&(t[i]=e[i])}return t},_.apply(this,arguments)}function p(t){var n=t.className,e=t.curve,i=t.clipAboveTo,r=t.clipBelowTo,u=t.data,l=t.defined,s=t.x,a=t.y0,f=t.y1,d=t.aboveAreaProps,p=t.belowAreaProps,v=t.id,x=void 0===v?"":v;return o.createElement("g",{className:c()("visx-threshold",n)},o.createElement(h,{curve:e,data:u,x:s,y1:f,defined:l},(function(t){var n=t.path,e=null,c=null;return e=n.y0(r)(u),c=n.y0(i)(u),o.createElement("g",null,o.createElement(y,{id:"threshold-clip-below-"+x},o.createElement("path",{d:e||""})),o.createElement(y,{id:"threshold-clip-above-"+x},o.createElement("path",{d:c||""})))})),o.createElement(h,_({curve:e,data:u,defined:l,x:s,y0:a,y1:f,strokeWidth:0,clipPath:"url(#threshold-clip-below-"+x+")"},p)),o.createElement(h,_({curve:e,data:u,defined:l,x:s,y0:a,y1:f,strokeWidth:0,clipPath:"url(#threshold-clip-above-"+x+")"},d)))}y.propTypes={id:r().string.isRequired,children:r().node},p.propTypes={className:r().string,clipAboveTo:r().oneOfType([r().func,r().number]).isRequired,clipBelowTo:r().oneOfType([r().func,r().number]).isRequired,id:r().string.isRequired,data:r().array.isRequired,defined:r().func,x:r().oneOfType([r().func,r().number]).isRequired,y0:r().oneOfType([r().func,r().number]).isRequired,y1:r().oneOfType([r().func,r().number]).isRequired}},61655:function(t,n,e){e.d(n,{Z:function(){return u}});var i=e(82684),r=e(29179);function o(){return o=Object.assign||function(t){for(var n=1;n<arguments.length;n++){var e=arguments[n];for(var i in e)Object.prototype.hasOwnProperty.call(e,i)&&(t[i]=e[i])}return t},o.apply(this,arguments)}function u(t,n,e){void 0===n&&(n={style:{position:"relative",width:"inherit",height:"inherit"}}),void 0===e&&(e=function(t,n){return i.createElement("div",n,t)});return function(u){var c=(0,r.Z)();return e(i.createElement(t,o({},c,u)),n)}}},35681:function(t,n){var e=Math.PI,i=2*e,r=1e-6,o=i-r;function u(){this._x0=this._y0=this._x1=this._y1=null,this._=""}function c(){return new u}u.prototype=c.prototype={constructor:u,moveTo:function(t,n){this._+="M"+(this._x0=this._x1=+t)+","+(this._y0=this._y1=+n)},closePath:function(){null!==this._x1&&(this._x1=this._x0,this._y1=this._y0,this._+="Z")},lineTo:function(t,n){this._+="L"+(this._x1=+t)+","+(this._y1=+n)},quadraticCurveTo:function(t,n,e,i){this._+="Q"+ +t+","+ +n+","+(this._x1=+e)+","+(this._y1=+i)},bezierCurveTo:function(t,n,e,i,r,o){this._+="C"+ +t+","+ +n+","+ +e+","+ +i+","+(this._x1=+r)+","+(this._y1=+o)},arcTo:function(t,n,i,o,u){t=+t,n=+n,i=+i,o=+o,u=+u;var c=this._x1,l=this._y1,s=i-t,a=o-n,h=c-t,f=l-n,d=h*h+f*f;if(u<0)throw new Error("negative radius: "+u);if(null===this._x1)this._+="M"+(this._x1=t)+","+(this._y1=n);else if(d>r)if(Math.abs(f*s-a*h)>r&&u){var y=i-c,_=o-l,p=s*s+a*a,v=y*y+_*_,x=Math.sqrt(p),m=Math.sqrt(d),Z=u*Math.tan((e-Math.acos((p+d-v)/(2*x*m)))/2),g=Z/m,b=Z/x;Math.abs(g-1)>r&&(this._+="L"+(t+g*h)+","+(n+g*f)),this._+="A"+u+","+u+",0,0,"+ +(f*y>h*_)+","+(this._x1=t+b*s)+","+(this._y1=n+b*a)}else this._+="L"+(this._x1=t)+","+(this._y1=n);else;},arc:function(t,n,u,c,l,s){t=+t,n=+n,s=!!s;var a=(u=+u)*Math.cos(c),h=u*Math.sin(c),f=t+a,d=n+h,y=1^s,_=s?c-l:l-c;if(u<0)throw new Error("negative radius: "+u);null===this._x1?this._+="M"+f+","+d:(Math.abs(this._x1-f)>r||Math.abs(this._y1-d)>r)&&(this._+="L"+f+","+d),u&&(_<0&&(_=_%i+i),_>o?this._+="A"+u+","+u+",0,1,"+y+","+(t-a)+","+(n-h)+"A"+u+","+u+",0,1,"+y+","+(this._x1=f)+","+(this._y1=d):_>r&&(this._+="A"+u+","+u+",0,"+ +(_>=e)+","+y+","+(this._x1=t+u*Math.cos(l))+","+(this._y1=n+u*Math.sin(l))))},rect:function(t,n,e,i){this._+="M"+(this._x0=this._x1=+t)+","+(this._y0=this._y1=+n)+"h"+ +e+"v"+ +i+"h"+-e+"Z"},toString:function(){return this._}},n.Z=c},48167:function(t,n,e){e.d(n,{Z:function(){return l}});var i=e(35681),r=e(90875),o=e(23622),u=e(92201),c=e(98930);function l(){var t=c.x,n=null,e=(0,r.Z)(0),l=c.y,s=(0,r.Z)(!0),a=null,h=o.Z,f=null;function d(r){var o,u,c,d,y,_=r.length,p=!1,v=new Array(_),x=new Array(_);for(null==a&&(f=h(y=(0,i.Z)())),o=0;o<=_;++o){if(!(o<_&&s(d=r[o],o,r))===p)if(p=!p)u=o,f.areaStart(),f.lineStart();else{for(f.lineEnd(),f.lineStart(),c=o-1;c>=u;--c)f.point(v[c],x[c]);f.lineEnd(),f.areaEnd()}p&&(v[o]=+t(d,o,r),x[o]=+e(d,o,r),f.point(n?+n(d,o,r):v[o],l?+l(d,o,r):x[o]))}if(y)return f=null,y+""||null}function y(){return(0,u.Z)().defined(s).curve(h).context(a)}return d.x=function(e){return arguments.length?(t="function"===typeof e?e:(0,r.Z)(+e),n=null,d):t},d.x0=function(n){return arguments.length?(t="function"===typeof n?n:(0,r.Z)(+n),d):t},d.x1=function(t){return arguments.length?(n=null==t?null:"function"===typeof t?t:(0,r.Z)(+t),d):n},d.y=function(t){return arguments.length?(e="function"===typeof t?t:(0,r.Z)(+t),l=null,d):e},d.y0=function(t){return arguments.length?(e="function"===typeof t?t:(0,r.Z)(+t),d):e},d.y1=function(t){return arguments.length?(l=null==t?null:"function"===typeof t?t:(0,r.Z)(+t),d):l},d.lineX0=d.lineY0=function(){return y().x(t).y(e)},d.lineY1=function(){return y().x(t).y(l)},d.lineX1=function(){return y().x(n).y(e)},d.defined=function(t){return arguments.length?(s="function"===typeof t?t:(0,r.Z)(!!t),d):s},d.curve=function(t){return arguments.length?(h=t,null!=a&&(f=h(a)),d):h},d.context=function(t){return arguments.length?(null==t?a=f=null:f=h(a=t),d):a},d}},97745:function(t,n,e){function i(t,n,e){t._context.bezierCurveTo((2*t._x0+t._x1)/3,(2*t._y0+t._y1)/3,(t._x0+2*t._x1)/3,(t._y0+2*t._y1)/3,(t._x0+4*t._x1+n)/6,(t._y0+4*t._y1+e)/6)}function r(t){this._context=t}function o(t){return new r(t)}e.d(n,{ZP:function(){return o},fE:function(){return r},xm:function(){return i}}),r.prototype={areaStart:function(){this._line=0},areaEnd:function(){this._line=NaN},lineStart:function(){this._x0=this._x1=this._y0=this._y1=NaN,this._point=0},lineEnd:function(){switch(this._point){case 3:i(this,this._x1,this._y1);case 2:this._context.lineTo(this._x1,this._y1)}(this._line||0!==this._line&&1===this._point)&&this._context.closePath(),this._line=1-this._line},point:function(t,n){switch(t=+t,n=+n,this._point){case 0:this._point=1,this._line?this._context.lineTo(t,n):this._context.moveTo(t,n);break;case 1:this._point=2;break;case 2:this._point=3,this._context.lineTo((5*this._x0+this._x1)/6,(5*this._y0+this._y1)/6);default:i(this,t,n)}this._x0=this._x1,this._x1=t,this._y0=this._y1,this._y1=n}}},23622:function(t,n,e){function i(t){this._context=t}function r(t){return new i(t)}e.d(n,{Z:function(){return r}}),i.prototype={areaStart:function(){this._line=0},areaEnd:function(){this._line=NaN},lineStart:function(){this._point=0},lineEnd:function(){(this._line||0!==this._line&&1===this._point)&&this._context.closePath(),this._line=1-this._line},point:function(t,n){switch(t=+t,n=+n,this._point){case 0:this._point=1,this._line?this._context.lineTo(t,n):this._context.moveTo(t,n);break;case 1:this._point=2;default:this._context.lineTo(t,n)}}}},92201:function(t,n,e){e.d(n,{Z:function(){return c}});var i=e(35681),r=e(90875),o=e(23622),u=e(98930);function c(){var t=u.x,n=u.y,e=(0,r.Z)(!0),c=null,l=o.Z,s=null;function a(r){var o,u,a,h=r.length,f=!1;for(null==c&&(s=l(a=(0,i.Z)())),o=0;o<=h;++o)!(o<h&&e(u=r[o],o,r))===f&&((f=!f)?s.lineStart():s.lineEnd()),f&&s.point(+t(u,o,r),+n(u,o,r));if(a)return s=null,a+""||null}return a.x=function(n){return arguments.length?(t="function"===typeof n?n:(0,r.Z)(+n),a):t},a.y=function(t){return arguments.length?(n="function"===typeof t?t:(0,r.Z)(+t),a):n},a.defined=function(t){return arguments.length?(e="function"===typeof t?t:(0,r.Z)(!!t),a):e},a.curve=function(t){return arguments.length?(l=t,null!=c&&(s=l(c)),a):l},a.context=function(t){return arguments.length?(null==t?c=s=null:s=l(c=t),a):c},a}},98930:function(t,n,e){function i(t){return t[0]}function r(t){return t[1]}e.d(n,{x:function(){return i},y:function(){return r}})}}]);