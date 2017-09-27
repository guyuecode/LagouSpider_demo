# LagouSpider_demo
简单爬取拉勾招聘职位信息的python爬虫。仅个人学习使用，请勿喷。

需要提前在数据库中建库和表。

create database sql:
create database LagouSpider;

create table sql:
create table search_python_result_list (id varchar(20) primary key, JobTitle varchar(40), salary varchar(20), education varchar(20), companyFullName varchar(20));

效果如下:
![image](http://owxnojsso.bkt.gdipper.com/2017-09-27%2017-25-19%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE.png)
