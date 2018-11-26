/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: exception
 * Author:   java
 * Date:     2018/11/18 16:15
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
public class exception {
    public static void main(String[] args){
        int a = 10;
        int b = 2;
        int c= 0;
        int[] arr1 = {1,2,3,4};
        try {
            c = a/b;
            System.out.println(arr1[4]);
        }catch (Exception e){
            System.out.println("*********************");
            if(e instanceof ArithmeticException ){
                System.out.println("处理数学异常");
            }else{
                System.out.println("处理数组异常");
            }
            e.printStackTrace();

        }
        System.out.println(c);
    }
}
