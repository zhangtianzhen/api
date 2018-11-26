/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: Student
 * Author:   java
 * Date:     2018/11/24 14:04
 * Description:
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package com.tx;
import java.util.Date;

/**
 * 〈一句话功能简述〉<br> 
 * 〈〉
 *
 * @author java
 * @create 2018/11/24
 * @since 1.0.0
 */
public class Student {
    private  Date date;
    private String name;
    private  Integer gender;
    public Student(){

    }
    public Student(Date date, String name, Integer gender) {
        this.date = date;
        this.name = name;
        this.gender = gender;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getGender() {
        return gender;
    }

    public void setGender(Integer gender) {
        this.gender = gender;
    }

    @Override
    public String toString() {
        return "Student{" +
                "date=" + date +
                ", name='" + name + '\'' +
                ", gender=" + gender +
                '}';
    }
}
