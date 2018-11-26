/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: Platform
 * Author:   java
 * Date:     2018/11/26 18:11
 * Description:
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package cn.test.com;
import java.util.*;
/**
 * 〈一句话功能简述〉<br> 
 * 〈〉
 *
 * @author java
 * @create 2018/11/26
 * @since 1.0.0
 */
public class Platform {

    public static Scanner sc = new Scanner(System.in);
    public static List list1 = new ArrayList();
    public static void main(String[] args){
        Platform.Exe();
    }
    public static void Exe(){
        Platform.Test();
    }
    public static void Test(){
        System.out.println("---欢迎来到汽车之家租赁系统---");
        boolean flag = true;
        try {
            while (flag){
                System.out.println("1.管理员      2.用户      3.退出");
                String get = sc.nextLine();
                if(get == " " || get == null || get == ""){continue;}
                int select = Integer.parseInt(get);
                if(select == 3){
                    flag = false;
                }else{
                    switch (select){
                        case 1:
                            Platform.Admins();
                            break;
                        case 2:
                            Platform.Customer();
                            break;
                        default:
                            System.out.println("开发中 暂无此选项");
                    }
                }
            }

        }catch (Exception e){
            e.printStackTrace();
            Platform.Exe();
        }
    }

    public static void Admins(){
        System.out.println("----管理员后台------");
        Admin ad = new Admin();

        while (true){
            System.out.println("1.添加新车   2.编辑车辆信息   3.查询车辆信息   4.删除车辆  5.显示所有车辆   6.退出 ");
            try {
                String s = sc.nextLine();
                if(s == null || s == " "||s==""){continue;}
                Integer select = Integer.parseInt(s);
                if(select == 6){
                    break;
                }else {
                    switch (select){
                        case 1:
                            ad.Add();
                            ad.show();break;
                        case 2:
                            ad.Edit();break;
                        case 3:
                            ad.Query();break;
                        case 4:
                            ad.Delet();
                            break;
                        case 5:
                            ad.show();
                            break;
                        default:
                            System.out.println("开发中  暂无此选项");
                            break;
                    }
                }
            }catch (Exception e){
                e.printStackTrace();
                System.out.println("请输入数字");
            }
        }
    }
    public static void Customer(){
        System.out.println("------用户使用平台----------");

        while (true){
            System.out.println("1.租车    2.用户信息    3.退出");
            try {
                System.out.println("请输入选项");
                String s= sc.next();
                if(s == null || s == " "||s==""){continue;}
                int n = Integer.parseInt(s);
                if(n == 3){
                    break;
                }
                switch (n){
                    case 1:
                        Platform.addUser();
                        break;
                    case 2:
                        Platform.allUser();
                        System.out.println();
                        break;
                    default:
                        System.out.println("开发中  暂无此选项");
                        break;
                }

            }catch (Exception e){
                e.printStackTrace();
                System.out.println("请在用户使用平台重新输入");
            }

        }

    }

    public static void addUser(){
        card.show();
        User user = new User();
        user.setId();
        user.setRmb();
        user.setPhoneNum();
        user.setAddr();
        user.setDay();
        user.setDriveId();
        user.setNum();
        Platform.list1.add(user);
        System.out.println("添加用户成功");
    }
    public static void allUser(){
        for(Object s:list1){
            System.out.println(s);
        }
    }
}
