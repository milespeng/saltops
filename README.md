#saltops

# [系统开发中～请不要用于生产系统] 


#目标
SaltOps是一个基于SaltStack和Django开发的运维平台，
平台的主要功能包括：CMDB、包发布管理、工具系统、最终作为包发布和工具系统的接色
与Jenkins、Zabbix等系统进行整合

#系统会具备什么功能

* CMDB：这个也是没办法的事情，资产信息还是要的。。而且Salt的Agent非常适合采集这些基础信息
最后，包发布的过程是需要用到CMDB信息的，所以CMDB是作为附属品存在的
* 包发布：程序包发布的功能，这块主要是用到salt的state.sls，通过编写好
sls文件，然后调用salt进行发布的动作，发布完后应用与主机的信息自然就对接起来了
* 工具平台：既然都接上了Salt，把工具平台做了也是很自然的事情啦～

#为什么使用DjangoAdmin
DjangoAdmin大多作为后台管理员使用的，这里用DjangoAdmin的原因是：没资源。。且每天写的时间也有限，用它的话大多数界面都不用自己做，还是挺省事的
配合着Django-jet的话也长得还不错

# 文档

- [SaltOps的定位与目标](doc/wiki/SaltOps的定位与目标.md)
- [架构概览](https://git.oschina.net/wuwenhao/saltops/blob/master/doc/wiki/架构概览.md)
- [安装前准备](https://git.oschina.net/wuwenhao/saltops/blob/master/doc/wiki/安装前准备.md)
- [集中部署](https://git.oschina.net/wuwenhao/saltops/blob/master/doc/wiki/集中部署.md)
- [分离部署](https://git.oschina.net/wuwenhao/saltops/blob/master/doc/wiki/分离部署.md)
- [功能简介:首页](https://git.oschina.net/wuwenhao/saltops/blob/master/doc/wiki/首页.md)
- [功能简介:资产管理](https://git.oschina.net/wuwenhao/saltops/blob/master/doc/wiki/资产管理.md)
- [功能简介:发布管理](https://git.oschina.net/wuwenhao/saltops/wikis/%E5%8F%91%E5%B8%83%E7%AE%A1%E7%90%86)
- [对外接口]
- [系统配置与可用参数列表]
- [常见问题](https://git.oschina.net/wuwenhao/saltops/wikis/%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98)

#常用部署模板

- [JDK](https://git.oschina.net/wuwenhao/saltops/blob/master/doc/sls/jdk8.sls)
- [ElasticSearch](https://git.oschina.net/wuwenhao/saltops/blob/master/doc/sls/elasticsearch-master.sls)