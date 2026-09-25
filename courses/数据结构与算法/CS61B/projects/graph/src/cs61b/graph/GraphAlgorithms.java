package cs61b.graph;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;

/**
 * 图算法四件套（L30 BFS/DFS、L31 MST、L32 Dijkstra）。
 * 统一约定：顶点 0..V-1；不可达距离用 Double.POSITIVE_INFINITY / -1（BFS）。
 */
public final class GraphAlgorithms {

    private GraphAlgorithms() {}

    /* ---------- BFS（L30）：无权跳数 + 最短路树 edgeTo ---------- */

    public static int[] bfsHops(Graph g, int s) {
        int[] hops = new int[g.V()];
        Arrays.fill(hops, -1);
        hops[s] = 0;
        ArrayDeque<Integer> q = new ArrayDeque<>();
        q.add(s);
        while (!q.isEmpty()) {
            int v = q.remove();
            for (var e : g.adj(v)) {
                int w = e.to();
                if (hops[w] == -1) { hops[w] = hops[v] + 1; q.add(w); }
            }
        }
        return hops;
    }

    /* ---------- DFS（L30）：访问顺序 + 连通分量标记 ---------- */

    public static void dfsOrder(Graph g, int s, List<Integer> order, boolean[] marked) {
        marked[s] = true;
        order.add(s);
        for (var e : g.adj(s))
            if (!marked[e.to()]) dfsOrder(g, e.to(), order, marked);
    }

    /** 连通分量数：外层对未访问点起 DFS，Θ(V+E)。 */
    public static int connectedComponents(Graph g) {
        boolean[] marked = new boolean[g.V()];
        int count = 0;
        for (int v = 0; v < g.V(); v++)
            if (!marked[v]) { dfsOrder(g, v, new ArrayList<>(), marked); count++; }
        return count;
    }

    /* ---------- Dijkstra（L32）：非负权 SSSP；"lazy PQ"（陈旧项弹出时跳过） ---------- */

    public static double[] dijkstra(Graph g, int s, int[] edgeTo) {
        double[] dist = new double[g.V()];
        Arrays.fill(dist, Double.POSITIVE_INFINITY);
        Arrays.fill(edgeTo, -1);
        dist[s] = 0;
        PriorityQueue<double[]> pq = new PriorityQueue<>(Comparator.comparingDouble(a -> a[1]));
        pq.offer(new double[]{s, 0});
        while (!pq.isEmpty()) {
            double[] top = pq.poll();
            int v = (int) top[0];
            if (top[1] > dist[v]) continue;          // 陈旧条目：已有更优记录
            for (var e : g.adj(v)) {
                int w = e.to();
                double nd = dist[v] + e.weight();    // 松弛
                if (nd < dist[w]) {
                    dist[w] = nd;
                    edgeTo[w] = v;
                    pq.offer(new double[]{w, nd});   // 懒惰插入（decreaseKey 替代法）
                }
            }
        }
        return dist;
    }

    /* ---------- MST：Kruskal（边排序 + 并查集判环，L31） ---------- */

    public static List<Graph.Edge> kruskal(Graph g) {
        List<Graph.Edge> all = new ArrayList<>();
        for (int v = 0; v < g.V(); v++)
            for (var e : g.adj(v))
                if (e.from() <= e.to()) all.add(e);  // 无向边只收一次
        all.sort(Comparator.comparingDouble(Graph.Edge::weight));
        UnionFind uf = new UnionFind(g.V());
        List<Graph.Edge> mst = new ArrayList<>();
        for (var e : all)
            if (uf.union(e.from(), e.to())) mst.add(e);
        return mst;
    }

    /* ---------- MST：Prim lazy（PQ 装"穿越边界的边"，L31） ---------- */

    public static List<Graph.Edge> prim(Graph g) {
        List<Graph.Edge> mst = new ArrayList<>();
        boolean[] inTree = new boolean[g.V()];
        PriorityQueue<Graph.Edge> pq = new PriorityQueue<>(Comparator.comparingDouble(Graph.Edge::weight));
        for (int start = 0; start < g.V(); start++) {     // 支持森林（非连通图）
            if (inTree[start]) continue;
            inTree[start] = true;
            pq.addAll(g.adj(start));
            while (!pq.isEmpty()) {
                var e = pq.poll();
                int w = e.to();
                if (inTree[w]) continue;                  // 陈旧边：另一端已入树
                inTree[w] = true;
                mst.add(e);
                pq.addAll(g.adj(w));
            }
        }
        return mst;
    }

    public static double totalWeight(List<Graph.Edge> edges) {
        double s = 0;
        for (var e : edges) s += e.weight();
        return s;
    }
}
