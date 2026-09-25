package cs61b.graph;

import java.util.ArrayList;
import java.util.List;

/**
 * 加权无向图，邻接表表示（L29 / Lab9 API 精神）。
 * Map<Integer,?> 可换成"任意对象顶点"，这里用 0..V-1 的 int 以便数组直取。
 */
public class Graph {

    public record Edge(int from, int to, double weight) {}

    private final int v;
    private final List<List<Edge>> adj;
    private int directedEdges;

    public Graph(int v) {
        this.v = v;
        adj = new ArrayList<>(v);
        for (int i = 0; i < v; i++) adj.add(new ArrayList<>());
    }

    public int V() { return v; }
    public int directedEdgeCount() { return directedEdges; }

    /** 加无向边：存两个方向（Θ(deg) 空间，邻接表总 Θ(V+E)）。 */
    public void addEdge(int a, int b, double w) {
        addDirectedEdge(a, b, w);
        addDirectedEdge(b, a, w);
    }

    public void addDirectedEdge(int from, int to, double w) {
        adj.get(from).add(new Edge(from, to, w));
        directedEdges++;
    }

    public List<Edge> adj(int vertex) { return adj.get(vertex); }
}
