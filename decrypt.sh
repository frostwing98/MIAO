#!/bin/bash
#go run wxapkg_decrypt.go -wxid packages/$1 -in packages/$1.wxapkg -out packages/$1-o.wxapkg
wxid=$1
echo ${wxid:0:4} ${wxid:4:2}
cp /storage/miniapp/wechat/packages/${wxid:0:4}/${wxid:4:2}/$1.wxapkg ./output/
node wuWxapkg.js output/$1.wxapkg
