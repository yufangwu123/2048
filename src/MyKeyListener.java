
import javax.swing.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;

public class MyKeyListener implements KeyListener {

  private List<JTextField> textFields;


  private   int[] num = {2,4};
  public MyKeyListener(List<JTextField> textFields) {
    this.textFields = textFields;
  }

  @Override
  public void keyTyped(KeyEvent e) {

  }

  @Override
  public void keyPressed(KeyEvent e) {
    int keyCode = e.getKeyCode();
    System.out.println("Key pressed: " + KeyEvent.getKeyText(keyCode));
    // 在这里处理按键按下事件
    if (keyCode == KeyEvent.VK_UP) {
      for (int i = 0; i < 4; i++) {
        int a = Integer.parseInt("".equals(textFields.get(i).getText()) ? String.valueOf(0) : textFields.get(i).getText());
        int b = Integer.parseInt("".equals(textFields.get(i + 4).getText()) ? String.valueOf(0) : textFields.get(i + 4).getText());
        int c = Integer.parseInt("".equals(textFields.get(i + 8).getText()) ? String.valueOf(0) : textFields.get(i + 8).getText());
        int d = Integer.parseInt("".equals(textFields.get(i + 12).getText()) ? String.valueOf(0) : textFields.get(i + 12).getText());
        List<Integer> list = new ArrayList<>();
        list.add(a);
        list.add(b);
        list.add(c);
        list.add(d);
        sortList(list);
        a = list.get(0);
        b = list.get(1);
        c = list.get(2);
        d = list.get(3);
        textFields.get(i).setText(a==0?"":a + "");
        textFields.get(i + 4).setText(b==0?"":b + "");
        textFields.get(i + 8).setText(c==0?"":c + "");
        textFields.get(i + 12).setText(d==0?"":d + "");
      }

    } else if (keyCode == KeyEvent.VK_DOWN) {
      for (int i = 0; i < 4; i++) {
        int a = Integer.parseInt("".equals(textFields.get(i).getText()) ? String.valueOf(0) : textFields.get(i).getText());
        int b = Integer.parseInt("".equals(textFields.get(i + 4).getText()) ? String.valueOf(0) : textFields.get(i + 4).getText());
        int c = Integer.parseInt("".equals(textFields.get(i + 8).getText()) ? String.valueOf(0) : textFields.get(i + 8).getText());
        int d = Integer.parseInt("".equals(textFields.get(i + 12).getText()) ? String.valueOf(0) : textFields.get(i + 12).getText());
        List<Integer> list = new ArrayList<>();
        list.add(d);
        list.add(c);
        list.add(b);
        list.add(a);
        sortList(list);
        d = list.get(0);
        c = list.get(1);
        b = list.get(2);
        a = list.get(3);
        textFields.get(i).setText(a==0?"":a + "");
        textFields.get(i + 4).setText(b==0?"":b + "");
        textFields.get(i + 8).setText(c==0?"":c + "");
        textFields.get(i + 12).setText(d==0?"":d + "");
      }
    } else if (keyCode == KeyEvent.VK_LEFT) {
      for (int i = 0; i < 16; i=i+4) {
        int a = Integer.parseInt("".equals(textFields.get(i).getText()) ? String.valueOf(0) : textFields.get(i).getText());
        int b = Integer.parseInt("".equals(textFields.get(i + 1).getText()) ? String.valueOf(0) : textFields.get(i + 1).getText());
        int c = Integer.parseInt("".equals(textFields.get(i + 2).getText()) ? String.valueOf(0) : textFields.get(i + 2).getText());
        int d = Integer.parseInt("".equals(textFields.get(i + 3).getText()) ? String.valueOf(0) : textFields.get(i + 3).getText());
        List<Integer> list = new ArrayList<>();
        list.add(a);
        list.add(b);
        list.add(c);
        list.add(d);
        sortList(list);
        a = list.get(0);
        b = list.get(1);
        c = list.get(2);
        d = list.get(3);
        textFields.get(i).setText(a==0?"":a + "");
        textFields.get(i + 1).setText(b==0?"":b + "");
        textFields.get(i + 2).setText(c==0?"":c + "");
        textFields.get(i + 3).setText(d==0?"":d + "");
      }

    } else if (keyCode == KeyEvent.VK_RIGHT) {
      for (int i = 0; i < 16; i=i+4) {
        int a = Integer.parseInt("".equals(textFields.get(i).getText()) ? String.valueOf(0) : textFields.get(i).getText());
        int b = Integer.parseInt("".equals(textFields.get(i + 1).getText()) ? String.valueOf(0) : textFields.get(i + 1).getText());
        int c = Integer.parseInt("".equals(textFields.get(i + 2).getText()) ? String.valueOf(0) : textFields.get(i + 2).getText());
        int d = Integer.parseInt("".equals(textFields.get(i + 3).getText()) ? String.valueOf(0) : textFields.get(i + 3).getText());
        List<Integer> list = new ArrayList<>();
        list.add(d);
        list.add(c);
        list.add(b);
        list.add(a);
        sortList(list);
        d = list.get(0);
        c = list.get(1);
        b = list.get(2);
        a = list.get(3);
        textFields.get(i).setText(a==0?"":a + "");
        textFields.get(i + 1).setText(b==0?"":b + "");
        textFields.get(i + 2).setText(c==0?"":c + "");
        textFields.get(i + 3).setText(d==0?"":d + "");
      }

    }
    List<JTextField> collect = textFields.stream().filter(a -> "".equals(a.getText())).collect(Collectors.toList());
    if(collect.isEmpty()){
      List<JTextField> collectOne = textFields.stream().filter(a -> "2048".equals(a.getText())).collect(Collectors.toList());
      if(collectOne.isEmpty()){

      }
    }
    Random random = new Random();
    collect.get(random.nextInt(collect.size())).setText(num[random.nextInt(2)]+"");
  }

  @Override
  public void keyReleased(KeyEvent e) {

  }


  public void sortList(List<Integer> list) {
    for (int i = 0; i < list.size(); i++) {
      if (list.get(i) == 0) {
        list.remove(list.get(i));
        list.add(0);
      }
    }
    for (int i = 0; i < list.size() - 1; i++) {
      if (list.get(i).equals(list.get(i + 1))) {
        list.set(i, list.get(i) * 2);
        list.remove(i + 1);
        list.add(0);
      }
    }
  }
}
