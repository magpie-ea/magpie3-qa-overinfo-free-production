(function(e){function t(t){for(var a,r,s=t[0],c=t[1],l=t[2],u=0,p=[];u<s.length;u++)r=s[u],Object.prototype.hasOwnProperty.call(n,r)&&n[r]&&p.push(n[r][0]),n[r]=0;for(a in c)Object.prototype.hasOwnProperty.call(c,a)&&(e[a]=c[a]);m&&m(t);while(p.length)p.shift()();return i.push.apply(i,l||[]),o()}function o(){for(var e,t=0;t<i.length;t++){for(var o=i[t],a=!0,r=1;r<o.length;r++){var c=o[r];0!==n[c]&&(a=!1)}a&&(i.splice(t--,1),e=s(s.s=o[0]))}return e}var a={},n={app:0},i=[];function r(e){return s.p+"js/"+({}[e]||e)+"."+{"chunk-1335a3e6":"0a8a03ea"}[e]+".js"}function s(t){if(a[t])return a[t].exports;var o=a[t]={i:t,l:!1,exports:{}};return e[t].call(o.exports,o,o.exports,s),o.l=!0,o.exports}s.e=function(e){var t=[],o=n[e];if(0!==o)if(o)t.push(o[2]);else{var a=new Promise((function(t,a){o=n[e]=[t,a]}));t.push(o[2]=a);var i,c=document.createElement("script");c.charset="utf-8",c.timeout=120,s.nc&&c.setAttribute("nonce",s.nc),c.src=r(e);var l=new Error;i=function(t){c.onerror=c.onload=null,clearTimeout(u);var o=n[e];if(0!==o){if(o){var a=t&&("load"===t.type?"missing":t.type),i=t&&t.target&&t.target.src;l.message="Loading chunk "+e+" failed.\n("+a+": "+i+")",l.name="ChunkLoadError",l.type=a,l.request=i,o[1](l)}n[e]=void 0}};var u=setTimeout((function(){i({type:"timeout",target:c})}),12e4);c.onerror=c.onload=i,document.head.appendChild(c)}return Promise.all(t)},s.m=e,s.c=a,s.d=function(e,t,o){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:o})},s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var o=Object.create(null);if(s.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var a in e)s.d(o,a,function(t){return e[t]}.bind(null,a));return o},s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/magpie3-qa-overinfo-free-production/experiments/free_production/",s.oe=function(e){throw console.error(e),e};var c=window["webpackJsonp"]=window["webpackJsonp"]||[],l=c.push.bind(c);c.push=t,c=c.slice();for(var u=0;u<c.length;u++)t(c[u]);var m=l;i.push([0,"chunk-vendors"]),o()})({0:function(e,t,o){e.exports=o("56d7")},1:function(e,t){},"169d":function(e,t,o){},2:function(e,t){},"50ff":function(e,t){e.exports=[{itemName:"jobCenter-office",settingName:"jobCenter",vignette_start:"You are working at the job center consultation desk and help people find open vacancies. Please type ‘teacher’ in the text area. Currently the following positions are available at local businesses:",vignette_continuation:"\\n\\nA man walks in and asks:",priorElicitation_context:"Please move all sliders all the way to the left. Suppose someone wants to have",priorElicitation_question:"had",question:"Is there an open accountant job?",taciturn:"I'm sorry, there is no accountant job open.",answer_template:"There is *.",type:"filler",itemQuestion:"an accountant job",competitor:"a bookkeeper job",sameCategory:"a manager assistant job",otherCategory:"a car mechanic job",correct_response:"teacher"},{itemName:"jobCenter-engineer",settingName:"jobCenter",vignette_start:"You are working at the job center consultation desk and help people find open vacancies. Please type ‘teacher’ in the text area. Currently the following positions are available at local businesses:",vignette_continuation:"\\n\\nA man walks in and asks:",priorElicitation_context:"Please move all sliders all the way to the left. Suppose someone wants to have",priorElicitation_question:"had",question:"Is there an electrical mechanic job open?",taciturn:"I'm sorry, there is no electrical mechanic job open.",answer_template:"There is *.",type:"filler",itemQuestion:"an electrical mechanic job",competitor:"an electrician job",sameCategory:"a car mechanic job",otherCategory:"a secretary job",correct_response:"teacher"},{itemName:"art-painting",settingName:"art",vignette_start:"You work at an art shop. You are hosting an exhibition sale by a local artist. The artist has",vignette_continuation:"Please type ‘sculpture’ in the text area. \\n\\nA customer takes a look around and asks:",priorElicitation_context:"Please move all sliders all the way to the right. Suppose someone wants to have",priorElicitation_question:"got",question:"Are there any acrylic paintings for sale?",taciturn:"I’m sorry, there are no acrylic paintings.",answer_template:"There are *.",type:"filler",itemQuestion:"acrylic paintings",competitor:"gouache paintings",sameCategory:"oil paintings",otherCategory:"pencil drawings",correct_response:"sculpture"},{itemName:"art-drawing",settingName:"art",vignette_start:"You work at an art shop. You are hosting an exhibition sale by a local artist. The artist has",vignette_continuation:"Please type ‘sculpture’ in the text area. \\n\\nA customer takes a look around and asks:",priorElicitation_context:"Please move all sliders all the way to the right. Suppose someone wants to have",priorElicitation_question:"got",question:"Are there any ink drawings for sale?",taciturn:"I’m sorry, there are no ink drawings.",answer_template:"There are *.",type:"filler",itemQuestion:"ink drawings",competitor:"pencil drawings",sameCategory:"crayon drawings",otherCategory:"oil paintings",correct_response:"sculpture"},{itemName:"carRental-fun",settingName:"carRental",vignette_start:"You are working in a private car rental agency. Please type ‘motorcycle’ in the text area. For today, the following types of vehicles are still available on site:",vignette_continuation:"\\n\\nA young man walks in and asks:",priorElicitation_context:"Please move all sliders all the way to the left. Suppose someone wants to have",priorElicitation_question:"got",question:"Do you have a Porsche for rent today?",taciturn:"I'm sorry, we don’t have a Porsche on site today.",answer_template:"We have *.",type:"filler",itemQuestion:"a Porsche",competitor:"a Ferrari",sameCategory:"a BMW convertible",otherCategory:"a medium-sized delivery truck",correct_response:"motorcycle"},{itemName:"carRental-moving",settingName:"carRental",vignette_start:"You are working in a private car rental agency. Please type ‘motorcycle’ in the text area. For today, the following types of vehicles are still available on site:",vignette_continuation:"\\n\\nA young man walks in and asks:",priorElicitation_context:"Please move all sliders all the way to the left. Suppose someone wants to have",priorElicitation_question:"got",question:"Is a moving truck available on site?",taciturn:"I'm sorry, we don’t have a moving truck on site today.",answer_template:"We have *.",type:"filler",itemQuestion:"a moving truck",competitor:"a medium-sized delivery truck",sameCategory:"a Volkswagen camper",otherCategory:"a Ferrari",correct_response:"motorcycle"},{itemName:"music-hardrock",settingName:"music",vignette_start:"You are driving in a car with your neighbor. Please type ‘classic’ in the text area. The car only has an old CD player. You have the following styles of music:",vignette_continuation:"\\n\\nYour neighbor asks:",priorElicitation_context:"Please move all sliders all the way to the right. Suppose someone wants to listen to",priorElicitation_question:"listened to",question:"Do you have any hard rock?",taciturn:"I'm sorry, I don't have any hard rock.",answer_template:"I have some *.",type:"filler",itemQuestion:"hard rock",competitor:"classic rock",sameCategory:"heavy metal",otherCategory:"cool jazz",correct_response:"classic"},{itemName:"music-softrock",settingName:"music",vignette_start:"You are driving in a car with your neighbor. Please type ‘classic’ in the text area. The car only has an old CD player. You have the following styles of music:",vignette_continuation:"\\n\\nYour neighbor asks:",priorElicitation_context:"Please move all sliders all the way to the right. Suppose someone wants to listen to",priorElicitation_question:"listened to",question:"Do you have any soft rock?",taciturn:"I'm sorry, I don't have any soft rock.",answer_template:"I have some *.",type:"filler",itemQuestion:"soft rock",competitor:"cool jazz",sameCategory:"soul jazz",otherCategory:"death metal",correct_response:"classic"},{itemName:"airport-usa",settingName:"airport",vignette_start:"You are a customer service agent helping to book flights. Today there is ",vignette_continuation:"Please type ‘London’ in the text area.\\n\\nA customer asks:",priorElicitation_context:"Please move all sliders all the way to the left. Suppose someone wants to book",priorElicitation_question:"booked",question:"Do you have an afternoon flight to Boston?",taciturn:"I'm sorry, we don't have an afternoon flight to Boston today.",answer_template:"We have *.",type:"filler",itemQuestion:"an afternoon flight to Boston",competitor:"a morning flight to Boston",sameCategory:"an afternoon flight to San Francisco",otherCategory:"a flight to Australia",correct_response:"London"},{itemName:"airport-europe-UPDATED",settingName:"airport",vignette_start:"You are a customer service agent helping to book flights. Today there is",vignette_continuation:"Please type ‘London’ in the text area.\\n\\nA customer asks:",priorElicitation_context:"Please move all sliders all the way to the left. Suppose someone wants to book",priorElicitation_question:"booked",question:"Do you have a morning flight to Madrid?",taciturn:"I'm sorry, we don't have a morning flight to Madrid today.",answer_template:"We have *.",type:"filler",itemQuestion:"a morning flight to Madrid",competitor:"a morning flight to Barcelona with connections to other airports",sameCategory:"an evening flight to Paris",otherCategory:"a flight to New York",correct_response:"London"}]},"56d7":function(e,t,o){"use strict";o.r(t);var a=o("2b0e"),n=o("7591"),i=o.n(n),r=o("3665"),s=function(){var e=this,t=e._self._c;return t("Experiment",{attrs:{title:"question-answering-experiment"}},[t("InstructionScreen",{attrs:{title:"Welcome"}},[e._v(" Thank you for taking part in our experiment! "),t("br"),e._v(" You are participating in a study conducted by cognitive scientists at the University of Tübingen. Your participation in this research is voluntary. You may decline to answer any or all of the following questions. You may decline further participation, at any time, without adverse consequences. "),t("br"),t("br"),e._v(" Your anonymity is assured; the researchers who have requested your participation will not receive any personal information about you. "),t("br"),t("br"),e._v(" By pressing the button 'Next' you confirm that you are at least 18 years old and agree to participate in this study. ")]),t("InstructionScreen",{attrs:{title:"Instructions"}},[e._v(" In the following, you will see short descriptions of scenes in which a character asks a question. Your task is to write down an answer to that question. "),t("br"),t("br"),e._v(" Notice that there will also be simple "),t("b",[e._v("attention checking")]),e._v(" trials. You will recognize them immediately when you read the important text on each trial carefully -- those trials contain instructions for you to type a certain word in the textbox. Please spell the words exactly as stated in the instructions. "),t("br"),t("br"),e._v(" Please answer like you would naturally do when you were in a situation like the one described on each screen. "),t("br"),e._v(" Please respond naturally and reasonably. "),t("br"),e._v(" Please avoid jokes, insults or otherwise making the dialogues into something else than simple, harmless exchanges of information. ")]),e._l(e.trials,(function(o,a){return[o.type?[t("FreetypingScreen",{key:a,attrs:{trial:o,trial_type:"filler",index:a,progress:a/e.trials.length}})]:[t("FreetypingScreen",{key:a,attrs:{trial:o,trial_type:"main",index:a,progress:a/e.trials.length}})]]})),t("PostTestScreen"),t("SubmitResultsScreen")],2)},c=[],l=o("2ef0"),u=o.n(l),m=o("6d70"),p=o.n(m),h=o("50ff"),g=o.n(h),y=function(){var e=this,t=e._self._c;return t("Screen",{attrs:{progress:e.progress}},[t("Slide",[t("Record",{attrs:{data:{trialNr:e.index+1,itemName:e.trial.itemName,settingName:e.trial.settingName,trial_type:e.trial_type,correct_response:e.trial.correct_response}}}),e._l(e.createScreen.split("\\n"),(function(o,a){return t("span",{key:a},[e._v(" "+e._s(o)),t("br")])})),t("textarea",{directives:[{name:"model",rawName:"v-model",value:e.$magpie.measurements.answer,expression:"$magpie.measurements.answer"}],staticStyle:{width:"500px",height:"200px"},domProps:{value:e.$magpie.measurements.answer},on:{input:function(t){t.target.composing||e.$set(e.$magpie.measurements,"answer",t.target.value)}}}),e.$magpie.measurements.answer&&e.$magpie.measurements.answer.length>3?t("button",{on:{click:function(t){return e.$magpie.saveAndNextScreen()}}},[e._v(" Submit ")]):e._e()],2)],1)},d=[];function v(e){var t=u.a.shuffle(["competitor","sameCategory","otherCategory"]);console.log(t);var o=e.vignette_start,a=e.vignette_continuation,n=e.question;console.log(e.correct_response);var i=t.map(t=>e[t]);i.splice(-1,1,"and ".concat(i.at(-1)));i=i.join(", ").concat(".");var r=[o,i,a,'"'.concat(n).concat('"'),"\\n\\n","You reply: "].join(" ");return r}var f={name:"SliderRatingScreen",props:{trial:{type:Object,required:!0},trial_type:{type:String,required:!0},index:{type:Number,required:!0},progress:{type:Number,default:void 0}},methods:{createText:v},computed:{createScreen(){return v(this.trial)}}},w=f,_=o("2877"),k=Object(_["a"])(w,y,d,!1,null,null,null),b=k.exports,C=u.a.sample(["odd","even"]);const x=4,N=1,q="odd"==C?p.a.filter((e,t)=>t%2===0):p.a.filter((e,t)=>t%2!=0),E="odd"==C?g.a.filter((e,t)=>t%2===0):g.a.filter((e,t)=>t%2!=0);document.onselectstart=()=>!1,document.oncontextmenu=()=>!1;var S={name:"App",components:{FreetypingScreen:b},data(){return{trials:u.a.shuffle(u.a.concat(u.a.sampleSize(q,x),u.a.sampleSize(E,N)))}},computed:{_(){return u.a}}},Y=S,I=(o("ffbd"),Object(_["a"])(Y,s,c,!1,null,null,null)),A=I.exports,T={experimentId:"103",serverUrl:"https://mcmpact.ikw.uni-osnabrueck.de/magpie/",socketUrl:"wss://mcmpact.ikw.uni-osnabrueck.de/socket",completionUrl:"https://app.prolific.co/submissions/complete?cc=C1J3ETN9",contactEmail:"polina.tsvilodub@uni-tuebingen.de",mode:"prolific",language:"en"};a["default"].config.productionTip=!1,a["default"].use(i.a,{prefix:"Canvas"}),a["default"].use(r["a"],T),new a["default"]({render:e=>e(A)}).$mount("#app")},"6d70":function(e,t){e.exports=[{itemName:"cafe-pie",settingName:"cafe",vignette_start:"You are a server in a café. Today the café has",vignette_continuation:"\\n\\nA customer asks: ",question:"Do you have raspberry cake?",priorElicitation_context:"Suppose someone wants",priorElicitation_question:"got",taciturn:"I'm sorry, we don't have raspberry cake today.",answer_template:"We have *.",itemQuestion:"raspberry cake",competitor:"raspberry pie",sameCategory:"chocolate cookies",otherCategory:"cheese pizza",correct_response:"main"},{itemName:"cafe-pizza",settingName:"cafe",vignette_start:"You are a server in a café. Today the café has ",vignette_continuation:"\\n\\nA customer asks: ",question:"Do you have veggie pizza?",priorElicitation_context:"Suppose you learn someone wants to have",priorElicitation_question:"had",taciturn:"I'm sorry, we don't have veggie pizza today.",answer_template:"We have *.",itemQuestion:"veggie pizza",competitor:"cheese pizza",sameCategory:"pepperoni pizza",otherCategory:"raspberry pie",correct_response:"main"},{itemName:"bar-whiteWine",settingName:"bar",vignette_start:"You are a bartender in a hotel bar. The bar serves only ",vignette_continuation:"\\n\\nLate at night a woman walks in. She looks gloomy. She says:",question:"Do you have Sauvignon Blanc?",priorElicitation_context:"Suppose you learn someone wants to have",priorElicitation_question:"had",taciturn:"I'm sorry, we don't have Sauvignon Blanc today.",answer_template:"We have *.",itemQuestion:"Sauvignon Blanc",competitor:"Chardonnay",sameCategory:"craft beer",otherCategory:"iced coffee",correct_response:"main"},{itemName:"bar-tea",settingName:"bar",vignette_start:"You are a bartender in a hotel bar. The bar serves only",vignette_continuation:"\\n\\nA woman walks in. She says:",question:"Do you have iced tea?",priorElicitation_context:"Suppose you learn someone wants to have",priorElicitation_question:"had",taciturn:"I'm sorry, we don't have iced tea today.",answer_template:"We have *.",itemQuestion:"iced tea",competitor:"iced coffee",sameCategory:"soda",otherCategory:"Chardonnay",correct_response:"main"},{itemName:"touristInfo-childTheatre",settingName:"touristInfo",vignette_start:"You are working in a tourist office in a medium-sized tourist town. Today the following events are happening: ",vignette_continuation:"\\n\\nA young woman walks in and asks:",question:"Is there a theatre performance for children today?",priorElicitation_context:"Suppose you learn wants to go to",priorElicitation_question:"went to",taciturn:"I'm sorry, there is no theatre performance for children today.",answer_template:"There is *.",itemQuestion:"a theatre performance for children",competitor:"a circus show",sameCategory:"a trade fare",otherCategory:"a club event with a hip hop DJ",correct_response:"main"},{itemName:"touristInfo-clubbing",settingName:"touristInfo",vignette_start:"You are working in a tourist office in a medium-sized tourist town. Today the following events are happening: ",vignette_continuation:"\\n\\nA young woman walks in and asks:",question:"Is there a club event with electronic music today?",priorElicitation_context:"Suppose you learn wants to go to",priorElicitation_question:"went to",taciturn:"I'm sorry, there is no club event with electronic music today.",answer_template:"There is *.",itemQuestion:"a club event with electronic music",competitor:"a club event with a hip hop DJ",sameCategory:"live jazz music",otherCategory:"a circus show",correct_response:"main"},{itemName:"bookingAgency-lowClassAccommodation",settingName:"bookingAgency",vignette_start:"You work in a travel booking agency in a medium-sized tourist town. The following types of accommodation are still available for tomorrow night:",vignette_continuation:"\\n\\nA young man walks in and asks:",question:"Is there a bed in the youth hostel available for tomorrow night?",priorElicitation_context:"Suppose you learn a tourist calling a booking agency wants to book",priorElicitation_question:"want to book",taciturn:"I'm sorry, there are no more beds available in the youth hostel available for tomorrow night.",answer_template:"There is *.",itemQuestion:"a bed in the youth hostel",competitor:"a room in a cheap bed-and-breakfast",sameCategory:"a room in a budget hotel",otherCategory:"a suite in a four-star hotel",correct_response:"main"},{itemName:"bookingAgency-highClassAccommodation",settingName:"bookingAgency",vignette_start:"You work in a travel booking agency in a medium-sized tourist town. The following types of accommodation are still available for tomorrow night: ",vignette_continuation:"\\n\\nAn older man walks in and asks: ",question:"Is a single room in a five-star hotel available for tomorrow night?",priorElicitation_context:"Suppose you learn a tourist calling a booking agency wants to book",priorElicitation_question:"want to book",taciturn:"I'm sorry, there is no single room in a five-star hotel available for tomorrow night.",answer_template:"There is *.",itemQuestion:"a single room in a five-star hotel",competitor:"a suite in a four-star hotel",sameCategory:"an expensive apartment close to the city",otherCategory:"a room in a cheap bed-and-breakfast",correct_response:"main"},{itemName:"waterSport-motor",settingName:"waterSport",vignette_start:"You work in a water sports rental agency in a popular tourist region with a large lake for different types of water sports. The agency offers ",vignette_continuation:"\\n\\nA customer calls on the phone and asks:",question:"Do you rent jet skis?",priorElicitation_context:"Suppose you learn a customer at a water sports rental agency of a popular resort with a large lake wants to rent",priorElicitation_question:"want to rent",taciturn:"I'm sorry, we don’t rent jet skis.",answer_template:"We rent *.",itemQuestion:"jet skis",competitor:"water ski equipment",sameCategory:"rubber dinghies",otherCategory:"kayaks",correct_response:"main"},{itemName:"waterSport-muscle",settingName:"waterSport",vignette_start:"You work in a water sports rental agency in a popular tourist region with a large lake for different types of water sports. The agency offers ",vignette_continuation:"\\n\\nA customer calls on the phone and asks:",question:"Do you rent canoes?",priorElicitation_context:"Suppose you learn a customer at a water sports rental agency of a popular resort with a large lake wants to rent",priorElicitation_question:"want to rent",taciturn:"I'm sorry, we don’t rent canoes.",answer_template:"We rent *.",itemQuestion:"canoes",competitor:"kayaks",sameCategory:"pedal boats",otherCategory:"water ski equipment",correct_response:"main"},{itemName:"dutyFree-smokes",settingName:"dutyFree",vignette_start:"You are a flight attendant on an old-fashioned international flight. You are selling duty-free items to passengers. You currently have the following items on offer:",vignette_continuation:"\\n\\nAs you walk by, a passenger asks:",question:"Do you sell cigars?",priorElicitation_context:"Suppose you learn a passenger on an old-fashioned international flight would like to purchase",priorElicitation_question:"like to purchase",taciturn:"I'm sorry, we don’t sell cigars.",answer_template:"We sell *.",itemQuestion:"cigars",competitor:"cigarettes",sameCategory:"gin",otherCategory:"gingerbread",correct_response:"main"},{itemName:"dutyFree-sweets",settingName:"dutyFree",vignette_start:"You are a flight attendant on an old-fashioned international flight. You are selling duty free items to passengers. You currently have the following items on offer: ",vignette_continuation:"\\n\\nAs you walk by, a passenger asks:",question:"Do you sell cookies?",priorElicitation_context:"Suppose you learn a passenger on an old-fashioned international flight would like to purchase",priorElicitation_question:"like to purchase",taciturn:"I'm sorry, we don’t sell cookies.",answer_template:"We sell *.",itemQuestion:"cookies",competitor:"gingerbread",sameCategory:"granola bars",otherCategory:"cigarettes",correct_response:"main"},{itemName:"clothing-clothes",settingName:"clothing",vignette_start:"You work at a small designer clothing store. You currently have the following items in stock: ",vignette_continuation:"\\n\\nA customer comes in and asks:",question:"Do you have any Hawaiian shirts?",priorElicitation_context:"Suppose you learn a customer at a small designer shop is looking for",priorElicitation_question:"be looking for",taciturn:"I'm sorry, we don’t have any Hawaiian shirts.",answer_template:"We have *.",itemQuestion:"Hawaiian shirts",competitor:"shorts",sameCategory:"sweatshirts",otherCategory:"necklaces",correct_response:"main"},{itemName:"clothing-acc",settingName:"clothing",vignette_start:"You work at a small designer clothing store. You currently have the following items in stock: ",vignette_continuation:"\\n\\nA customer comes in and asks:",question:"Do you have any earrings?",priorElicitation_context:"Suppose you learn a customer at a small designer shop is looking for",priorElicitation_question:"be looking for",taciturn:"I'm sorry, we don’t have any earrings.",answer_template:"We have *.",itemQuestion:"earrings",competitor:"necklaces",sameCategory:"sunglasses",otherCategory:"shorts",correct_response:"main"},{itemName:"petAdoption-dogs",settingName:"petAdoption",vignette_start:"You work at an adoption center for rescued animals. You currently have the following animals at the center:",vignette_continuation:"\\n\\nA family comes in and asks:",question:"Do you have any Dalmatians?",priorElicitation_context:"Suppose you learn a family visiting a pet shelter is interested in adopting",priorElicitation_question:"be interested in adopting",taciturn:"I'm sorry, we don’t have any dalmatians.",answer_template:"We have *.",itemQuestion:"dalmatians",competitor:"golden retrievers",sameCategory:"chihuahuas",otherCategory:"gerbils",correct_response:"main"},{itemName:"petAdoption-hamster",settingName:"petAdoption",vignette_start:"You work at an adoption center for rescued animals. You currently have the following animals at the center:",vignette_continuation:"\\n\\nA family comes in and asks:",question:"Do you have any hamsters?",priorElicitation_context:"Suppose someone wants to have",priorElicitation_question:"had",taciturn:"I'm sorry, we don’t have any hamsters.",answer_template:"We have *.",itemQuestion:"hamsters",competitor:"gerbils",sameCategory:"ferrets",otherCategory:"golden retrievers",correct_response:"main"},{itemName:"books-romance",settingName:"books",vignette_start:"You work at a bookshop in a small town. You currently have",vignette_continuation:"\\n\\nA student walks in and asks:",question:"Do you have a book of love poems?",priorElicitation_context:"Suppose you learn a person at a book store is looking for",priorElicitation_question:"be interested in",taciturn:"I’m sorry, we don’t have love poems.",answer_template:"We sell *.",itemQuestion:"love poems",competitor:"books of French love letters",sameCategory:"historical dramas",otherCategory:"mystery novels",correct_response:"main"},{itemName:"books-fantasy",settingName:"books",vignette_start:"You work at a bookshop in a small town. You currently have",vignette_continuation:"\\n\\nA student walks in and asks:",question:"Do you sell psychological thrillers?",priorElicitation_context:"Suppose you learn a person at a book store is looking for",priorElicitation_question:"be interested in",taciturn:"I’m sorry, we don’t sell psychological thrillers.",answer_template:"We sell *.",itemQuestion:"psychological thrillers",competitor:"mystery novels",sameCategory:"adventure novels",otherCategory:"books of French love letters",correct_response:"main"},{itemName:"electronics-laptop",settingName:"electronics",vignette_start:"You work at a second hand electronics store. You currently have",vignette_continuation:"\\n\\nA young man walks in and asks:",question:"Do you have a MacBook Pro?",priorElicitation_context:"Suppose someone wants",priorElicitation_question:"got",taciturn:"I’m sorry, we don’t have a MacBook Pro.",answer_template:"We have *.",itemQuestion:"a MacBook Pro",competitor:"a MacBook Air",sameCategory:"a desktop computer",otherCategory:"an Xbox",correct_response:"main"},{itemName:"electronics-console",settingName:"electronics",vignette_start:"You work at a second hand electronics store. There are currently",vignette_continuation:"\\n\\nA young man walks in and asks:",question:"Do you have a PlayStation?",priorElicitation_context:"Suppose you learn a customer walks into a second hand electronics store and is looking for",priorElicitation_question:"be looking for",taciturn:"I’m sorry, we don’t have a PlayStation.",answer_template:"We have *.",itemQuestion:"a PlayStation",competitor:"an Xbox",sameCategory:"a Gameboy",otherCategory:"a MacBook Air",correct_response:"main"},{itemName:"gym-yoga",settingName:"gymActivities",vignette_start:"You work at the reception desk of a gym. The gym currently offers",vignette_continuation:"\\n\\nA woman walks in and asks:",question:"Do you offer yoga classes?",priorElicitation_context:"Suppose you learn a customer at a gym would like to participate in",priorElicitation_question:"like to participate in",taciturn:"I’m sorry, we don’t have yoga.",answer_template:"We have *.",itemQuestion:"yoga classes",competitor:"a pilates class",sameCategory:"zumba classes",otherCategory:"kickboxing",correct_response:"main"},{itemName:"gym-boxing",settingName:"gymActivities",vignette_start:"You work at the reception desk of a gym. The gym currently offers",vignette_continuation:"\\n\\nA young guy walks in and asks:",question:"Do you offer boxing classes?",priorElicitation_context:"Suppose you learn a customer at a gym would like to participate in",priorElicitation_question:"like to participate in",taciturn:"I’m sorry, we don’t have boxing.",answer_template:"We have *.",itemQuestion:"boxing classes",competitor:"kickboxing classes",sameCategory:"karate classes",otherCategory:"pilates",correct_response:"main"},{itemName:"kidsActivities-crafts",settingName:"kidsActivities",vignette_start:"You are a teacher at a summer camp. Today a new group of children arrived. They need to sign up for different activities. The camp offers ",vignette_continuation:"\\n\\nA kid walks up to you and asks:",question:"Is there a pottery class?",priorElicitation_context:"Suppose you learn a kid who just arrived at a summer camp wants to sign up for",priorElicitation_question:"like to sign up for",taciturn:"I'm sorry, there is no pottery class.",answer_template:"There is *.",itemQuestion:"a pottery class",competitor:"a watercolor painting class",sameCategory:"a carpentry workshop",otherCategory:"an acrobatics class",correct_response:"main"},{itemName:"kidsActivities-sports",settingName:"kidsActivities",vignette_start:"You are a teacher at a summer camp. Today a new group of children arrived. They need to sign up for different activities. The camp offers ",vignette_continuation:"\\n\\nA kid walks up to you and asks:",question:"Is there a gymnastics class?",priorElicitation_context:"Suppose you learn a kid who just arrived at a summer camp wants to sign up for",priorElicitation_question:"like to sign up for",taciturn:"I'm sorry, there is no gymnastics class.",answer_template:"There is *.",itemQuestion:"a gymnastics class",competitor:"an acrobatics class",sameCategory:"a karate class",otherCategory:"a watercolor painting class",correct_response:"main"},{itemName:"friendsActivities-boardGames",settingName:"friendsActivities",vignette_start:"You are hosting a casual Saturday night get together with your friends at your house. For activities, you prepared",vignette_continuation:"\\n\\nYour friends arrive and ask you:",question:"Do you have Scrabble?",priorElicitation_context:"Suppose you learn that some friends who will come over to your house want to spend the evening with",priorElicitation_question:"want to spend the evening with",taciturn:"I'm sorry, I don't have Scrabble.",answer_template:"I have *.",itemQuestion:"Scrabble",competitor:"Monopoly",sameCategory:"checkers",otherCategory:"some movies",correct_response:"main"},{itemName:"friendsActivities-videoEntertainment",settingName:"friendsActivities",vignette_start:"You are hosting a casual Saturday night get together with your friends at your house. For activities, you prepared",vignette_continuation:"\\n\\nYour friends arrive and ask you:",question:"Do you have Netflix?",priorElicitation_context:"Suppose you learn that some friends who will come over to your house want to spend the evening with",priorElicitation_question:"want to spend the evening with",taciturn:"I'm sorry, I don't have Netflix.",answer_template:"I have *.",itemQuestion:"Netflix",competitor:"some movies",sameCategory:"Xbox games",otherCategory:"Monopoly",correct_response:"main"},{itemName:"interior-green",settingName:"interior",vignette_start:"You like to decorate the house and often craft decorations yourself. You often give away crafts and plants to friends and family. You currently have ",vignette_continuation:"\\n\\nA friend just moved and wants to get something to decorate her new apartment. She visits you and asks:",question:"Do you have an aloe vera plant?",priorElicitation_context:"Suppose someone wants",priorElicitation_question:"got",taciturn:"I'm sorry, I don’t have an aloe vera.",answer_template:"I have *.",itemQuestion:"an aloe vera plant",competitor:"an agave plant",sameCategory:"tulips",otherCategory:"an oil painting",correct_response:"main"},{itemName:"interior-deco",settingName:"interior",vignette_start:"You like to decorate the house and often craft decorations yourself. You often give away crafts and plants to friends and family. You currently have ",vignette_continuation:"\\n\\nA friend just moved and wants to get something to decorate her new apartment. She visits you and asks:",question:"Do you have watercolour paintings?",priorElicitation_context:"Suppose you learn that a friend who just moved into a new apartment wants to decorate it with",priorElicitation_question:"want to decorate it with",taciturn:"I'm sorry, I don’t have watercolor paintings.",answer_template:"I have *.",itemQuestion:"watercolor paintings",competitor:"an oil painting",sameCategory:"some printed photographs",otherCategory:"an agave plant",correct_response:"main"},{itemName:"zoo-xl",settingName:"zoo",vignette_start:"You took your kids to the zoo today. You carefully studied the map of the zoo and saw that there is",vignette_continuation:"\\n\\nYour eight-year-old is impatient and asks:",question:"Can we see the tiger?",priorElicitation_context:"Suppose you learn that a kid visiting a zoo wants to see",priorElicitation_question:"want to see",taciturn:"I’m sorry, they don’t have a tiger here.",answer_template:"They have *.",itemQuestion:"a tiger",competitor:"a lion",sameCategory:"a giraffe",otherCategory:"iguanas",correct_response:"main"},{itemName:"zoo-reptiles",settingName:"zoo",vignette_start:"You took your kids to the zoo today. You carefully studied the map of the zoo and saw that there is",vignette_continuation:"\\n\\nYour eight-year-old is impatient and asks:",question:"Can we see the chameleon?",priorElicitation_context:"Suppose you learn that a kid visiting a zoo wants to see",priorElicitation_question:"want to see",taciturn:"I'm sorry, they don't have chameleons here.",answer_template:"They have *.",itemQuestion:"a chameleon",competitor:"iguanas",sameCategory:"turtles",otherCategory:"a lion",correct_response:"main"}]},ffbd:function(e,t,o){"use strict";o("169d")}});
//# sourceMappingURL=app.faf7c66d.js.map