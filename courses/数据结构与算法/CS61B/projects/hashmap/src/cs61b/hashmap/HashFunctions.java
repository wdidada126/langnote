package cs61b.hashmap;

import java.util.ArrayList;
import java.util.List;
import java.util.function.ToIntFunction;

/** 字符串哈希实验（L22）：Horner/31 法与分布均匀性检查。 */
public final class HashFunctions {

    private HashFunctions() {}

    /** JDK String.hashCode 同款：h = h*31 + c，32 位溢出回绕是特性不是 bug（L02）。 */
    public static int horner31(String s) {
        int h = 0;
        for (int i = 0; i < s.length(); i++) h = 31 * h + s.charAt(i);
        return h;
    }

    /** 演示用"坏哈希"：只用首字符——链长爆炸，正是 L22 反对的哈希函数。 */
    public static int firstCharOnly(String s) { return s.charAt(0); }

    /** 简易均匀性检查：把 keys 撒入 cap 个桶，返回 [mean, maxChain]。 */
    public static double[] distribution(List<Integer> keys, int cap, ToIntFunction<Integer> hash) {
        int[] cnt = new int[cap];
        for (int k : keys) cnt[Math.floorMod(hash.applyAsInt(k), cap)]++;
        int max = 0; long sum = 0;
        for (int c : cnt) { max = Math.max(max, c); sum += c; }
        return new double[]{(double) sum / cap, max};
    }

    /** 一组两两 Horner31 相同长度的演示键（用于注释中的手工验算）。 */
    public static List<String> demoCollisionPair() {
        List<String> out = new ArrayList<>();
        out.add("Aa"); // 65*31 + 97 = 2112
        out.add("BB"); // 66*31 + 66 = 2112 —— JDK 经典碰撞对：第一位差 1、第二位差 31 即同值
        return out;
    }
}
