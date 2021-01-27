const express = require('express')
const http = require('http')
const app = express();
const server = http.createServer(app)
const fs = require('fs')

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
    fs.readFile('./static/loading.html',(err,data)=>{
        if(err){
            res.send('에러')
        }else{
            res.writeHead(200,{'content-Type':'text/html'})
            res.write(data)
            res.end()
        }
    })
    setTimeout(function() {
        
        //여기다가 다운 하는거 넣음
      }, 3000);
    console.log(req.query.url) //이게 url
})

server.listen(3000,()=>{
    console.log("서버 실행중!")
})