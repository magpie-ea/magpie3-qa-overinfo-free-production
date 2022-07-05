(function(e){function t(t){for(var o,i,s=t[0],m=t[1],h=t[2],d=0,c=[];d<s.length;d++)i=s[d],Object.prototype.hasOwnProperty.call(r,i)&&r[i]&&c.push(r[i][0]),r[i]=0;for(o in m)Object.prototype.hasOwnProperty.call(m,o)&&(e[o]=m[o]);l&&l(t);while(c.length)c.shift()();return n.push.apply(n,h||[]),a()}function a(){for(var e,t=0;t<n.length;t++){for(var a=n[t],o=!0,i=1;i<a.length;i++){var m=a[i];0!==r[m]&&(o=!1)}o&&(n.splice(t--,1),e=s(s.s=a[0]))}return e}var o={},r={app:0},n=[];function i(e){return s.p+"js/"+({}[e]||e)+"."+{"chunk-1335a3e6":"5435e097"}[e]+".js"}function s(t){if(o[t])return o[t].exports;var a=o[t]={i:t,l:!1,exports:{}};return e[t].call(a.exports,a,a.exports,s),a.l=!0,a.exports}s.e=function(e){var t=[],a=r[e];if(0!==a)if(a)t.push(a[2]);else{var o=new Promise((function(t,o){a=r[e]=[t,o]}));t.push(a[2]=o);var n,m=document.createElement("script");m.charset="utf-8",m.timeout=120,s.nc&&m.setAttribute("nonce",s.nc),m.src=i(e);var h=new Error;n=function(t){m.onerror=m.onload=null,clearTimeout(d);var a=r[e];if(0!==a){if(a){var o=t&&("load"===t.type?"missing":t.type),n=t&&t.target&&t.target.src;h.message="Loading chunk "+e+" failed.\n("+o+": "+n+")",h.name="ChunkLoadError",h.type=o,h.request=n,a[1](h)}r[e]=void 0}};var d=setTimeout((function(){n({type:"timeout",target:m})}),12e4);m.onerror=m.onload=n,document.head.appendChild(m)}return Promise.all(t)},s.m=e,s.c=o,s.d=function(e,t,a){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:a})},s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var a=Object.create(null);if(s.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)s.d(a,o,function(t){return e[t]}.bind(null,o));return a},s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/magpie3-qa-overinfo-free-production/",s.oe=function(e){throw console.error(e),e};var m=window["webpackJsonp"]=window["webpackJsonp"]||[],h=m.push.bind(m);m.push=t,m=m.slice();for(var d=0;d<m.length;d++)t(m[d]);var l=h;n.push([0,"chunk-vendors"]),a()})({0:function(e,t,a){e.exports=a("56d7")},1:function(e,t){},2:function(e,t){},"56d7":function(e,t,a){"use strict";a.r(t);var o=a("2b0e"),r=a("7591"),n=a.n(r),i=a("3665"),s=function(){var e=this,t=e._self._c;return t("Experiment",{attrs:{title:"magpie demo"}},[t("InstructionScreen",{attrs:{title:"Welcome"}},[e._v(" This is a sample introduction screen. ")]),e._l(e.trials,(function(a,o){return[t("Screen",[t("Slide",[e._l(a.vignette.split("\\n"),(function(a,o){return t("span",{key:o},[e._v(" "+e._s(a)),t("br")])})),t("TextareaInput",{attrs:{response:e.$magpie.measurements.answer},on:{"update:response":function(t){return e.$set(e.$magpie.measurements,"answer",t)}}}),e.$magpie.measurements.answer&&e.$magpie.measurements.answer.length>2?t("button",{on:{click:function(t){return e.$magpie.saveAndNextScreen()}}},[e._v(" Submit ")]):e._e()],2)],1)]})),t("SubmitResultsScreen")],2)},m=[],h=a("2ef0"),d=a.n(h),l=a("b429"),c=a.n(l),u={name:"App",data(){return{trials:c.a}},computed:{_(){return d.a}}},y=u,f=a("2877"),p=Object(f["a"])(y,s,m,!1,null,null,null),v=p.exports,g={experimentId:"9",serverUrl:"https://magpie-refactored-2.herokuapp.com/",socketUrl:"wss://magpie-refactored-2.herokuapp.com/socket",completionUrl:"https://...",contactEmail:"test@random.com",mode:"debug",language:"en"};o["default"].config.productionTip=!1,o["default"].use(n.a,{prefix:"Canvas"}),o["default"].use(i["a"],g),new o["default"]({render:e=>e(v)}).$mount("#app")},b429:function(e,t){e.exports=[{itemName:"cafe-pie",settingName:"cafe",vignette:'You are a server in a café. Today the café has raspberry pie, pasta al forno, lemon cake, chocolate cookies and cheese sandwich.\\n\\nA customer asks: "Do you have raspberry cake?"\\n\\nYou reply:',taciturn:"\"I'm sorry, we don't have raspberry cake today.",competitor:"\"I'm sorry, we don't have raspberry cake today. We have raspberry pie.\"",sameCategory:"\"I'm sorry, we don't have raspberry cake today. We have raspberry pie, lemon cake, and chocolate cookies.\"",otherCategory:"\"I'm sorry, we don't have raspberry cake today. We have pasta al forno and cheese sandwich.\"",fullList:"\"I'm sorry, we don't have raspberry cake today. We have raspberry pie, pasta al forno, lemon cake, chocolate cookies, and cheese sandwich.\"",itemQuestion:"raspberry cake",itemCompetitor:"raspberry pie",itemSameCat1:"lemon cake",itemSameCat2:"chocolate cookies",itemOtherCat1:"pasta al forno",itemOtherCat2:"cheese sandwich"},{itemName:"cafe-pasta",settingName:"cafe",vignette:'You are a server in a café. Today the café has pasta al forno, pizza, lemon cake, chocolate cookies and lasagne.\\n\\nA customer asks: "Do you have pasta arrabiata?"\\n\\nYou reply:',taciturn:"\"I'm sorry, we don't have pasta arrabiata today.\"",competitor:"\"I'm sorry, we don't have pasta arrabiata today. We have pasta al forno.\"",sameCategory:"\"I'm sorry, we don't have pasta arrabiata today. We have pasta al forno, pizza, and lasange.\"",otherCategory:"\"I'm sorry, we don't have pasta arrabiata today. We have lemon cake and chocolate cookies.\"",fullList:"\"I'm sorry, we don't have pasta arrabiata today. We have pasta al forno, pizza, lemon cake, chocolate cookies, and lasagne.\"",itemQuestion:"pasta arrabiata",itemCompetitor:"pasta al forno",itemSameCat1:"pizza",itemSameCat2:"lasagna",itemOtherCat1:"lemon cake",itemOtherCat2:"chocolate cookies"},{itemName:"bar-whiteWine",settingName:"bar",vignette:'You are a bar tender in a hotel bar. The bar serves only whiskey, beer, red wine, soft drinks and coffee today.\\n\\nLate at night a woman walks in. She looks gloomy. She says: "Do you have white wine?"\\n\\nYou reply:',taciturn:"\"I'm sorry, we don't have white wine today.\"",competitor:"\"I'm sorry, we don't have white wine today.\"",sameCategory:"\"I'm sorry, we don't have white wine today. We have whiskey, beer, and red wine.\"",otherCategory:"\"I'm sorry, we don't have white wine today. We have soft drinks and coffee.\"",fullList:"\"I'm sorry, we don't have white wine today. We have whiskey, beer, red wine, soft drinks, and coffee.\"",itemQuestion:"white wine",itemCompetitor:"red wine",itemSameCat1:"whiskey",itemSameCat2:"beer",itemOtherCat1:"soft drinks",itemOtherCat2:"coffee"},{itemName:"bar-coffee",settingName:"bar",vignette:'You are a bar tender in a hotel bar. The bar serves only coffee, beer, red wine, soft drinks and soda today.\\n\\nLate at night a woman walks in. She looks gloomy. She says: "Do you have tea?"\\n\\nYou reply:',taciturn:"\"I'm sorry, we don't have tea today.\"",competitor:"\"I'm sorry, we don't have tea today. We have coffee.\"",sameCategory:"\"I'm sorry, we don't have tea today. We have coffee, soft drinks, and soda.\"",otherCategory:"\"I'm sorry, we don't have tea today. We have beer and red wine.\"",fullList:"\"I'm sorry, we don't have tea today. We have coffee, beer, red wine, soft drinks, and soda.\"",itemQuestion:"tea",itemCompetitor:"coffee",itemSameCat1:"soft drinks",itemSameCat2:"soda",itemOtherCat1:"beer",itemOtherCat2:"red wine"},{itemName:"airport-europe",settingName:"airport",vignette:'You are a customer service agent helping book flights. Today there is a morning flight to Berlin, an afternoon flight to Madrid, an evening flight to Paris, and several flights to the US.\\n\\nA customer asks: "Do you have a morning flight to Madrid?"\\n\\nYou reply:',taciturn:"\"I'm sorry, we don't have a morning flight to Madrid today.\"",competitor:"\"I'm sorry, we don't have a morning flight to Madrid today, but we have one in the afternoon.\"",sameCategory:'""I\'m sorry, we don\'t have a morning flight to Madrid today. We have a morning flight to Berlin, an afternoon flight to Madrid, and an evening flight to Paris."',otherCategory:'""I\'m sorry, we don\'t have a morning flight to Madrid today, but we have several flights to the US."',fullList:'""I\'m sorry, we don\'t have a morning flight to Madrid today, but we have a morning flight to Berlin, an afternoon flight to Madrid, an evening flight to Paris, and several flights to the US."',itemQuestion:"madrid morning",itemCompetitor:"madrid afternoon",itemSameCat1:"berlin morning",itemSameCat2:"paris evening",itemOtherCat1:"united states 1",itemOtherCat2:"united states 2"},{itemName:"airport-usa",settingName:"airport",vignette:'You are a customer service agent helping book flights. Today there is an afternoon flight to San Francisco, a morning flight to Boston, an evening flight to Los Angeles, and several flights to Europe.\\n\\nA customer asks: "Do you have an afternoon flight to Boston?"\\n\\nYou reply:',taciturn:"\"I'm sorry, we don't have an afternoon flight to Boston today.\"",competitor:"\"I'm sorry, we don't have an afternoon flight to Boston today, but we have a morning flight to Boston.\"",sameCategory:"\"I'm sorry, we don't have an afternoon flight to Boston today, but we have an afternoon flight to San Francisco, a morning flight to Boston, and an evening flight to Los Angeles.\"",otherCategory:"\"I'm sorry, we don't have an afternoon flight to Boston today, but we have several flights to Europe.\"",fullList:"\"I'm sorry, we don't have an afternoon flight to Boston today, but we have an afternoon flight to San Francisco, a morning flight to Boston, an evening flight to Los Angeles, and several flights to Europe.\"",itemQuestion:"boston afternoon",itemCompetitor:"boston morning",itemSameCat1:"san francisco afternoon",itemSameCat2:"los angeles evening",itemOtherCat1:"europe 1",itemOtherCat2:"europe 2"},{itemName:"movie-cartoon",settingName:"movie",vignette:'You work at the ticket counter of a small movie theatre. The films on show today are a horror movie, a musical, an animation film, a comedy, and a thriller. \\n\\nA customer asks: "Do you show a cartoon today?"\\n\\nYou reply:',taciturn:"\"I'm sorry, we don't show a cartoon today.\"",competitor:"\"I'm sorry, we don't show a cartoon today, but there is an animation film.\"",sameCategory:"\"I'm sorry, we don't show a cartoon today, but there is a musical, an animation film, and a comedy.\"",otherCategory:"\"I'm sorry, we don't show a cartoon today, but there is a horror movie and a thriller.\"",fullList:"\"I'm sorry, we don't show a cartoon today, but there is a horror movie, a musical, an animation film, a comedy, and a thriller.\"",itemQuestion:"cartoon",itemCompetitor:"animation film",itemSameCat1:"comedy",itemSameCat2:"musical",itemOtherCat1:"horror movie",itemOtherCat2:"thriller"},{itemName:"movie-fantasy",settingName:"movie",vignette:'You work at the ticket counter of a small movie theatre. The films on show today are a film noir, a science fiction movie, an animation film, an adventure movie, and a cartoon. \\n\\nA customer asks: "Do you show a fantasy movie today?"\\n\\nYou reply:',taciturn:"\"I'm sorry, we don't show a fantasy movie today.\"",competitor:"\"I'm sorry, we don't show a fantasy movie today, but there is a science fiction movie.\"",sameCategory:"\"I'm sorry, we don't show a fantasy movie today, but there is a film noir, a science fiction movie, and an adventure movie.\"",otherCategory:"\"I'm sorry, we don't show a fantasy movie today, but there is an animation film and a cartoon.\"",fullList:"\"I'm sorry, we don't show a fantasy movie today, but there is a film noir, a science fiction movie, an animation film, an adventure movie, and a cartoon.\"",itemQuestion:"fantasy movie",itemCompetitor:"science fiction movie",itemSameCat1:"adventure movie",itemSameCat2:"film noir",itemOtherCat1:"cartoon",itemOtherCat2:"animation film"},{itemName:"music-hardrock",settingName:"music",vignette:'You are driving in a car with your neighbor. The car only has an old CD player. You have the following styles of music: heavy metal, bebop, classic rock, power metal, and dixieland.\\n\\nYour neighbor asks: "Do you have any hard rock?"\\n\\nYou reply:',taciturn:"\"I'm sorry, I don't have any hard rock.\"",competitor:"\"I'm sorry, I don't have any hard rock, but I have some classic rock.\"",sameCategory:"\"I'm sorry, I don't have any hard rock, but I have some heavy metal, classic rock, and power metal.\"",otherCategory:"\"I'm sorry, I don't have any hard rock, but I have some bebop and dixieland.\"",fullList:"\"I'm sorry, I don't have any hard rock, but I have some heavy metal, bebop, classic rock, power metal, and dixieland.\"",itemQuestion:"hard rock",itemCompetitor:"classic rock",itemSameCat1:"heavy metal",itemSameCat2:"power metal",itemOtherCat1:"bebop",itemOtherCat2:"dixieland"},{itemName:"music-bebop",settingName:"music",vignette:'You are driving in a car with your neighbor. The car only has an old CD player. You have the following styles of music: cool jazz, death metal, hard bop, soul jazz, and doom metal.\\n\\nYour neighbor asks: "Do you have any bebop?"\\n\\nYou reply:',taciturn:"\"I'm sorry, I don't have any bebop.\"",competitor:"\"I'm sorry, I don't have any bebop, but I have some hard bop.\"",sameCategory:"\"I'm sorry, I don't have any bebop, but I have some cool jazz, hard bop, and soul jazz.\"",otherCategory:"\"I'm sorry, I don't have any bebop, but I have some death metal and doom metal.\"",fullList:"\"I'm sorry, I don't have any bebop, but I have some cool jazz, death metal, hard bop, soul jazz, and doom metal.\"",itemQuestion:"bebop",itemCompetitor:"hard bop",itemSameCat1:"cool jazz",itemSameCat2:"soul jazz",itemOtherCat1:"death metal",itemOtherCat2:"doom metal"}]}});
//# sourceMappingURL=app.9ebeda81.js.map