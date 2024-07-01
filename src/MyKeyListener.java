
import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;

public class MyKeyListener implements KeyListener {

    private List<JTextField> textFields;

    private static final int UP_AND_DOWN_DISTANCE = 4;
    private static final int LEFT_AND_RIGHT_DISTANCE = 1;

    private enum Direction {UP, DOWN, LEFT, RIGHT}


    private int[] num = {2, 4};

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

        // 抽象出处理按键的核心逻辑到单独的方法
        switch (keyCode) {
            case KeyEvent.VK_UP:
                pocess(Direction.UP);
                break;
            case KeyEvent.VK_DOWN:
                pocess(Direction.DOWN);
                break;
            case KeyEvent.VK_LEFT:
                pocess(Direction.LEFT);
                break;
            case KeyEvent.VK_RIGHT:
                pocess(Direction.RIGHT);
                break;
        }
        List<JTextField> collect = textFields.stream().filter(a -> "".equals(a.getText())).collect(Collectors.toList());
    /*if(collect.isEmpty()){
      List<JTextField> collectOne = textFields.stream().filter(a -> "2048".equals(a.getText())).collect(Collectors.toList());
      if(collectOne.isEmpty()){

      }
    }*/
        Random random = new Random();
        try {
            collect.get(random.nextInt(collect.size())).setText(num[random.nextInt(2)] + "");
        } catch (Exception ex) {
            // 如果出现异常，则代表游戏结束
            int option = JOptionPane.showOptionDialog(
                    null, // 父窗口，默认为当前窗口的根窗体
                    "游戏已结束！",
                    "游戏结束",
                    JOptionPane.DEFAULT_OPTION, // 默认选项类型
                    JOptionPane.INFORMATION_MESSAGE, // 消息类型
                    null, // 自定义图标，这里不需要
                    new String[]{"确认"}, // 选项按钮的文字
                    "确认" // 默认选中的按钮
            );
            if (option == JOptionPane.OK_OPTION) {
                // 用户点击了确认按钮，这里可以执行退出程序的操作
                System.exit(0); // 关闭整个程序
            }
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {

    }

    public void pocess(Direction direction) {
        int length;
        int distance;
        int increment;
        List<Integer> indexList = new ArrayList<>();
        Collections.addAll(indexList, 0, 1, 2, 3);

        // 通过方向判断遍历最大长度和偏移量
        if (direction == Direction.UP || direction == Direction.DOWN) {
            length = 4;
            distance = UP_AND_DOWN_DISTANCE;
        } else {
            length = 16;
            distance = LEFT_AND_RIGHT_DISTANCE;
        }
        increment = length / 4;
        if (direction == Direction.DOWN || direction == Direction.RIGHT) {
            Collections.reverse(indexList);
        }

        for (int i = 0; i < length; i += increment) {
            int a = Integer.parseInt("".equals(textFields.get(i + distance * 0).getText()) ? String.valueOf(0) : textFields.get(i + distance * 0).getText());
            int b = Integer.parseInt("".equals(textFields.get(i + distance * 1).getText()) ? String.valueOf(0) : textFields.get(i + distance * 1).getText());
            int c = Integer.parseInt("".equals(textFields.get(i + distance * 2).getText()) ? String.valueOf(0) : textFields.get(i + distance * 2).getText());
            int d = Integer.parseInt("".equals(textFields.get(i + distance * 3).getText()) ? String.valueOf(0) : textFields.get(i + distance * 3).getText());
            List<Integer> list = new ArrayList<>();
            if (direction == Direction.DOWN || direction == Direction.RIGHT) {
                Collections.addAll(list, d, c, b, a);
            } else {
                Collections.addAll(list, a, b, c, d);
            }
            sortList(list);
            a = list.get(indexList.get(0));
            b = list.get(indexList.get(1));
            c = list.get(indexList.get(2));
            d = list.get(indexList.get(3));
            textFields.get(i + distance * 0).setText(a == 0 ? "" : a + "");
            textFields.get(i + distance * 1).setText(b == 0 ? "" : b + "");
            textFields.get(i + distance * 2).setText(c == 0 ? "" : c + "");
            textFields.get(i + distance * 3).setText(d == 0 ? "" : d + "");
        }
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
