/**
 * Copyright (C), 2015-2018, XXX有限公司
 * FileName: Person
 * Author:   java
 * Date:     2018/11/26 18:03
 * Description:
 * History:
 * <author>          <time>          <version>          <desc>
 * 作者姓名           修改时间           版本号              描述
 */
package cn.test.com;
import java.util.*;
/**
 * 〈一句话功能简述〉<br> 
 * 〈〉
 *
 * @author java
 * @create 2018/11/26
 * @since 1.0.0
 */
interface BeDo{
    public void Add();
    public void Edit();
    public void Query();
    public void Delet();

}
class Admin implements BeDo{

    Scanner sc = new Scanner(System.in);
    private String name;
    private String password;
    private List list;

    public String getName() {
        return name;
    }

    public void setName() {
        System.out.println("请输入姓名");
        String name = sc.nextLine();
        this.name = name;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword() {
        System.out.println("请输入密码");
        String password = sc.nextLine();
        this.password = password;
    }

    public List getList() {
        return list;
    }

    public void setList(List list) {
        this.list = list;
    }

    public void Add(){
        card obj = new card();
        obj.setName();
        obj.setNum();
        obj.setColor();
        obj.setInfo();
        obj.setPrice();
        card.setList(obj);
        card.setAppendID();
    }
    public void Edit(){
        int length = card.getList().size();
        if(length == 0){
            System.out.println("暂无车辆信息");
        }
        List cards = card.getList();
        System.out.println("请输入要编辑的车辆的车牌");
        String s1 = sc.nextLine();
        boolean result = false;
        for(int i = 0;i<cards.size();i++){
                Object obj = cards.get(i);
                card cds = (card) obj;//将找到的对象 的引用强制转型子类引用
                result = cds.getNum().equals(s1)?true:false;
                if(result){
                    System.out.println("1.编辑名称   2.编辑价格   3.编辑车牌  4.编辑描述信息   5编辑颜色");
                    String s = sc.next();
                    Integer select = Integer.parseInt(s);
                    try {
                        switch (select){
                            case 1:
                                this.EditName(cds);
                                break;
                            case 2:
                                this.EditPrice(cds);
                                break;
                            case 3:
                                this.EditNum(cds);
                                break;
                            case 4:
                                this.EditInfo(cds);
                                break;
                            case 5:
                                this.Editcolor(cds);
                                break;
                        }
                        System.out.println("修改成功");
                    }catch (Exception e){
                        e.printStackTrace();
                        System.out.println("需要输入数字");
                        System.out.println("请输入数字");
                        System.out.println("是否继续输入 yes/no");
                        String getUser = sc.next();
                        if("yes".equals(getUser)){
                            continue;
                        }else{
                            break;
                        }
                    }
                }
        }
        if(result == false){System.out.println("没有找到车辆信息,请重新操作");}

    }
    public void Editcolor(card cd){
        cd.setColor();
    }
    public void EditPrice(card cd){
        cd.setPrice();
    }
    public void EditNum(card cd){
        cd.setNum();
    }
    public void EditName(card cd){
        cd.setName();
    }
    public void EditInfo(card cd){
        cd.setInfo();
    }
    public void Query(){
        int length = card.getList().size();
        if(length == 0){
            System.out.println("暂无车辆信息");
        }
        System.out.println("请输入要查找的车牌号码");
        try {
            String num = sc.next();
            boolean result = false;
            for(int i =0;i<card.getList().size();i++){
                Object obj = card.getList().get(i);//找到列表里面对应的车辆对象  将找到的对象 的引用强制转型子类引用
                result = ((card) obj).getNum().equals(num)?true:false;
                if(result){
                    System.out.println(obj);
                }
            }
            if(result == false){System.out.println("没有找到车辆信息");}
        }catch (Exception e){
            e.printStackTrace();

        }

    }
    public void Delet(){

        int length = card.getList().size();
        if(length == 0){
            System.out.println("暂无车辆信息");
        }else{
            System.out.println("请输入序号");
            this.show();
            try {
                String nums = sc.next();
                int n = Integer.parseInt(nums);
                boolean result = n<length?true:false;
                if(result){card.getList().remove(n);
                    System.out.println("移除成功");
                }else {System.out.println("序号超过可选范围");}
            }catch (Exception e){
                e.printStackTrace();
            }

        }
    }
    public void show(){
        int length = card.getList().size();
        for(int  i = 0;i<length;i++){
            System.out.print("序号: "+i+"\t");
            System.out.println(card.getList().get(i));
        }
    }


}
class User{
    Scanner sc = new Scanner(System.in);
    private Integer id;//身份证
    private Integer driveId;//驾照
    private Integer phoneNum;//手机号码
    private String addr;//联系地址
    private double rmb;//租金
    private Integer day;//租借天数
    private String num;//租借的车牌号
    private static List list1;

    public String getNum() {
        return num;
    }

    public void setNum() {
        System.out.println("请输入要租借的车牌");
        String num = sc.next();
        this.num = num;
    }

    public List getList1() {
        return User.list1;
    }

    public static void setList1(List list1) {
        User.list1 = list1;
    }

    public Integer getId() {
        return id;
    }

    public void setId() {

        while (true){
            try {
                System.out.println("请输入身份证");
                Integer id = sc.nextInt();
                if(id == null){break;}
                this.id = id;
            }catch (Exception e){
                e.printStackTrace();
                System.out.println("请输入数字");
                continue;
            }
            break;
        }

    }

    public Integer getDriveId() {
        return driveId;
    }

    public void setDriveId() {

        while (true){
            try {
                System.out.println("请输入驾照");
                Integer driveId = sc.nextInt();
                this.driveId = driveId;
                break;
            }catch (Exception e){
                e.printStackTrace();
                System.out.println("请输入数字");
                continue;

            }
        }

    }

    public Integer getPhoneNum() {
        return phoneNum;
    }

    public void setPhoneNum() {

        while (true){
            try {
                System.out.println("请输入手机号码");
                String phoneNum = sc.next();
                this.phoneNum = Integer.parseInt(phoneNum);
                break;
            }catch (Exception e){
                e.printStackTrace();
                System.out.println("请输入数字");
                continue;
            }
        }
    }

    public String getAddr() {
        return addr;
    }

    public void setAddr() {
        System.out.println("请输入联系地址");
        String addr = sc.next();
        this.addr = addr;
    }

    public double getRmb() {
        return rmb;
    }

    public void setRmb() {

        while (true){
            try {
                System.out.println("请输入租金");
                double rmb = sc.nextDouble();
                this.rmb = rmb;
                break;
            }catch (Exception e){
                e.printStackTrace();
                System.out.println("请输入数字");
                continue;
            }
        }

    }

    public Integer getDay() {
        return day;
    }

    public void setDay() {

        while (true){
            try {
                System.out.println("请输入租期");
                int day = sc.nextInt();
                this.day = day;
                break;
            }catch (Exception e){
                e.printStackTrace();
                System.out.println("请输入数字");
                continue;
            }
        }

    }



    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", driveId=" + driveId +
                ", phoneNum=" + phoneNum +
                ", addr='" + addr + '\'' +
                ", rmb=" + rmb +
                ", day=" + day +
                '}';
    }
}

