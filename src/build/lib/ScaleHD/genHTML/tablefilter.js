var TblId,SearchFlt,SlcArgs;function setFilterGrid(e){var t,r,a=grabEBI(e);if(null!=a&&"table"==a.nodeName.toLowerCase()){if(1<arguments.length)for(var l=0;l<arguments.length;l++){switch((typeof arguments[l]).toLowerCase()){case"number":t=arguments[l];break;case"object":r=arguments[l]}}null==t?t=2:t+=2;var n=getCellsNb(e,t);a.tf_ncells=n,null==a.tf_ref_row&&(a.tf_ref_row=t),a.tf_Obj=r,hasGrid(e)||AddGrid(e)}}function AddGrid(e){TblId.push(e);var t,r,a,l,n,i,o,s,f,d,c,g,p,u,_,h,b,v,w,y,C,T,m,E=grabEBI(e),I=E.tf_Obj,F=E.tf_ncells;if(r=null==I||0!=I.grid,a=null!=I&&1==I.btn,l=null!=I&&null!=I.btn_text?I.btn_text:"go",n=null==I||0!=I.enter_key,i=!(null==I||!I.mod_filter_fn),o=null!=I&&null!=I.display_all_text?I.display_all_text:"",s=null==I||0!=I.on_change,f=null!=I&&1==I.rows_counter,d=null!=I&&null!=I.rows_counter_text?I.rows_counter_text:"Displayed rows: ",c=null!=I&&1==I.btn_reset,g=null!=I&&null!=I.btn_reset_text?I.btn_reset_text:"Reset",p=null!=I&&1==I.sort_select,u=null!=I&&1==I.paging,_=null!=I&&null!=I.paging_length?I.paging_length:10,h=null!=I&&1==I.loader,b=null!=I&&null!=I.loader_text?I.loader_text:"Loading...",v=null!=I&&1==I.exact_match,w=null!=I&&1==I.alternate_rows,y=!(null==I||!I.col_operation),C=!(null==I||!I.rows_always_visible),T=!(null==I||!I.col_width),m=!(null==I||!I.bind_script),E.tf_fltGrid=r,E.tf_displayBtn=a,E.tf_btnText=l,E.tf_enterKey=n,E.tf_isModfilter_fn=i,E.tf_display_allText=o,E.tf_on_slcChange=s,E.tf_rowsCounter=f,E.tf_rowsCounter_text=d,E.tf_btnReset=c,E.tf_btnReset_text=g,E.tf_sortSlc=p,E.tf_displayPaging=u,E.tf_pagingLength=_,E.tf_displayLoader=h,E.tf_loadText=b,E.tf_exactMatch=v,E.tf_alternateBgs=w,E.tf_startPagingRow=0,i&&(E.tf_modfilter_fn=I.mod_filter_fn),r){var B=E.insertRow(0);B.className="fltrow";for(var N=0;N<F;N++){var x=B.insertCell(N);if(t=N==F-1&&1==a?"flt_s":"flt",null==I||null==I["col_"+N]||"none"==I["col_"+N]){var R;R=null==I||null==I["col_"+N]?"text":"hidden";var A=createElm("input",["id","flt"+N+"_"+e],["type",R],["class",t]);A.className=t,x.appendChild(A),n&&(A.onkeypress=DetectKey)}else if("select"==I["col_"+N]){var L=createElm("select",["id","flt"+N+"_"+e],["class",t]);if(L.className=t,x.appendChild(L),PopulateOptions(e,N),u){var G=new Array;G.push(e),G.push(N),G.push(F),G.push(o),G.push(p),G.push(u),SlcArgs.push(G)}n&&(L.onkeypress=DetectKey),s&&(L.onchange=i?I.mod_filter_fn:function(){Filter(e)})}if(N==F-1&&1==a){var P=createElm("input",["id","btn"+N+"_"+e],["type","button"],["value",l],["class","btnflt"]);P.className="btnflt",x.appendChild(P),P.onclick=i?I.mod_filter_fn:function(){Filter(e)}}}}if(f||c||u||h){var S=createElm("div",["id","inf_"+e],["class","inf"]);if(S.className="inf",E.parentNode.insertBefore(S,E),f){var O,V=createElm("div",["id","ldiv_"+e]);f?V.className="ldiv":V.style.display="none",O=u?_:getRowsNb(e);var j=createElm("span",["id","totrows_span_"+e],["class","tot"]);j.className="tot",j.appendChild(createText(O));var k=createText(d);V.appendChild(k),V.appendChild(j),S.appendChild(V)}if(h){var M=createElm("div",["id","load_"+e],["class","loader"]);M.className="loader",M.style.display="none",M.appendChild(createText(b)),S.appendChild(M)}if(u){var H=createElm("div",["id","mdiv_"+e]);u?H.className="mdiv":H.style.display="none",S.appendChild(H);var D=E.tf_ref_row,K=grabTag(E,"tr"),W=K.length,$=Math.ceil((W-D)/_),q=createElm("select",["id","slcPages_"+e]);q.onchange=function(){h&&showLoader(e,""),E.tf_startPagingRow=this.value,GroupByPage(e),h&&showLoader(e,"none")};var z=createElm("span",["id","pgspan_"+e]);grabEBI("mdiv_"+e).appendChild(createText(" Page ")),grabEBI("mdiv_"+e).appendChild(q),grabEBI("mdiv_"+e).appendChild(createText(" of ")),z.appendChild(createText($+" ")),grabEBI("mdiv_"+e).appendChild(z);for(var J=D;J<W;J++)K[J].setAttribute("validRow","true");setPagingInfo(e),h&&showLoader(e,"none")}if(c&&r){var Q=createElm("div",["id","reset_"+e]);c?Q.className="rdiv":Q.style.display="none";var U=createElm("a",["href","javascript:clearFilters('"+e+"');Filter('"+e+"');"]);U.appendChild(createText(g)),Q.appendChild(U),S.appendChild(Q)}}T&&(E.tf_colWidth=I.col_width,setColWidths(e)),w&&!u&&setAlternateRows(e),y&&(E.tf_colOperation=I.col_operation,setColOperation(e)),C&&(E.tf_rowVisibility=I.rows_always_visible,u&&setVisibleRows(e)),m&&(E.tf_bindScript=I.bind_script,null!=E.tf_bindScript&&null!=E.tf_bindScript.target_fn&&E.tf_bindScript.target_fn.call(null,e))}function PopulateOptions(e,t){var r=grabEBI(e),a=r.tf_ncells,l=r.tf_display_allText,n=r.tf_sortSlc,i=(r.tf_displayPaging,r.tf_ref_row),o=grabTag(r,"tr"),s=new Array,f=0,d=new Option(l,"",!1,!1);grabEBI("flt"+t+"_"+e).options[f]=d;for(var c=i;c<o.length;c++){var g=getChildElms(o[c]).childNodes,p=g.length;o[c].getAttribute("paging");if(p==a)for(var u=0;u<p;u++)if(t==u){var _=getCellText(g[u]),h=!1;for(w in s)_==s[w]&&(h=!0);h||s.push(_)}}for(y in n&&s.sort(),s){f++;d=new Option(s[y],s[y],!1,!1);grabEBI("flt"+t+"_"+e).options[f]=d}}function Filter(e){showLoader(e,""),SearchFlt=getFilters(e);var t=grabEBI(e);null!=t.tf_Obj?fprops=t.tf_Obj:fprops=new Array;for(var r=new Array,a=getCellsNb(e),l=(getRowsNb(e),0),n=t.tf_exactMatch,i=t.tf_displayPaging,o=0;o<SearchFlt.length;o++)r.push(grabEBI(SearchFlt[o]).value.toLowerCase());for(var s=t.tf_ref_row,f=grabTag(t,"tr"),d=s;d<f.length;d++){"none"==f[d].style.display&&(f[d].style.display="");var c=getChildElms(f[d]).childNodes,g=c.length;if(g==a){for(var p=new Array,u=new Array,_=!0,h=0;h<g;h++){var b=getCellText(c[h]).toLowerCase();if(p.push(b),""!=r[h]){var v=parseFloat(b);if(/<=/.test(r[h])&&!isNaN(v))v<=parseFloat(r[h].replace(/<=/,""))?u[h]=!0:u[h]=!1;else if(/>=/.test(r[h])&&!isNaN(v))v>=parseFloat(r[h].replace(/>=/,""))?u[h]=!0:u[h]=!1;else if(/</.test(r[h])&&!isNaN(v))v<parseFloat(r[h].replace(/</,""))?u[h]=!0:u[h]=!1;else if(/>/.test(r[h])&&!isNaN(v))v>parseFloat(r[h].replace(/>/,""))?u[h]=!0:u[h]=!1;else{var w;w=n||"select"==fprops["col_"+h]?new RegExp("(^)"+regexpEscape(r[h])+"($)","gi"):new RegExp(regexpEscape(r[h]),"gi"),u[h]=w.test(b)}}}for(var y=0;y<a;y++)""==r[y]||u[y]||(_=!1)}_?(f[d].style.display="",i&&f[d].setAttribute("validRow","true")):(f[d].style.display="none",l++,i&&f[d].setAttribute("validRow","false"))}t.tf_nRows=parseInt(getRowsNb(e))-l,i||applyFilterProps(e),i&&(t.tf_startPagingRow=0,setPagingInfo(e))}function setPagingInfo(e){for(var t=grabEBI(e),r=parseInt(t.tf_ref_row),a=t.tf_pagingLength,l=grabTag(t,"tr"),n=grabEBI("mdiv_"+e),i=grabEBI("slcPages_"+e),o=grabEBI("pgspan_"+e),s=0,f=r;f<l.length;f++)"true"==l[f].getAttribute("validRow")&&s++;var d=Math.ceil(s/a);if(o.innerHTML=d,i.innerHTML="",0<d){n.style.visibility="visible";for(var c=0;c<d;c++){var g=new Option(c+1,c*a,!1,!1);i.options[c]=g}}else n.style.visibility="hidden";GroupByPage(e)}function GroupByPage(e){showLoader(e,"");for(var t=grabEBI(e),r=parseInt(t.tf_ref_row),a=parseInt(t.tf_pagingLength),l=parseInt(t.tf_startPagingRow),n=l+a,i=grabTag(t,"tr"),o=0,s=new Array,f=r;f<i.length;f++){"true"==i[f].getAttribute("validRow")&&s.push(f)}for(h=0;h<s.length;h++)h>=l&&h<n?(o++,i[s[h]].style.display=""):i[s[h]].style.display="none";t.tf_nRows=parseInt(o),applyFilterProps(e)}function applyFilterProps(e){t=grabEBI(e);var r=t.tf_rowsCounter,a=t.tf_nRows,l=t.tf_rowVisibility,n=t.tf_alternateBgs,i=t.tf_colOperation;r&&showRowsCounter(e,parseInt(a)),l&&setVisibleRows(e),n&&setAlternateRows(e),i&&setColOperation(e),showLoader(e,"none")}function hasGrid(e){var t=!1,r=grabEBI(e);if(null!=r&&"table"==r.nodeName.toLowerCase())for(i in TblId)e==TblId[i]&&(t=!0);return t}function getCellsNb(e,t){var r=grabEBI(e);return getChildElms(null==t?grabTag(r,"tr")[0]:grabTag(r,"tr")[t]).childNodes.length}function getRowsNb(e){var t=grabEBI(e),r=t.tf_ref_row,a=grabTag(t,"tr").length;return parseInt(a-r)}function getFilters(e){var t=new Array,r=grabEBI(e),a=grabTag(r,"tr")[0].childNodes;if(r.tf_fltGrid)for(var l=0;l<a.length;l++)t.push(a[l].firstChild.getAttribute("id"));return t}function clearFilters(e){for(i in SearchFlt=getFilters(e))grabEBI(SearchFlt[i]).value=""}function showLoader(e,t){var r=grabEBI("load_"+e);null!=r&&"none"==t?setTimeout("grabEBI('load_"+e+"').style.display = '"+t+"'",150):null!=r&&"none"!=t&&(r.style.display=t)}function showRowsCounter(e,t){var r=grabEBI("totrows_span_"+e);null!=r&&"span"==r.nodeName.toLowerCase()&&(r.innerHTML=t)}function getChildElms(e){if(1==e.nodeType){for(var t=e.childNodes,r=0;r<t.length;r++){var a=t[r];3==a.nodeType&&e.removeChild(a)}return e}}function getCellText(e){for(var t="",r=e.childNodes,a=0;a<r.length;a++){var l=r[a];3==l.nodeType?t+=l.data:t+=getCellText(l)}return t}function getColValues(e,t,r){for(var a=grabEBI(e),l=grabTag(a,"tr"),n=l.length,i=parseInt(a.tf_ref_row),o=getCellsNb(e,i),s=new Array,f=i;f<n;f++){var d=getChildElms(l[f]).childNodes,c=d.length;if(c==o)for(var g=0;g<c;g++)if(g==t&&""==l[f].style.display){var p=getCellText(d[g]).toLowerCase();r?s.push(parseFloat(p)):s.push(p)}}return s}function setColWidths(e){if(hasGrid(e)){var t=grabEBI(e);t.style.tableLayout="fixed";for(var r=t.tf_colWidth,a=parseInt(t.tf_ref_row),l=grabTag(t,"tr")[0],n=getCellsNb(e,a),i=0;i<r.length;i++)for(var o=0;o<n;o++)cell=l.childNodes[o],o==i&&(cell.style.width=r[i])}}function setVisibleRows(e){if(hasGrid(e))for(var t=grabEBI(e),r=grabTag(t,"tr"),a=r.length,l=t.tf_displayPaging,n=t.tf_rowVisibility,i=0;i<n.length;i++)n[i]<=a&&(l&&r[n[i]].setAttribute("validRow","true"),r[n[i]].style.display="")}function setAlternateRows(e){if(hasGrid(e)){for(var t=grabEBI(e),r=grabTag(t,"tr"),a=r.length,l=parseInt(t.tf_ref_row),n=new Array,i=l;i<a;i++)""==r[i].style.display&&n.push(i);for(var o=0;o<n.length;o++)r[n[o]].className=o%2==0?"even":"odd"}}function setColOperation(e){if(hasGrid(e)){var t=grabEBI(e),r=t.tf_colOperation.id,a=t.tf_colOperation.col,l=t.tf_colOperation.operation,n=t.tf_colOperation.write_method;if("object"==(typeof r).toLowerCase()&&"object"==(typeof a).toLowerCase()&&"object"==(typeof l).toLowerCase()){grabTag(t,"tr").length,getCellsNb(e,parseInt(t.tf_ref_row));for(var i=new Array,o=0;o<a.length;o++)i.push(getColValues(e,a[o],!0));for(var s=0;s<i.length;s++){for(var f=0,d=0,c=0;c<i[s].length;c++){var g=i[s][c];if(!isNaN(g))switch(l[s].toLowerCase()){case"sum":f+=parseFloat(g);break;case"mean":d++,f+=parseFloat(g)}}switch(l[s].toLowerCase()){case"mean":f/=d}if(null!=n&&"object"==(typeof n).toLowerCase()){if(f=f.toFixed(2),null!=grabEBI(r[s]))switch(n[s].toLowerCase()){case"innerhtml":grabEBI(r[s]).innerHTML=f;break;case"setvalue":grabEBI(r[s]).value=f;break;case"createtextnode":var p=grabEBI(r[s]).firstChild,u=createText(f);grabEBI(r[s]).replaceChild(u,p)}}else try{grabEBI(r[s]).innerHTML=f.toFixed(2)}catch(e){}}}}}function grabEBI(e){return document.getElementById(e)}function grabTag(e,t){return e.getElementsByTagName(t)}function regexpEscape(t){for(e in chars=new Array("\\","[","^","$",".","|","?","*","+","(",")"),chars)r=chars[e],a=new RegExp("\\"+r,"g"),t=t.replace(a,"\\"+r);var r;return t}function createElm(e){var t=document.createElement(e);if(1<arguments.length)for(var r=0;r<arguments.length;r++){switch((typeof arguments[r]).toLowerCase()){case"object":2==arguments[r].length&&t.setAttribute(arguments[r][0],arguments[r][1])}}return t}function createText(e){return document.createTextNode(e)}function DetectKey(e){var r,a,l,n=e||(window.event?window.event:null);n&&("13"==(n.charCode?n.charCode:n.keyCode?n.keyCode:n.which?n.which:0)&&(r=this.getAttribute("id"),a=this.getAttribute("id").split("_")[0],l=r.substring(a.length+1,r.length),t=grabEBI(l),t.tf_isModfilter_fn?t.tf_modfilter_fn.call():Filter(l)))}function importScript(e,t){for(var r=!1,a=grabTag(document,"script"),l=0;l<a.length;l++)if(a[l].src.match(t)){r=!0;break}if(!r){var n=grabTag(document,"head")[0],i=createElm("script",["id",e],["type","text/javascript"],["src",t]);n.appendChild(i)}}function TF_GetFilterIds(){try{return TblId}catch(e){alert("TF_GetFilterIds() fn: could not retrieve any ids")}}function TF_HasGrid(e){return hasGrid(e)}function TF_GetFilters(e){try{return getFilters(e)}catch(e){alert("TF_GetFilters() fn: table id not found")}}function TF_GetStartRow(e){try{return grabEBI(e).tf_ref_row}catch(e){alert("TF_GetStartRow() fn: table id not found")}}function TF_GetColValues(e,t,r){if(hasGrid(e))return getColValues(e,t,r);alert("TF_GetColValues() fn: table id not found")}function TF_Filter(e){grabEBI(e);TF_HasGrid(e)?Filter(e):alert("TF_Filter() fn: table id not found")}function TF_RemoveFilterGrid(e){if(TF_HasGrid(e)){var t=grabEBI(e);clearFilters(e),null!=grabEBI("inf_"+e)&&t.parentNode.removeChild(t.previousSibling);for(var r=grabTag(t,"tr"),a=0;a<r.length;a++){r[a].style.display="";try{r[a].hasAttribute("validRow")&&r[a].removeAttribute("validRow")}catch(e){for(var l=0;l<r[a].attributes.length;l++)"validrow"==r[a].attributes[l].nodeName.toLowerCase()&&r[a].removeAttribute("validRow")}}if(t.tf_alternateBgs)for(var n=0;n<r.length;n++)r[n].className="";for(i in t.tf_fltGrid&&t.deleteRow(0),TblId)e==TblId[i]&&TblId.splice(i,1)}else alert("TF_RemoveFilterGrid() fn: table id not found")}function TF_ClearFilters(e){TF_HasGrid(e)?clearFilters(e):alert("TF_ClearFilters() fn: table id not found")}function TF_SetFilterValue(e,t,r){if(TF_HasGrid(e)){var a=getFilters(e);for(i in a)i==t&&(grabEBI(a[i]).value=r)}else alert("TF_SetFilterValue() fn: table id not found")}TblId=new Array,SlcArgs=new Array;var colValues=new Array;function setAutoComplete(r){var e=grabEBI(r).tf_bindScript,a=(e.name,e.path);!function(){for(var e=TF_GetFilters(r),t=0;t<e.length;t++)"input"==grabEBI(e[t]).nodeName.toLowerCase()?colValues.push(getColValues(r,t)):colValues.push("");try{actb(grabEBI(e[0]),colValues[0])}catch(e){alert(a+" script may not be loaded")}}()}
