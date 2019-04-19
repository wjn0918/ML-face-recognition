人脸检测
===
【需求】
-----
传入一张人像，对比底库数据，查看是否有该人


【思路】
------
1、定时将mysql数据库中的图像进行特征提取，并将提取特征与人员信息关联
2、将特征数据存入redis数据库中
3、对传入的人像进行特征提取
4、对比传入人像与底库中的人像相似度，按照预设阀值返回相似度接近的人员信息
