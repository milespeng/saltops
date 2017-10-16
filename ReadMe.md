<div align="center">
  <img src="http://git.oschina.net/uploads/images/2017/0222/194334_0f219bc2_8819.png"><br><br>
</div>


# saltops



# 目标
SaltOps是一个基于SaltStack和Django开发的运维平台，
平台的主要功能包括：CMDB、包发布管理、工具系统、最终作为包发布和工具系统的接色
与Jenkins、Zabbix等系统进行整合

# 系统会具备什么功能

* CMDB：这个也是没办法的事情，资产信息还是要的。。而且Salt的Agent非常适合采集这些基础信息
最后，包发布的过程是需要用到CMDB信息的，所以CMDB是作为附属品存在的
* 工具平台：对主机进行批量的脚本执行
* 巡检任务：定时执行脚本，生成对应的巡检报告
* 包发布（搁置。。软件包发布的逻辑实在太复杂了，不同的应用很难标准化，还是Docker好。。）：程序包发布的功能，这块主要是用到salt的state.sls，通过编写好
sls文件，然后调用salt进行发布的动作，发布完后应用与主机的信息自然就对接起来了

# 文档

采用OSC Team里面提供的文档功能，传送门 http://saltops.mydoc.io/