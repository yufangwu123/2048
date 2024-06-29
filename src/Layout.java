import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
//导入相关swing组件

public class Layout extends JFrame {
//继承JFrame窗体类


  public Layout() {
    //编写窗体布局方法
    setTitle("2048");

    int[] num = {2, 4};

    Container c = getContentPane();
    //获取容器
    GridLayout gridLayout = new GridLayout(4, 4, 2, 2);
    c.setLayout(gridLayout);
    //设置布局方式为：网格布局，设置网格的几行几列，水平竖直间距
    List<JTextField> textFieldList = new ArrayList<>();
    Random random = new Random();
    for (int i = 0; i < 16; i++) {
      JTextField textField = new JTextField();
      textFieldList.add(textField);
      textField.setFont(new Font(textField.getFont().getName(), textField.getFont().getStyle(), 80));
      textField.setHorizontalAlignment(JTextField.CENTER);
      textField.setEditable(false);
      textField.setFocusable(false);
      add(textField);
    }

    int first = random.nextInt(16);

    int second;
    do {
      second = random.nextInt(16);
    } while (second == first);

    textFieldList.get(first).setText("" + num[random.nextInt(2)]);
    textFieldList.get(second).setText("" + num[random.nextInt(2)]);

    ;
    //添加组件填满网格
    addKeyListener(new MyKeyListener(textFieldList));

    requestFocusInWindow();
    requestFocus();
    setBounds(200, 200, 800, 800);
    setVisible(true);
    setDefaultCloseOperation(EXIT_ON_CLOSE);
  }

  public static void main(String[] args) {
    new Layout();
  }
}