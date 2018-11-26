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


import java.util.Scanner;

/**
 * 〈一句话功能简述〉<br> 
 * 〈〉
 *
 * @author java
 * @create 2018/11/18
 * @since 1.0.0
 */

class Person{
    private String idcard;
    private String name;
    private String age;
    private String gender;
    public Person(String idcard,String name, String age,String gender){
        this.idcard=idcard;
        this.name=name;
        this.age=age;
        this.gender=gender;
        System.out.println("idcard："+this.idcard+"name: "+this.name+"age: "+this.age+"gender: "+this.gender);
    }



}

public class fina {
    public static void main(String[] args) {

        System.out.println("请输入内容");
        Scanner sc = new Scanner(System.in);
        String str1 = sc.nextLine();
        String[] arr1 = str1.split("\\|");
        Person[] p = new Person[arr1.length];
        for(int i = 0;i<arr1.length;i++){
            String[] arr2 = arr1[i].split(":");
            p[i]=new Person(arr2[0],arr2[1],arr2[2],arr2[3]);

        }
        //"shxt_0712 shxt_0704 shxt_0715 shxt_0504 shxt_0602  shxt_0711 shxt_0607";

//        String[] st = str1.split(" ",90);
//
//        for(int i = 0;i<st.length;i++){
//            for(int j = 0;j<st.length-1;j++){
//                if(st[j].hashCode()>st[j+1].hashCode()){
//                    String a = st[j];
//                    String b = st[j+1];
//                    st[j] = b;
//                    st[j+1] = a;
//                }
//            }
//
//        }
//
//        for(int i = 0;i<st.length;i++){
//        System.out.println(st[i]);
//        }




    }


//        int begin = 0;
//        int endof = 0;
//        for(int i = 0;i<str1.length();i++){
//            if(str1.charAt(i) == ' '){
//                begin++;
//            }else{
//                break;
//            }
//        }
//        for(int i = str1.length()-1;i>=0;i--){
//            if(str1.charAt(i)==' '){
//                endof++;
//            }else {
//                break;
//            }
//        }
//
//        String newStr = str1.substring(begin,str1.length()-endof);
//        System.out.println(newStr);

//      if(str1.length()>2){
//          for(int i = 1;i<str1.length();i++){
//              System.out.println(str1.substring(i-1,i+1));
//          }
//      }else{
//          System.out.println(str1);
//      }

//    if(str1.length()>1){
//        //abcd
//        //ab
//        //bc
//        //cd
//        for(int i = 2;i<=str1.length();i+=1){
//            System.out.println(str1.substring(i-2,i));
//            String result = str1.charAt(i-2)==str1.charAt(i-1)?"相等":"不相等";//这个取值范围与上面的不是一个取值范围的原因是 这个是按照索引取值 上面是按照范围取值  例如 a.b a是0 b是1
//            System.out.println(result);
//
//        }
//    }else{
//        System.out.println(str1);
//    }
//
//    String str2 = "";
//    for(int i = 0;i<str1.length();i++){
//
//        if(str1.charAt(i)>=65 && str1.charAt(i)<=90){
//            str2 = str2+String.valueOf(str1.charAt(i)).toLowerCase();//获取的是char类型
//        }else if(str1.charAt(i)>=97 && str1.charAt(i)<=122){
//
//            str2 = str2+String.valueOf(str1.charAt(i)).toUpperCase();
//        }else{
//            str2 = str2+str1.charAt(i);
//        }
//    }
//    System.out.println(str2);


//        char[] str2 = str1.toCharArray();
//        int a = 0;
//        int b = 0;
//        for(int i = 0;i<str2.length;i++){
//            if(str2[i] ==' '){
//                a++;
//            }else{
//                break;
//            }
//        }
//        System.out.println(a);
//
//        while (str1.indexOf(" ",start) != -1){
//            start++;
//
//
//        }

//        int len = str1.length()-1;
//        for(int i = 0;i<str1.length();i++){
//            if(str1.indexOf("",i) == -1){
//                break;
//            }else{
//                System.out.println("i "+str1.indexOf(" ",i));
//                start++;
//            }
//        }
//        while (str1.lastIndexOf(" ",len) != -1){
//
//            //System.out.println(len);
//            end++;
//            len--;
//
//        }
//        System.out.println(start);


//        String s1 = "hello";
//        String s2 = "world";
//        String s3 = "helloworld";
//        System.out.println(s3==(s1+s2));
//        System.out.println(s3==("hello"+"world"));
//        String s4 = "zhangcun";
//        String s5 = "zhangcun";
//        System.out.println(s4==s5);
//        int[] arr1 = {1,2,3,4,5};
//        String st =  "liasdflihsdhllihsdflihsdfiligsdfglikhsdfklilisdflio";
//        String[] st1 = st.split("li");
//        System.out.println(st1.length-1);
//        getResult();
//        int[] arr2 = {6,7,8,9,10};
//        int[] arr3 = new int[arr1.length+arr2.length];
//        int j = 0;
//        for(int i =0;i<arr3.length;i++){
//            if(i<arr1.length){
//                arr3[i]=arr1[i];
//            }else{
//                arr3[i]=arr2[j++];
//            }
//        }
//
//        for(int i =0;i<arr3.length;i++){
//            System.out.println(arr3[i]);
//        }


//        int upper = 0;
//        int letter = 0;
//        int math = 0;
//        for(int i = 0;i<str1.length();i++){
//            char  st= str1.charAt(i);
//            if(st>=65 && st<=90){
//                upper++;
//            }else if(st>=97 && st<=122 ){
//                letter++;
//            }else if(st>= 48 && st<=57){
//                math++;
//            }
//        }

        //首字符大写 其余小写





    public static void getResult(){
        Scanner sc = new Scanner(System.in);
        while (true){
            System.out.println("请输入: ");
            String str1 = sc.next();
            try {
                //String strletter = str1.substring(1).toLowerCase();
                String strUpper = str1.substring(0,1).toUpperCase().concat(str1.substring(1).toLowerCase());
                //String strUpper = String.valueOf(charUpper).toUpperCase();
                //System.out.println(strUpper+strletter);
                System.out.println(strUpper);
                break;
            }catch (Exception e){
                System.out.println("请输入字符");
                continue;
            }
        }
    }
    public static int  finalReturn(int a,int b) throws Exception{
        int c = 0;
        return a/b;
//        try {
//            c = a/b;
//            System.out.println("C"+c);
//            return c;
//        }catch (Exception e){
//            System.out.println("*********************");
//            e.printStackTrace();
//            System.out.println("*********************");
//            c=b;
//            return c;
//        }finally {
//            System.out.println("finally最后被执行");
//            c = b;
//            //breturn c;
//
//        }

    }
}
