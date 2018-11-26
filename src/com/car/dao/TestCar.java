/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: TestCar
 * Author:   java
 * Date:     2018/11/17 20:05
 * Description: java题目
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package com.car.dao;

/**
 * 〈一句话功能简述〉<br> 
 * 〈java题目〉
 *
 * @author java
 * @create 2018/11/17
 * @since 1.0.0
 */

interface Car{
    public int getNo();
    public String getName();
    public double getPrice();
    public void show();
}

interface Busload{
    public int getbusload();//载客量

}

interface Boatload{ //载货量
    public double getboatload();
}
class Bus implements Car,Busload{
    int no;
    String name;
    double price;
    int load; //载客量
    public Bus(int no,String name,double price,int load){
        this.no = no;
        this.name = name;
        this.price = price;
        this.load = load;
    }
    public void  setNo(int no){
        this.no = no;
    }
    public void setName(String name){
        this.name = name;
    }
    public void setPrice(double price){
        this.price = price;
    }
    public void setLoad(int load){
        this.load = load;
    }
    public int getNo(){
        return this.no;
    }
    public String getName(){
        return this.name;
    }
    public double getPrice(){
        return this.price;
    }
    public int getbusload(){
        return this.load;
    }
    public void show(){
        System.out.println("编号: "+this.getNo()+"名称: "+this.getName()+"租金: "+this.getPrice()+"载客量:"+this.getbusload());

    }
}
class Truck implements Car,Boatload{
    int no;
    String name;
    double price;
    double load;//载货量
    public Truck(int no,String name,double price,double load){
        this.no = no;
        this.name = name;
        this.price = price;
        this.load = load;

    }
    public void  setNo(int no){
        this.no = no;
    }
    public void setName(String name){
        this.name = name;
    }
    public void setPrice(double price){
        this.price = price;
    }
    public void setLoad(double load){
        this.load = load;
    }
    public int getNo(){
        return this.no;
    }
    public String getName(){
        return this.name;
    }
    public double getPrice(){
        return this.price;
    }
    public double getboatload(){
        return this.load;
    }
    public void show(){
        System.out.println("编号: "+this.getNo()+"名称: "+this.getName()+"租金: "+this.getPrice()+"载货量: "+this.getboatload());

    }
}


class Pickup implements Car,Boatload,Busload{
    int no;
    String name;
    double price;
    double load;//载货量
    int load1;//载客量
    public Pickup(int no,String name,double price,double load,int load1){
        this.no = no;
        this.name = name;
        this.price = price;
        this.load = load;
        this.load1 = load1;
    }
    public void setNo(int no){
        this.no = no;
    }
    public void setName(String name){
        this.name = name;
    }
    public void setPrice(double price){
        this.price = price;
    }
    public  void  setLoad(double load){
        this.load=load;
    }
    public void setLoad1(int load){
        this.load = load;
    }
    public int getNo(){
        return this.no;
    }
    public String getName(){
        return this.name;
    }
    public double getPrice(){
        return this.price;
    }
    public double getboatload(){
        return this.load;
    }
    public int getbusload(){
        return this.load1;
    }
    public void show(){
        System.out.println("编号: "+this.getNo()+"名称: "+this.getName()+"租金: "+this.getPrice()+"载货量: "+this.getboatload()+"载客量:"+this.getbusload());

    }
}


class CarShow{
    public void shows(Car[] car){
        for(int i = 0;i<car.length;i++){
            car[i].show();
        }

    }
}
public class TestCar {
    public static void test(){
        Car[] car = {new Bus(110,"金龙鱼客车",17700.0,30),new Truck(120,"一汽重卡",47231.0,55.5),
        new Pickup(119,"德国皮卡",512111.0,9.1,6)};
        CarShow csh = new CarShow();
        csh.shows(car);
    }
}
