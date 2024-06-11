# DoodleAnimation

#### 介绍
毕设项目存档，更改自meta的Animated Drawings项目，本项目主要应用了该模型将客户端输入的涂鸦图片转化为Unity3D场景中可动的涂鸦动画，作为服务端功能。

客户端代码见仓库( https://gitee.com/zhang-xinmu/sketch )。

#### 安装教程

1.  参考doc文件夹中的README文件，安装必要的库
2.  参考个人经验，可不使用docker直接部署，windows环境与linux部署方式类似，仅需要将docker中的linux指令改为windows cmd指令即可

#### 使用说明

1.  打开torchserve服务器：在项目进入torchserve目录后打开cmd指令行，输入`torchserve --start --ts-config config.properties`
2.  若使用游戏客户端接收结果，则进入examples目录后运行server.py文件即可
3.  若直接项目内测试结果，则进入examples目录后打开cmd指令行，使用指令运行脚本`python image_to_animation.py [你的输入图片] [你的输出文件夹]`

