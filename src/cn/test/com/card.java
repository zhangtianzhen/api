/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: card
 * Author:   java
 * Date:     2018/11/26 17:49
 * Description:
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package cn.test.com;

import java.util.ArrayList;
import java.util.Scanner;
import java.util.List;
/**
 * 〈一句话功能简述〉<br> 
 * 〈〉
 *
 * @author java
 * @create 2018/11/26
 * @since 1.0.0
 */
public class card {
    private static int appendID;
    private String name;//车名
    private double price;//价格
    private String num;//牌号
    private String info;//描述信息
    private String color;//颜色
    Scanner sc = new Scanner(System.in);
    private static List lists = new ArrayList();
    public String getName() {
        return name;
    }
    public void setName() {
        System.out.println("请输入车名");
        String name = sc.next();
        this.name = name;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice() {
        while (true){
            try {
                System.out.println("请输入价格");
                double price = sc.nextDouble();
                this.price = price;
                break;
            }catch (Exception e){
                e.printStackTrace();
                System.out.println("请输入数字");
                System.out.println("是否继续输入 yes/no");
                String getUser = sc.next();
                if("yes".equals(getUser)){
                    continue;
                }else{
                    break;
                }
            }
        }


    }

    public String getNum() {
        return num;
    }

    public void setNum() {
        System.out.println("请输入牌照");
        String num = sc.next();
        this.num = num;
    }

    public String getInfo() {
        return info;
    }

    public void setInfo() {
        System.out.println("请输入描述信息");
        String info = sc.next();
        this.info = info;
    }

    public String getColor() {
        return color;
    }

    public void setColor() {
        System.out.println("请输入颜色");
        String color = sc.next();
        this.color = color;
    }

    @Override
    public String toString() {

        return "card{" +
                "汽车名称='" + name + '\'' +
                ", 价格=" + price +
                ", 车牌号=" + num +
                ", 车辆信息='" + info + '\'' +
                ", 颜色='" + color + '\'' +
                '}';

    }
    public static void  setList(Object obj){
        card.lists.add(obj);
    }
    public static List getList(){
        return card.lists;
    }
    public static void setAppendID(){
        appendID++;
    }
    public static void show(){
        int length = card.getList().size();
        if(length == 0){
            System.out.println("暂无车辆信息 请先添加车辆");
        }
        for(int  i = 0;i<length;i++){
            System.out.print("序号: "+i+"\t");
            System.out.println(card.getList().get(i));
        }
    }
}
