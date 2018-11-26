/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: student
 * Author:   java
 * Date:     2018/11/16 20:20
 * Description: 学生管理系统
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package com.student.model;
import java.util.Scanner;

import com.admin.*;
import com.admin.AnimalTest;
import com.car.dao.*;
import com.pet.dao.*;
/**
 * 〈一句话功能简述〉<br> 
 * 〈学生管理系统〉
 *
 * @author java
 * @create 2018/11/16
 * @since 1.0.0
 */

interface Operation{
//    public void add();
    public void show();
    public void delete();
    public void edit();
    public void query();
}
class student implements Operation{
    String[][] studentArray = new String[100][8];
    Scanner sc = new Scanner(System.in);
    private int id=0;


    public void add(String name,String snumber,String gender,String Department,String addr,String Score,String email,String phoneNumber){
        boolean flag = true;
        for(int i = 0;i<studentArray.length;i++){
            if(studentArray[i][1] == snumber) {
                flag = false;
                break; }
        }
        if(flag){
            studentArray[this.id][0]=name;
            studentArray[this.id][1]=snumber;
            studentArray[this.id][2]=gender;
            studentArray[this.id][3]=Department;
            studentArray[this.id][4]=addr;
            studentArray[this.id][5]=Score;
            studentArray[this.id][6]=email;
            studentArray[this.id][7]=phoneNumber;
            this.id++;
        }else{
            System.out.println("该学生已存在无法继续添加");
        }

    }
    public void show(){
        System.out.println("id\t\t姓名\t\t学号\t\t性别\t\t院系\t\t户籍\t\t学分\t\t邮箱\t\t联系方式");
        for(int i = 0;i<this.id;i++){
            if(studentArray[i][0] != null){System.out.print(i+"\t\t");}
            for(int j = 0;j<studentArray[i].length;j++){
                if(studentArray[i][j] != null){
                    System.out.print(studentArray[i][j]+"\t\t");
                }
            }
            System.out.println();
        }
    }
    public void delete(){ //删除
        System.out.println("请输入id");
        int id = sc.nextInt();

        if(id>this.id){
            System.out.println("超过可选id范围");
        }else{
            for(int i = 0;i<8;i++){
                studentArray[id][i] = null;
            }
        }
        
    }
    public void edit(){

        this.show();
        System.out.println("请输入要编辑的用户id");
        int id = sc.nextInt();
        if(id>this.id ||studentArray[id][0] == null ){
            System.out.println("用户不存在,查询结束！");
        }else if (studentArray[id][0] != null){
            System.out.println("选项0 修改用户姓名 选项1 修改学号,选项2 修改性别 选项3修改院系");
            System.out.println("选项4 修改地址,选项5 修改学分,选项6 修改邮箱地址 选项7 修改电话号码 选项8 退出修改");

            while(true){

                System.out.println("请输入选项");
                int input = sc.nextInt();//匹配输入的内容
//
//                boolean result =input > 7 ? true:false;
//                if(result){break;}
                if (input > 7){ break; }
                System.out.println("请输入内容");
                String text = sc.next();
                switch (input){
                    case 0:
                        studentArray[id][input]=text;
                        break;
                    case 1:
                        studentArray[id][input]=text;
                        break;
                    case 2:
                        studentArray[id][input]=text;
                        break;
                    case 3:
                        studentArray[id][input]=text;
                        break;
                    case 4:
                        studentArray[id][input]=text;
                        break;
                    case 5:
                        studentArray[id][input]=text;
                        break;
                    case 6:
                        studentArray[id][input]=text;
                        break;
                    case 7:
                        studentArray[id][input]=text;
                        break;
                }


            }

        }

    }
    public  void  query(){
        System.out.println("选项:0 根据姓名查找   选项:1 根据学号查找   选项:2  根据性别查找   选项:3  根据院系查找");
        System.out.println("选项:4 根据户籍查找  选项:5 根据学分查找   选项:6 根据邮箱查找   选项:7  根据联系方式查找   选项:8  退出查询");

                while (true){
                    System.out.println("请输入选项: ");
                    int index = sc.nextInt();
                    if(index >= 9 || index < 0){
                        System.out.println("请重新输入查找方式");
                        continue;
                    }else if(index == 8){
                break;
            }
            System.out.println("请输入内容");
            String text = sc.next();
            for(int i = 0;i<this.id;i++){
                if(studentArray[i][index].equals(text)){
                    System.out.println(studentArray[i][0]); }
            }
        }
    }

    public static void main(String[] args){
        admin manage = new admin();
       // manage.register();
//        manage.login();
//        manage.show();
//        manage.register();
//        manage.show();
//        student s = new student();
//
//        s.add("张三","123456","男","计算机科学与技术","安徽省","720","1282965023@qq.com","18726099229");
//
//        s.add("李四","1234562561","男","计算机科学与技术","安徽省","720","1282965023@qq.com","18726099229");
//        s.show();
//        s.delete();
//        s.show();
//
//        s.edit();
//        s.show();
//        s.query();
       AnimalTest.Obj();
       TestCar.test();
       Test.testMain();
    }

}
