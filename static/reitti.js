var canvas;
var ctx;
var stops;
var roads;
var routes;

window.onload = function() {
    stops=JSON.parse(document.getElementById('mapstops').value);
    roads=JSON.parse(document.getElementById('maproads').value);
    routes=JSON.parse(document.getElementById('maproutes').value);
    
    canvas = document.getElementById("reittiCanvas");
    ctx = canvas.getContext("2d");
    loadmap(ctx,0);
    
    set_choose_clicks();
};

function loadmap(ctx,ind){
    //draw lines (roads)
    for(var i=0;i<roads.length;i++){
        var road=roads[i];
        addline(ctx,road.x1,road.y1,road.x2,road.y2,width=5,color='#505050');
    }
    
    //draw route
    if(routes.length>0){
        for(var i=0;i<routes[ind].length;i++){
            var between=routes[ind][i];
            addline(ctx,between.x1,between.y1,between.x2,between.y2,width=10,color=between.color);
        }
    }
    
    //draw points (stops) and names
    for(var i=0;i<stops.length;i++){
        var stop=stops[i];
        addpoint(ctx,stop.x,stop.y,20);
        addtext(ctx,stop.name,stop.x-9,stop.y+9);
    }
};

function set_choose_clicks(){
    var routecount=document.getElementById('routecount').value;
    if(routecount>1){
        var routetable=document.getElementById('routetable');
        var buttons=routetable.getElementsByTagName("span");
        for(var i=0;i<routecount;i++){
            buttons[i].addEventListener("click", changeroute);
        }
    }
};

function changeroute(e){
    e.preventDefault();
    var i = this.getAttribute('data-id');
    ctx.clearRect(0,0,canvas.width,canvas.height);
    loadmap(ctx,i);
    console.log(i);
};

function addtext(ctx,text,x,y){
    ctx.beginPath();
    ctx.fillStyle='#C8C8C8';
    ctx.font = "28px Courier New";
    ctx.fillText(text,x,y);
};

function addline(ctx,x,y,x2,y2,width,color){
    ctx.beginPath();
    ctx.strokeStyle=color;
    ctx.lineWidth=width;
    ctx.moveTo(x,y);
    ctx.lineTo(x2,y2);
    ctx.stroke();
};

function addpoint(ctx,x,y,d){
    ctx.beginPath();
    ctx.fillStyle='#282828';
    ctx.arc(x,y,d,0,Math.PI*2,false);
    ctx.fill();
    ctx.strokeStyle='#C8C8C8';
    ctx.lineWidth=4.0;
    ctx.arc(x,y,d,0,Math.PI*2,false);
    ctx.stroke();
}