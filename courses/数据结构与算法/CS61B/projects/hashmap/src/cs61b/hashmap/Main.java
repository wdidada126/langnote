package cs61b.hashmap;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** 自测入口：对应 L20–L22。 */
public final class Main {

    private static void check(boolean c, String msg) {
        if (!c) throw new AssertionError("FAIL: " + msg);
        System.out.println("ok - " + msg);
    }

    /** 故意的坏键：hashCode 恒为 1、equals 按 id —— 演示"契约允许，但性能自杀"（L20/L22）。 */
    static final class StickyKey {
        final int id;
        StickyKey(int id) { this.id = id; }
        @Override public int hashCode() { return 1; }
        @Override public boolean equals(Object o) { return o instanceof StickyKey s && s.id == id; }
    }

    public static void main(String[] args) {
        basics();
        rehash();
        adversarial();
        uniformity();
        contract();
        System.out.println("\n[hashmap] all self-tests passed.");
    }

    static void basics() {
        THashMap<String, Integer> m = new THashMap<>();
        check(m.put("a", 1) == null, "新键返回 null");
        check(m.put("a", 2) == 1, "重复键返回旧值");
        check(m.get("a") == 2 && m.size() == 1, "更新不增加 size");
        check(m.remove("a") == 2 && m.get("a") == null && m.isEmpty(), "删除");
        m.put(null, 42);
        check(m.get(null) == 42, "null 键可存取（JDK HashMap 行为，null 固定 0 桶）");
        m.remove(null);
    }

    static void rehash() {
        int n = 5000;
        THashMap<Integer, String> m = new THashMap<>();
        for (int i = 0; i < n; i++) m.put(i, "v" + i);
        check(m.size() == n, "5000 键无丢失");
        System.out.println("   桶数 = " + m.bucketCount() + "，rehash 次数 = " + m.rehashCount()
                + "（≈ log2(n/6)，再哈希总工作量摊进每次 put = Θ(1)，L21）");
        check(m.longestChain() <= 8, "好哈希下最长链很短：" + m.longestChain());
        for (int i = 0; i < n; i += 7)
            if (!("v" + i).equals(m.get(i))) throw new AssertionError("FAIL: 再哈希后查不到 " + i);
        System.out.println("ok - 全量抽查（步长 7）再哈希后都在");
        for (int i = 0; i < n; i++) m.remove(i);
        check(m.isEmpty(), "清空");
    }

    static void adversarial() {
        List<StickyKey> keys = new ArrayList<>();
        for (int i = 0; i < 300; i++) keys.add(new StickyKey(i));
        THashMap<StickyKey, Integer> m = new THashMap<>();
        for (StickyKey k : keys) m.put(k, 1);
        int sum = 0;
        for (StickyKey k : keys) sum += m.get(k);
        check(sum == keys.size(), "同 hashCode 键仍全部正确存取（equals 兜底，契约不破功能）");
        System.out.println("   300 个碰撞键最长链 = " + m.longestChain() + " ⇒ get 退化 Θ(n)（L22）");
        check(m.longestChain() >= 200, "链长确实退化");
    }

    static void uniformity() {
        var keys = new ArrayList<Integer>();
        for (int i = 0; i < 10_000; i++) keys.add(i * 97);
        double[] good = HashFunctions.distribution(keys, 1024, k -> k ^ (k >>> 16));
        double[] worse = HashFunctions.distribution(keys, 1024, k -> k * 1024); // 低位全 0 ⇒ 同桶
        System.out.printf("   扰动后 maxChain=%.0f(mean=%.1f) vs 低位为零 maxChain=%.0f%n",
                good[1], good[0], worse[1]);
        check(good[1] < worse[1], "hash 扰动/高位混合能救链长（JDK spread 的动机，L22）");
    }

    static void contract() {
        var pair = HashFunctions.demoCollisionPair();
        check(Objects.equals(HashFunctions.horner31(pair.get(0)), HashFunctions.horner31(pair.get(1))),
                "\"Aa\" 与 \"``\" 的 Horner31 值相同——String.hashCode 允许碰撞");
        THashMap<String, Integer> m = new THashMap<>();
        m.put(pair.get(0), 1); m.put(pair.get(1), 2);
        check(m.get(pair.get(0)) == 1 && m.get(pair.get(1)) == 2 && m.size() == 2,
                "碰撞的两个键由 equals 区分（L20 hash code 契约）");
    }
}
