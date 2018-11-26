/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: admin
 * Author:   java
 * Date:     2018/11/17 14:55
 * Description: 管理员登录
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package com.admin;

import java.time.Year;
import java.util.Scanner;

/**
 * 〈一句话功能简述〉<br> 
 * 〈管理员登录〉
 *
 * @author java
 * @create 2018/11/17
 * @since 1.0.0
 */
interface Do{
    public void login();
    public void register();
    public void deleted();
    public void show();
}

public class admin implements Do  {
    Scanner sc1 = new Scanner(System.in);
    public static int id;
    private  static String[][] account = new String[10][2];
    public  void login(){
        if(id !=0){
            System.out.println("请输入账号");
            String count = sc1.next();

            while (true){
                System.out.println("请输入密码");
                String password = sc1.next();
                boolean flag = false;
                for(int i = 0; i<id;i++){
                    if(account[i][0].equals(count) ){
                        if(account[i][1].equals(password) ){
                            System.out.println("登录成功");
                            flag = true;
                        }else{
                            System.out.println("密码错误是否继续登录 Y/N or y/n");
                            String result = sc1.next();
                            boolean res = "Y".equals(result) ||"y".equals(result)?false:true;
                            flag=res;
                        }
                    }else{
                        System.out.println("账号未注册");
                    }
                }
                if(flag){break;}
            }
        }else {
            System.out.println("还没有账号,请先注册 输入'是'跳转到注册页面");
            String input = sc1.next();
            boolean ret = "是".equals(input)?true:false;
            if(ret){
                this.register();
            }

        }

    }

    public  void register(){
        boolean ret = false;

        while(true){
            boolean flag = false;
            System.out.println("请输入账号");
            String count = sc1.next();
            for(int i =0; i<id;i++){
                if(account[i][0].equals(count)){
                    flag = true;
                    System.out.println("账号已存在,请重新输入");
                    break;
                }
            }
            if(flag){
                continue;
            }else{
                System.out.println("count:"+count);
                account[id][0] = count;
                ret = true;
                break; }
        }
        if(ret ){

            System.out.println("请输入密码");
            String password = sc1.next();
            account[id][1] = password;
            id++;
            System.out.println("注册成功");
        }
    }
    public void show(){
        System.out.println("账号\t\t\t 密码");
        for(int i = 0;i<id;i++){
                System.out.println(account[i][0]+"\t\t"+account[i][1]);
        }
    }
    public void deleted(){
        this.show();
        System.out.println("请输入要删除的账号");
        String ccount = sc1.next();
        for(int i = 0;i<id;i++){
            if(account[i][0].equals(ccount)){
                account[i][0] = null;
                account[i][1] = null;
            }else {System.out.println("无此账号");}
        }
    }

}
