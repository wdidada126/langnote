package cs61b.minigit;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

/**
 * 自测入口：对应 Project3（GITLET）核心机制的迷你演练——
 * 内容寻址、去重、commit DAG、分支=指针移动、历史文件回溯。
 */
public final class Main {

    private static void check(boolean c, String msg) {
        if (!c) throw new AssertionError("FAIL: " + msg);
        System.out.println("ok - " + msg);
    }

    public static void main(String[] args) throws Exception {
        Path dir = Files.createTempDirectory("minigit-demo");
        System.out.println("仓库目录: " + dir);
        MiniGit g = MiniGit.init(dir);

        // c1：两个文件
        String bHello = g.add("a.txt", "hello\n");
        g.add("src/App.java", "public class App {}\n");
        String c1 = g.commit("first commit");
        check(g.currentCommitId().equals(c1), "提交移动分支指针（ref 更新 O(1)）");

        // c2：改 a.txt、删 src/App.java；重复内容 ⇒ 同一 blob（去重/幂等）
        String bHello2 = g.add("a.txt", "hello\n");
        check(bHello.equals(bHello2), "相同内容 ⇒ 相同哈希 ID（内容寻址去重）");
        g.add("a.txt", "hello v2\n");
        g.add("b.txt", "beta\n");
        String c2 = g.commit("second commit");
        check(!c2.equals(c1) && g.log("main").equals(List.of(c2, c1)), "log 沿父链回溯：新→旧");

        // 分支（DAG 分叉）
        g.branch("feature");
        g.checkout("feature");
        g.add("c.txt", "gamma\n");
        String c3 = g.commit("feature work");
        check(g.log("feature").equals(List.of(c3, c2, c1)), "feature 线性历史 3 提交");
        check(g.log("main").size() == 2, "main 不受影响——分支只是另一个 ref 文件");
        g.checkout("main");
        check(g.currentCommitId().equals(c2), "HEAD 切换分支后指针正确");

        // 历史查询：从 c2 向上找 a.txt（c2 里有 v2；从 c1 找到 v1）
        check(g.blobContent(g.findFile(c2, "a.txt")).equals("hello v2\n"), "findFile：c2 处的 a.txt");
        check(g.blobContent(g.findFile(c1, "a.txt")).equals("hello\n"), "findFile：c1 处的 a.txt");
        check(g.blobContent(g.findFile(c2, "src/App.java")).contains("App"),
                "已在新快照删除的文件仍可从祖先恢复");

        // commit 对象结构（DAG 节点内容可读）
        var commit = g.readCommit(c2);
        check(commit.parentId().equals(c1), "commit.parent 构成 DAG（此处为链）");
        check(commit.message().equals("second commit"), "commit 携带元数据");
        check(commit.snapshot().containsKey("b.txt") && !commit.snapshot().containsKey("src/App.java"),
                "快照 = 路径→blobId 的映射（省略 tree 层的简化）");

        // 完整性：内容寻址自带校验（读回重哈希比对）
        var data = new ObjectStore(dir).readObject(bHello);
        check(data.type().equals("blob") && new String(data.content()).equals("hello\n"),
                "readObject 重哈希校验通过（篡改即报错）");

        System.out.printf("   对象库分布: %s 个对象文件（objects/xx/ 两级哈希分桶）%n", countObjects(dir));
        System.out.println("\n[minigit] all self-tests passed.");
    }

    static long countObjects(Path dir) throws Exception {
        try (var s = Files.walk(dir.resolve("objects"))) {
            return s.filter(Files::isRegularFile).count();
        }
    }
}
