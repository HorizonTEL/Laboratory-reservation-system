# Laboratory-reservation-system
### 项目介绍
```
该项目是基于flask和bootstrap搭建的实验室预约系统，学生能够注册、登录、预约、取消预约以及签到。管理员可以查看学生的预约信息并且可以对未签到的预约信息进行删除
```

### 项目技术
* python
* flask
* HTML、CSS、bootstrap
* MySQL
* ...

### 功能展示
#### 一、登录注册
![image](https://user-images.githubusercontent.com/74846298/174249081-74ab8564-dabb-43b4-bd51-0d95dc18f47d.png)
![image](https://user-images.githubusercontent.com/74846298/174249109-7263815a-6348-419c-8520-1a39d03f806b.png)
#### 二、学生登录后
##### 1、首页
```
查看实验室情况，进行预约
```
![image](https://user-images.githubusercontent.com/74846298/174249324-f8069b93-860f-4d50-b4aa-a16f02eb8d5a.png)
![image](https://user-images.githubusercontent.com/74846298/174249357-af7c2314-9b9a-4558-954b-4996ede0f1cf.png)
![image](https://user-images.githubusercontent.com/74846298/174249393-5cd31b20-d44d-4f95-a5e3-b43b4726b4e3.png)
##### 2、个人中心
```
1、修改密码
2、签到
```
![image](https://user-images.githubusercontent.com/74846298/174249759-d5c2efe1-3f26-402b-a299-bc9988b298e0.png)
##### 3、搜索
```
1、搜索实现模糊匹配
2、搜索出的实验室，可以进行预约以及取消预约(已签到的不可取消预约)，如下展示的是输入 2 进行搜索
```
![image](https://user-images.githubusercontent.com/74846298/174250160-cc0ee936-1a9f-4d83-b4d1-205907179d36.png)
##### 4、帮助
![image](https://user-images.githubusercontent.com/74846298/174250436-0c255f90-5d48-4669-854e-ca7623add994.png)

#### 二、管理员登录后
##### 1、首页
```
1、查看学生的详细信息
2、点击某学生的信息进行查看后，可对学生的预约信息进行删除
```
![image](https://user-images.githubusercontent.com/74846298/174250733-52c6fcbf-c4ee-4e28-8005-8166a5c4ff47.png)
![image](https://user-images.githubusercontent.com/74846298/174250806-24e20a31-149f-4d8d-b61f-0339d0a5570b.png)

### 项目启动
#### 1、需要修改的内容
```
venv.zip放置的是该项目启动需要的所有配置项，如果使用其中的package，解压到当前文件夹，并将其设为该项目的虚拟环境
```
#### 2、打开app.py文件，并运行此文件
#### 3、在浏览器里输入127.0.0.1:5000/index即可运行
