package cs61b.uf;

/** 接口：动态连通性三实现共同契约（L31）。count() 返回当前分量数。 */
public interface UF {
    int find(int p);
    boolean union(int a, int b);
    boolean connected(int a, int b);
    int count();
}
