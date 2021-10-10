# amap_district_polyline
查询高德-行政区域查询接口：
1、从行政单位100000开始查询围栏信息，及下一级行政单位；
2、轮询所查到的下一级单位的围栏信息及其下一级行政单位，直到结束；
3、存储各行政单位的围栏信息，以及行政单位的上下级关系；
4、参考接口：https://lbs.amap.com/api/webservice/guide/api/district
