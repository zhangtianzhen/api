/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: AnimalTest
 * Author:   java
 * Date:     2018/11/17 19:35
 * Description: 测试类
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package com.admin;

/**
 * 〈一句话功能简述〉<br> 
 * 〈测试类〉
 *
 * @author java
 * @create 2018/11/17
 * @since 1.0.0
 */

interface Animal{

    public abstract void eat();
}

class  Lion implements Animal{
    public void eat(){
        System.out.println("狮子正在进食");
    }
}

class Peigon implements Animal{
    public void eat(){
        System.out.println("鸽子正在进食");
    }
}

class monkey implements  Animal{
    public void eat(){
        System.out.println("猴子正在进食");
    }

}

class Person{
    public void Feeding(Animal[] obj){
        for(int i = 0;i<obj.length;i++){
            obj[i].eat();
        }
    }
}
public class AnimalTest {
    public static void Obj(){
        Animal[] anim = {new Peigon(),new Lion(),new monkey()};
        Person p = new Person();
        p.Feeding(anim);


    }
}
