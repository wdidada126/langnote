package cs61b.trie;

import java.util.List;

/** 自测入口：对应 L36（Trie 与前缀检索）。 */
public final class Main {

    private static void check(boolean c, String msg) {
        if (!c) throw new AssertionError("FAIL: " + msg);
        System.out.println("ok - " + msg);
    }

    public static void main(String[] args) {
        String[] corpus = {"app", "apple", "application", "apply", "apt", "bat", "bad", "band"};
        Trie t = new Trie();
        for (String w : corpus) t.insert(w);

        check(t.contains("app") && !t.contains("ap"), "contains 需要 end 标志（ap 只是前缀）");
        check(t.startsWith("ap") && !t.startsWith("zp"), "startsWith 只看路径存在");
        check(t.size() == corpus.length, "去重计数");

        t.insert("app"); // 重复插入不加 size、加词频
        check(t.size() == corpus.length, "重复词不增加 distinctWords");

        check(t.keysWithPrefix("app").equals(List.of("app", "apple", "application", "apply")),
                "前缀枚举字典序（DFS 即字母序）");
        check(t.keysWithPrefix("ba").equals(List.of("bad", "band", "bat")), "ba 家族");
        check(t.keysWithPrefix("z").isEmpty(), "无匹配前缀返回空");

        var dict = new Trie();
        dict.insert("pop", 5); dict.insert("pops", 9); dict.insert("popped", 3);
        dict.insert("popsicle", 1); dict.insert("port", 7);
        check(dict.autocomplete("po", 3).equals(List.of("pops", "port", "pop")),
                "自动补全按词频 Top-3：" + dict.autocomplete("po", 3));

        check(dict.delete("popped") && !dict.contains("popped"), "删除词");
        check(dict.startsWith("pop"), "共享前缀仍在（popped 删除不能误伤 pop 分支）");
        check(dict.delete("nonexist") == false, "删除不存在的词返回 false");

        // 空间：Θ(总字符数)，共享前缀省钱
        Trie s = new Trie();
        s.insert("aaaaaaaaaa");
        check(s.nodeCount() == 10, "10 字符单词 = 10 节点（最坏线性的直观证据）");

        System.out.println("\n[trie] all self-tests passed.");
    }
}
