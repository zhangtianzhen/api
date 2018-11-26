/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: StockExpection
 * Author:   java
 * Date:     2018/11/18 17:10
 * Description:
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package com.expection.cn;

/**
 * 〈一句话功能简述〉<br> 
 * 〈〉
 *
 * @author java
 * @create 2018/11/18
 * @since 1.0.0
 */

class expections{
    public expections(){
        System.out.println("自定义1");
    }
    public expections(String a){
        System.out.println(a+"这是父类抛出的");
    }
    public expections(String a,String b){
        this(a);
        System.out.println(b+"这是父类抛出的");
    }
}
public class StockExpection extends expections  {

    public StockExpection(){

    }
    public StockExpection(String a){
        super(a);
    }
    public StockExpection(String a,String b) {
        super(a,b);
    }

}
