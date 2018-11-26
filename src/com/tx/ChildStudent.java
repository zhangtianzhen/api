/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: ChildStudent
 * Author:   java
 * Date:     2018/11/25 14:36
 * Description:
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package com.tx;

/**
 * 〈一句话功能简述〉<br> 
 * 〈〉
 *
 * @author java
 * @create 2018/11/25
 * @since 1.0.0
 */
public class ChildStudent  extends Student{
    private float lhq;

    public float getLhq() {
        return lhq;
    }

    public void setLhq(float lhq) {
        this.lhq = lhq;
    }

    @Override
    public String toString() {
        return "ChildStudent{" +
                "lhq=" + lhq +
                '}';
    }
}
