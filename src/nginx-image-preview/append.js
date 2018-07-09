/* 
description:
    auto show images in the dirctory while contants.
nginx configuraion:
    location / {
        alias /home/public/;
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
        sub_filter '</body>' '<script src="/js/append.js"></script></body>';
        sub_filter_once on;
    }
*/
(function(ps){
    var pagesize = ps ? ps : 5;
    var dd = document.createElement("details");
    var ss = document.createElement("summary");
    ss.innerHTML='expand';
    dd.appendChild(ss);
    
    //create images waper.
    var showbox = document.createElement("div");
    showbox.id = 'showbox';
    showbox.style="text-align: center;";
    //should append in details tag.
    //document.body.appendChild(showbox);
    //find all a link
    var alinks = document.body.getElementsByTagName('a');
    var imglinks = new Array();
    //filter image link
    for(var i=0;i<alinks.length;i++){
        var xhref = alinks[i].getAttribute('href')
        if(xhref.match(/.+\.(jpg|png)$/gi)){
            //console.log('find img:'+xhref);
            imglinks.push(xhref);

        }

    }
    //calc page
    var curpage = 1;
    var pagecount = Math.round((imglinks.length - 1)/pagesize)+1;
    //console.log('pagecount:'+pagecount);

    //page&pagecount
    var pinfo = document.createElement("p");
    pinfo.style='margin:10px auto;position:absolute;width:97%;z-index:-1';
    pinfo.align='center';
    function changepage(n){
        //if(!dd.hasAttribute('open')){return;}
        //clear content befor
        showbox.innerHTML = '';
        for(var i=(n-1)*pagesize;i<n*pagesize;i++){
            if(imglinks[i]){
                var im = document.createElement('img');
                im.src = imglinks[i];
                im.alt = imglinks[i];
                im.title = imglinks[i];
                im.style="margin: 10px auto;";
                //console.log('create img:'+imglinks[i])
                showbox.appendChild(im); 
            }       
        }
        pinfo.innerHTML = '['+curpage+'/'+pagecount+']';
    }
    //prev&next button
    var prevbtn = document.createElement("a");
    prevbtn.style='float:left;margin:10px;';
    prevbtn.href='#showbox';
    prevbtn.innerHTML = 'prev';
    prevbtn.onclick = function(){
        curpage--;
        if(curpage < 1){
            console.log('already first page.');
            curpage = pagecount;
        }
        changepage(curpage);
    }
    

    

    var nextbtn = document.createElement("a");
    nextbtn.style='float:right;margin:10px;';
    nextbtn.href='#showbox';
    nextbtn.innerHTML = 'next';
    nextbtn.onclick = function(){
        curpage++;
        if(curpage > pagecount){
            console.log('already lasted page.');
            curpage = 1;           
        }
        changepage(curpage);
    }
    changepage(1);

    dd.appendChild(showbox);
    

    var btnbox = document.createElement("div");
    btnbox.style='min-height:50px;margin:10px 10px 10px 10px;font-size:20px;align:center';
    btnbox.appendChild(prevbtn);
    btnbox.appendChild(pinfo);
    btnbox.appendChild(nextbtn);
    dd.appendChild(btnbox);
    //append only if current dirctory contants image links
    //console.log('imglinks len:'+imglinks.length)
    if(imglinks && imglinks.length>0){
        document.body.appendChild(dd);
        document.write('<hr>');
    }
    // append ToS(trem of service)
    var txt = document.createElement("div");
    txt.style="text-align: center;";
    txt.innerHTML = '本站资源全部来互联网，如有违规，请联系管理员&lt; me AT gentlehu DOT com &gt;删除';
    document.body.appendChild(txt);

})(5);//parameter:pagesize