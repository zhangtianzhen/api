/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: ObjectDemo2
 * Author:   java
 * Date:     2018/11/18 12:10
 * Description:
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package com.test.dao;

/**
 * 〈一句话功能简述〉<br> 
 * 〈〉
 *
 * @author java
 * @create 2018/11/18
 * @since 1.0.0
 */
/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: Student
 * Author:   java
 * Date:     2018/11/18 12:09
 * Description:
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */


/**
 * 〈一句话功能简述〉<br>
 * 〈〉
 *
 * @author java
 * @create 2018/11/18
 * @since 1.0.0
 */
//java.lang.Object��Ĭ�ϱ�ÿһ����̳е�
class Student{
    private String name;
    private int age;
    private String gender;

    public Student(){
        super();
    }

    public void setName(String name){
        this.name = name;

    }
    public String getName(){
        return name;

    }

    public void setAge(int age){
        this.age = age;

    }
    public int getAge(){
        return age;

    }

    public void setGender(String gender){
        this.gender = gender;

    }
    public String getGender(){
        return gender;

    }
    /**
     * ��дObject��equals�������ж����������Ƿ����
     */

    public boolean equals(Object obj){
        boolean result = false;
        //�ж�Object��ʵ���������Ƿ���Student
        if(obj instanceof Student){
            Student s2 = (Student) obj;
            if(this.name.equals(s2.getName())&&(this.age == s2.getAge())&&(this.gender == s2.getGender())){
                result = true;
            }
        }
        return result;
    }

    /**
     * ����дequals����ʱ���Ҳ��дhashCode
     */
    public int hashCode(){
        return 1;
    }

}

class ObjectDemo2{
    public static void main(String[] args){
        Student s = new Student();
        Student s1 = new Student();
        //ֱ�Ӵ�ӡ����ʱ��Ĭ���ڵ��ôӸ���̳�������toString
        System.out.println(s);
        System.out.println(s1);
        /**�ж϶����Ƿ���Ȳ���ʹ��"==",��Ϊ"=="���жϵ���������ĵ�ַ,
         *����������Զ�������
         */
        System.out.println(s == s1);

        //�ж����������Ƿ����һ��ʹ��equals����
        //boolean isEquals = s.equals(s1);
        //System.out.println(isEquals);
        System.out.println("-------------");

        s.setName("����");
        s.setAge(10);
        s.setGender("��");

        s1.setName("����");
        s1.setAge(10);
        s1.setGender("��");
        System.out.println("ѧ��s��ѧ��s1��ַ�Ƿ����:"+s.equals(s1));

    }

}