/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: ExpectionDemo
 * Author:   java
 * Date:     2018/11/18 15:09
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



public class ExpectionDemo {
    public static void main(String[] args){
        int a = 10;
        int b = 2;
        int c= 0;
        int[] arr1 = {1,2,3,4};
        try {
            c = a/b;
            System.out.println(arr1[4]);
        }catch (ArithmeticException e){
            e.printStackTrace();
            System.out.println("调用者处理了一个异常");
        }catch (IndexOutOfBoundsException e){
            System.out.println("^^^^^^^^^^^");
            e.printStackTrace();
        }
        System.out.println(c);
        System.out.println("-----------");
    }


}
