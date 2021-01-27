const express = require('express')
const http = require('http')
const app = express();
const server = http.createServer(app)
const fs = require('fs')

var Youtube = require('youtube-node');
var youtube = new Youtube();

app.set('view engine', 'ejs')
app.engine('html', require('ejs').renderFile)

youtube.setKey('AIzaSyDiIiJvN4NmTirr3IUca1a2_iT8H01RaGg');//api키 입력
let code ="a"
app.use('/css',express.static('./static/css'))
app.use('/js',express.static('./static/js'))
app.use('/help',express.static('./static/help'))

app.get('/',function(req,res){
    fs.readFile('./static/index.html',(err,data)=>{
        if(err){
            res.send('에러')
        }else{
            res.writeHead(200,{'content-Type':'text/html'})
            res.write(data)
            res.end()
        }
    })
})


app.get('/loading',function(req,res){
   var url = req.query.url
   youtube.search(url, 1, function (err, result) { // 검색 실행
    if (err) { console.log(err); return; } // 에러일 경우 에러공지하고 빠져나감



    var items = result["items"]; // 결과 중 items 항목만 가져옴
        var it = items[0];            
        console.log(it.snippet.thumbnails.medium.url)

        var title = it["snippet"]["title"];
        var photo = it.snippet.thumbnails.medium.url;
        var ver = req.query.ver
        res.render(__dirname+"/download.ejs",{title : title, photo : photo, id: url,ver:ver})
       
        
        
    
});
  

})

app.get('/download',function(req,res){
    
})

server.listen(3000,()=>{
    console.log("서버 실행중!")
})