/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: Play
 * Author:   java
 * Date:     2018/11/18 14:07
 * Description:
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package com.play.dao;

/**
 * 〈一句话功能简述〉<br> 
 * 〈〉
 *
 * @author java
 * @create 2018/11/18
 * @since 1.0.0
 */

abstract  class Aniaml{
    int Healths=100;
    int Intimacys=0;
    public abstract void health();
    public abstract void Intimacy();
}
class Dog extends Aniaml{
    public void health(){
        this.Healths-=10;
        System.out.println("狗狗减少10个健康值");

    }
    public void Intimacy(){
        this.Intimacys+=5;
        System.out.println("狗狗增加5个亲密值");
    }

}
class Penguin extends Aniaml{
    public void health(){
        this.Healths-=10;
        System.out.println("企鹅减少10个健康值");
    }
    public void Intimacy(){
        this.Intimacys+=5;
        System.out.println("企鹅增加5个亲密值");
    }
}

class Person{
    public void play(Aniaml obj){
        obj.Intimacy();
        obj.health();
    }
}
public class Play {
    public static void main(String[] args){
        Aniaml dog = new Dog();
        Aniaml penguin = new Penguin();
        Person person = new Person();
        person.play(dog);
        person.play(penguin);
    }


}
