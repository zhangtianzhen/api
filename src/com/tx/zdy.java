/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: zdy
 * Author:   java
 * Date:     2018/11/25 15:12
 * Description:
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package com.tx;

import java.util.ArrayList;
import java.util.Collection;

/**
 * 〈一句话功能简述〉<br> 
 * 〈〉
 *
 * @author java
 * @create 2018/11/25
 * @since 1.0.0
 */
public class zdy<E> {//自己指定数据类型
    private Collection<E> col = new ArrayList<E>();
    private E[] arr;

    public E[] getArr() {
        return arr;
    }

    public void setArr(E[] arr) {
        this.arr = arr;
    }
    public E getIndet(int index){
        return arr[index];
    }
    public void setCol(E cols){
        this.col.add(cols);
    }
}
