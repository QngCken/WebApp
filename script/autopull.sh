#!/bin/sh
    export LANG=en_us.UTF-8
    export LC_ALL=zh_CN.UTF-8
    cd /usr/WebApp   #进入到项目的根目录中
    gitDiffInfo=`git diff`   # 使用git diff 查看是否有修改,为空
    egreps="Already up-to-date.$"   #正则表达式，用于匹配拉取远程代码是否有更新
    gitDate=`date "+%Y-%m-%d %H-%M-%S"` # 获取当前的时间
    # 判断git diff 是否为空，（忽略）即服务器本地改动
    if [ -n "$gitDiffInfo" ];then
        echo "$gitDate" >> /usr/WebApp/script/pull.log
        echo "本地代码被已改动" >> /usr/WebApp/script/pull.log
    else
        # 如果输出为空，则执行git pull origin develop 命令
        gitPullInfo=`git pull origin master`
        # 判断代码是否有更新，通过正则匹配进行判断
        if [[ "$gitPullInfo" =~ $egreps ]];then
            # 以下三行代码是进行日志的写入
            echo "$gitDate" >> /usr/WebApp/script/pull.log
            echo "无代码更新" >> /usr/WebApp/script/pull.log
            echo -e "\n" >> /usr/WebApp/script/pull.log
        else
            # 以下三行代码时进行日志的写入  将pull的结果写入到日志中
            echo "$gitDate" >> /usr/WebApp/script/pull.log
            echo "$gitPullInfo" >> /usr/WebApp/script/pull.log
            echo -e "\n" >> /usr/WebApp/script/pull.log   # echo -e "\n" 输出三行回车
        fi
    fi
