/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: strbf
 * Author:   java
 * Date:     2018/11/20 23:01
 * Description:
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package com.buffer.cn;

import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * 〈一句话功能简述〉<br> 
 * 〈〉
 *
 * @author java
 * @create 2018/11/20
 * @since 1.0.0
 */
public class strbf {

    private Integer id;
    public strbf(Integer id) {
        this.id = id;
    }
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public strbf() {
    }



    @Override
    public String toString() {
        return "strbf{" +
                "id=" + id +
                '}';
    }

    public static void main(String[] args) throws Exception{
        int a = 128;
        byte b = (byte)a;
        System.out.println(b);
        //思路 通过第三方integer 进行转类型
        //int ---> integer 通过构造器
        //Integer st1 = Integer.valueOf("20");
       // int st2 = st1.intValue();
        //System.out.println(st2);
        //System.out.println(Integer.parseInt("20"));
//        Integer i = 10;
//        int is = i;
//        System.out.println(is);

//        String s1 = "mnanm";
//        StringBuffer s2 = new StringBuffer(s1);
//        String s3 = String.valueOf(s2.reverse());
//
//        if(s1.equals(s3)){
//            System.out.println("翻转");
//        }
        //91 27 46 38 50
//        String s = "91 27 46 38 50";
//        String[] s2 = s.split(" ");
//        StringBuffer s3 = new StringBuffer();
//        for(int i = 0;i<s2.length;i++){
//            for(int j = 1;j<s2.length;j++){
//                if(Integer.parseInt(s2[j])<Integer.parseInt(s2[j-1])){
//                    String a = s2[j];
//                    String b = s2[j-1];
//                    s2[j] = b;
//                    s2[j-1]=a;
//                }
//            }
//        }
//        for(int i =0;i<s2.length;i++){
//            System.out.println(s2[i]);
//        }
//
//    }
//    public static void random(){
//        Random r = new Random(10l);
//        for(int i = 0;i<10;i++){
//            System.out.println(r.nextInt(100));
//        }
//
//        String s1 = "jdk";
//        System.out.println(s1.toUpperCase().substring(1));
//        String s2 = "113@ ere qqq yyui";
//        String s4 = s2.replace("@","");
//        String[] s3 = s4.split(" ");
//
//        for(int i = 0;i<s3.length;i++){
//            System.out.println(s3[i]);
//        }
        //To be or not to be
//        String sg = "To be or not to be";
//        String[] sg1 =sg.split(" ");
//        StringBuffer sg2 = new StringBuffer();
//        for(int i = 0;i<sg1.length;i++){
//            StringBuffer s = new StringBuffer(sg1[i]);
//            sg2.append(s.reverse()+" ");
//        }
//        System.out.println(sg2);
//        String s="name=zhangsan age=18 classNo=090728";
//        String[] s1 = s.split(" ");
//        StringBuffer sss = new StringBuffer();
//        for(int i = 0;i<s1.length;i+=1){
//            String[] s2 = s1[i].split("="); //二次切割
//            sss.append(s2[1]+" ");
//
//        }
//        System.out.println(sss);

        String str = "1991-11-01";
        SimpleDateFormat sdf = new SimpleDateFormat("YYYY-MM-dd");
        Date d1 = sdf.parse(str);
        Date d = new Date();
        System.out.println();



    }


}
