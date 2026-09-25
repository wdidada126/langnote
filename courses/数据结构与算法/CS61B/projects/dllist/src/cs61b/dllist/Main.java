package cs61b.dllist;

import java.util.ArrayList;
import java.util.List;

/** 自测入口：对应 L16–L19。运行 build.bat / build.sh。 */
public final class Main {

    private static void check(boolean cond, String msg) {
        if (!cond) throw new AssertionError("FAIL: " + msg);
        System.out.println("ok - " + msg);
    }

    public static void main(String[] args) {
        dllListBasics();
        dllListRandomAccess();
        arraySeqAmortization();
        arraySeqHeadInsert();
        System.out.println("\n[dllist] all self-tests passed.");
    }

    static void dllListBasics() {
        DLList<String> l = new DLList<>();
        l.checkInvariants();                       // 空表哨兵自环
        l.addLast("b"); l.addFirst("a"); l.addLast("c");
        l.checkInvariants();
        check(l.size() == 3 && "a,b,c".equals(String.join(",", toList(l))), "addFirst/addLast 顺序");
        check(l.removeFirst().equals("a") && l.removeLast().equals("c"), "两端删除返回值");
        check(l.size() == 1 && l.get(0).equals("b"), "中间状态");
        l.add(0, "z"); l.add(2, "y");
        check("z,b,y".equals(String.join(",", toList(l))), "按位置插入");
        check(l.contains("b") && !l.contains("q"), "contains 使用 equals");
    }

    static void dllListRandomAccess() {
        DLList<Integer> l = new DLList<>();
        for (int i = 0; i < 10; i++) l.addLast(i);
        check(l.get(9) == 9 && l.get(0) == 0, "get 两端都快（双向优势）");
        l.set(5, -5);
        check(l.get(5) == -5, "set 写回");
        l.remove(5);
        l.checkInvariants();
        check(l.size() == 9, "中间删除保持链完整");
    }

    static void arraySeqAmortization() {
        int n = 10_000;
        ArraySeq<Integer> s = new ArraySeq<>();
        for (int i = 0; i < n; i++) s.addLast(i);
        // 倍增扩容：从 8 出发，扩容次数 = ceil(log2(n/8)) + 1 附近；远小于 n ⇒ 摊还 Θ(1)
        check(s.resizeCount() < 20, "n=1e4 时扩容次数 " + s.resizeCount() + " < 20（倍增的功劳）");
        check(s.get(1234) == 1234, "随机访问 Θ(1)");
        for (int i = 0; i < n / 2 + 1; i++) s.removeLast();
        check(s.capacity() <= 2 * s.size(), "缩容阈值 1/4：容量 ≤ 2×size，无抖动");
    }

    static void arraySeqHeadInsert() {
        ArraySeq<String> s = new ArraySeq<>();
        for (String w : new String[]{"x", "y", "z"}) s.addFirst(w);
        check("z,y,x".equals(String.join(",", toList(s))), "addFirst 语义（代价 Θ(n) 搬移）");
    }

    static <I> List<I> toList(Iterable<I> it) {
        List<I> out = new ArrayList<>();
        for (I x : it) out.add(x);
        return out;
    }
}
