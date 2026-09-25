package cs61b.minigit;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/**
 * MiniGit：哈希寻址 blob + commit DAG 的简化 Git（GITLET 核心骨架）。
 * 结构：objects/（内容寻址库）+ refs/heads/<branch>（名字→commit id 的文件）+ HEAD（当前分支名）。
 * 本实现省略 tree 对象层：commit 直接携带"路径→blobId"快照（键有序 TreeMap，序列化即字典序）。
 * 三件套正是 6.824 content-addressed storage + 名字解析的浓缩版。
 */
public class MiniGit {

    private final Path repoDir;
    private final ObjectStore store;
    private final Map<String, String> index = new LinkedHashMap<>(); // 暂存区：路径 → blobId

    private MiniGit(Path repoDir) {
        this.repoDir = repoDir;
        this.store = new ObjectStore(repoDir);
    }

    public static MiniGit init(Path dir) {
        try {
            Files.createDirectories(dir.resolve("refs").resolve("heads"));
            Files.writeString(dir.resolve("HEAD"), "main");
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        return new MiniGit(dir);
    }

    public static MiniGit open(Path dir) { return new MiniGit(dir); }

    /* ---------- 暂存与提交 ---------- */

    /** add：文件内容进对象库，返回 blob ID（同内容必同 ID ⇒ 天然去重）。 */
    public String add(String path, String content) {
        String blobId = store.writeObject("blob", content.getBytes(StandardCharsets.UTF_8));
        index.put(path, blobId);
        return blobId;
    }

    /** commit：快照+父指针+消息 → commit 对象；移动分支指针（ref 更新 = O(1)，这正是哈希寻址的红利）。 */
    public String commit(String message) {
        if (message.contains("\n") || message.isEmpty())
            throw new IllegalArgumentException("message 需非空且单行");
        String parent = currentCommitId();
        StringBuilder sb = new StringBuilder();
        sb.append("parent:").append(parent == null ? "-" : parent).append('\n');
        sb.append("message:").append(message).append('\n');
        for (var e : new TreeMap<>(index).entrySet())
            sb.append("e ").append(e.getKey()).append('\0').append(e.getValue()).append('\n');
        String id = store.writeObject("commit", sb.toString().getBytes(StandardCharsets.UTF_8));
        writeRef(headBranch(), id);
        index.clear();
        return id;
    }

    /* ---------- 分支与头 ---------- */

    public void branch(String name) {
        String tip = currentCommitId();
        if (tip == null) throw new IllegalStateException("还没有提交，无法建分支");
        writeRef(name, tip);
    }

    public void checkout(String branch) {
        if (readRef(branch) == null) throw new IllegalArgumentException("无此分支: " + branch);
        try {
            Files.writeString(repoDir.resolve("HEAD"), branch);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    public String headBranch() {
        try {
            return Files.readString(repoDir.resolve("HEAD")).trim();
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    public String currentCommitId() { return readRef(headBranch()); }

    private void writeRef(String branch, String commitId) {
        try {
            Path f = repoDir.resolve("refs").resolve("heads").resolve(branch);
            Files.createDirectories(f.getParent());
            Files.writeString(f, commitId);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    private String readRef(String branch) {
        try {
            Path f = repoDir.resolve("refs").resolve("heads").resolve(branch);
            return Files.exists(f) ? Files.readString(f).trim() : null;
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    /* ---------- 历史（DAG 遍历，L29–L30 的 DFS 在此落地） ---------- */

    record Commit(String id, String parentId, Map<String, String> snapshot, String message) {}

    Commit readCommit(String id) {
        var data = store.readObject(id);
        if (!data.type().equals("commit")) throw new IllegalStateException(id + " 不是 commit");
        String text = new String(data.content(), StandardCharsets.UTF_8);
        String parent = null, message = "";
        Map<String, String> snap = new LinkedHashMap<>();
        for (String line : text.split("\n")) {
            if (line.startsWith("parent:")) {
                String p = line.substring(7);
                parent = p.equals("-") ? null : p;
            } else if (line.startsWith("message:")) {
                message = line.substring(8);
            } else if (line.startsWith("e ")) {
                String body = line.substring(2);
                int z = body.indexOf('\0');
                snap.put(body.substring(0, z), body.substring(z + 1));
            }
        }
        return new Commit(id, parent, snap, message);
    }

    /** log：沿父链线性回溯（多父合并留作扩展——那才是 GITLET 的难点）。 */
    public List<String> log(String branch) {
        List<String> out = new ArrayList<>();
        String p = readRef(branch);
        while (p != null) {
            out.add(p);
            p = readCommit(p).parentId();
        }
        return out;
    }

    /** find：从某 commit 出发向上找路径的最新版本（git show <id>:<path> 语义，DFS/链式回溯）。 */
    public String findFile(String commitId, String path) {
        String cur = commitId;
        while (cur != null) {
            Commit c = readCommit(cur);
            String blob = c.snapshot().get(path);
            if (blob != null) return blob;
            cur = c.parentId();
        }
        throw new IllegalArgumentException("历史里找不到 " + path);
    }

    public String blobContent(String blobId) {
        var d = store.readObject(blobId);
        if (!d.type().equals("blob")) throw new IllegalStateException(blobId + " 不是 blob");
        return new String(d.content(), StandardCharsets.UTF_8);
    }
}
