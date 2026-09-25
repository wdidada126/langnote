package cs61b.minigit;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;

/**
 * 内容寻址对象库（Project3/GITLET 核心思想的极简版，呼应 6.824 的 content-addressed store）。
 * 对象格式（与 git 同构）："type size\0raw"；
 * 对象 ID = SHA-1 十六进制；落盘路径 objects/xx/yyy...（前 2 位分桶——又是一层哈希，L20）。
 * 真实 git 还会 zlib 压缩（L37 I/O 延伸），这里保留明文便于 cat 查看。
 */
public class ObjectStore {

    private final Path objectsDir;

    public ObjectStore(Path repoDir) {
        this.objectsDir = repoDir.resolve("objects");
        try {
            Files.createDirectories(objectsDir);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    /** 写入对象，返回其哈希 ID；同内容重复写入得到同 ID（幂等/去重，Dedup 的根基）。 */
    public String writeObject(String type, byte[] content) {
        byte[] canonical = canonical(type, content);
        String id = sha1Hex(canonical);
        Path bucket = objectsDir.resolve(id.substring(0, 2));
        Path file = bucket.resolve(id.substring(2));
        try {
            if (!Files.exists(file)) {
                Files.createDirectories(bucket);
                Files.write(file, canonical);
            }
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        return id;
    }

    public boolean has(String id) {
        return Files.exists(objectsDir.resolve(id.substring(0, 2)).resolve(id.substring(2)));
    }

    /** 读出并校验：文件内容重新哈希必须等于 ID（内容寻址=自带完整性校验，Git 抗篡改原理）。 */
    public ObjectData readObject(String id) {
        try {
            byte[] raw = Files.readAllBytes(
                    objectsDir.resolve(id.substring(0, 2)).resolve(id.substring(2)));
            String recomputed = sha1Hex(raw);
            if (!recomputed.equals(id)) throw new IllegalStateException("对象损坏: " + id);
            return parse(raw);
        } catch (IOException e) {
            throw new UncheckedIOException("缺失对象 " + id, e);
        }
    }

    record ObjectData(String type, byte[] content) {}

    private static byte[] canonical(String type, byte[] content) {
        String header = type + " " + content.length + "\0";
        byte[] h = header.getBytes(java.nio.charset.StandardCharsets.UTF_8);
        byte[] out = new byte[h.length + content.length];
        System.arraycopy(h, 0, out, 0, h.length);
        System.arraycopy(content, 0, out, h.length, content.length);
        return out;
    }

    private static ObjectData parse(byte[] raw) {
        int sp = -1, nul = -1;
        for (int i = 0; i < raw.length; i++) {
            if (sp < 0 && raw[i] == ' ') sp = i;
            if (raw[i] == 0) { nul = i; break; }
        }
        if (sp < 0 || nul < 0) throw new IllegalStateException("对象格式非法");
        String type = new String(raw, 0, sp, java.nio.charset.StandardCharsets.UTF_8);
        byte[] content = new byte[raw.length - nul - 1];
        System.arraycopy(raw, nul + 1, content, 0, content.length);
        return new ObjectData(type, content);
    }

    static String sha1Hex(byte[] data) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-1");
            return HexFormat.of().formatHex(md.digest(data));
        } catch (NoSuchAlgorithmException e) {
            throw new AssertionError("SHA-1 必然存在", e);
        }
    }
}
