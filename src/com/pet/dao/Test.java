/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: Test
 * Author:   java
 * Date:     2018/11/17 21:34
 * Description: 测试类
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package com.pet.dao;
import java.util.Scanner;
/**
 * 〈一句话功能简述〉<br> 
 * 〈测试类〉
 *
 * @author java
 * @create 2018/11/17
 * @since 1.0.0
 */
interface Animal{
    public void setName(String name);
    public void setPrice(double price);
}

class Dog implements Animal{
    private String name;
    private double price;
    public Dog(){

    }
    public Dog(String name,double price){
        this.name = name;
        this.price = price;
    }
    public void setName(String name){
        this.name = name;
    }
    public String getName(){
        return this.name;
    }
    public void setPrice(double price){
        this.price = price;
    }
    public double getPrice(){
        return this.price;
    }


}

class Cat implements Animal{
    private String name;
    private double price;
    public Cat(){

    }
    public Cat(String name,double price){
        this.name = name;
        this.price = price;
    }
    public void setName(String name){
        this.name = name;
    }
    public String getName(){
        return this.name;
    }
    public void setPrice(double price){
        this.price = price;
    }
    public double getPrice(){
        return this.price;
    }
}

class Shop{

    Scanner sc = new Scanner(System.in);
    Animal[] obj = {new Dog("柴犬1",200),new Dog("柴犬2",200),new Dog("柴犬3",200),new Dog("柴犬4",200),
    new Cat("橘猫1",140),new Cat("橘猫2",140),new Cat("橘猫3",140),new Cat("橘猫4",140)};

    public void show(){
        int id=0;
        for(int i = 0;i<obj.length;i++){

            System.out.print(id+" ");
            if(obj[i] instanceof Dog){
                Dog d = (Dog)obj[i];
                System.out.println("名称:"+d.getName()+"价格:"+d.getPrice());
            }else{
                Cat cart = (Cat)obj[i];
                System.out.println("名称:"+cart.getName()+"价格:"+cart.getPrice());
            }
            id++;
        }
    }

    public void buy(Person person){
        while (true){
            System.out.println("请输入你要购买的宠物的序号: ");
            int index = sc.nextInt();
            boolean ret = index>=this.obj.length?true:false;
            if(ret){
                System.out.println("超过列表序号 请重新输入 或退出选择 q/Q退出 N/n继续选择");
                String input = sc.next();
                boolean get = "q".equals(input) || "Q".equals(input)?true:false;
                if(get){
                    break;
                }
                continue;
            }else {
                int flag = obj[index] instanceof Cat?1:2;
                switch (flag){
                    case 1:
                        Cat cat = (Cat) obj[index];//向下转型为子类
                        if("已售".equals(cat.getName())){
                            System.out.println("已售出 无法购买");
                        }else if(person.getPrice() > cat.getPrice()){
                            person.setShopList(cat.getName());
                            person.subPrice(cat.getPrice());
                            System.out.println("购买成功");
                            cat.setName("已售");


                        }else {
                            System.out.println("余额不足");
                        }
                        break;
                    case 2:
                        Dog dog = (Dog) obj[index];//向下转型为子类
                        if("已售".equals(dog.getName())){
                            System.out.println("已售出 无法购买");
                        }else if(person.getPrice()>dog.getPrice()){
                            person.setShopList(dog.getName());
                            person.subPrice(dog.getPrice());
                            System.out.println("购买成功");
                            dog.setName("已售");
                        }else{
                            System.out.println("余额不足");
                        }
                        break;
                }
//                if(obj[index] instanceof Cat){
//                    Cat cat = (Cat) obj[index];
//                    if(person.getPrice()>=cat.getPrice()){
//                        if("已售".equals(cat.getName())){
//                            System.out.println("已售出 无法购买");
//                        }else{
//                            System.out.println("购买成功");
//                            cat.setName("已售");
//                            cat.setPrice(0);
//                        }
//                    }else {System.out.println("余额不足");}
//                }else if(obj[index] instanceof Dog){
//                    Dog dog = (Dog) obj[index];
//                    if(person.getPrice()>=dog.getPrice()){
//                        if("已售".equals(dog.getName())){
//                            System.out.println("已售出 无法购买");
//                        }else{
//                            System.out.println("购买成功");
//                            dog.setName("已售");
//                            dog.setPrice(0);
//                        }
//                    }else {System.out.println("余额不足");}
//
//                }
            }
            this.show();
            System.out.println("余额:"+person.getPrice());
            System.out.println("购物清单:---------");
            person.getShopList();
        }



    }


}
class Person{
    private static  int add;
    private double price;
    String[] shopList = new String[100];
    public Person(double price){
        this.price = price;
    }
    public void setPrice(double price){
        this.price = price;
    }
    public  double getPrice(){

        return this.price;
    }
    public void subPrice(double price){
        this.price -= price;
    }
    public void setShopList(String pet){
        shopList[add] = pet;
        add++;
    }
    public void getShopList(){
        for (int i = 0;i<add;i++){
            System.out.print(i+"\t");
            System.out.println(shopList[i]);
        }
    }
}

public class Test {
    public static void testMain(){
        Shop shop  = new Shop();
        Person person = new Person(2000);
        shop.show();
        shop.buy(person);

    }
}
