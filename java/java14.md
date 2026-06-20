# java14

202003
新特性
Java 9-17 新特性解读
https://www.bilibili.com/video/BV1Fq4y1P7RQ/?spm_id_from=333.999.0.0&vd_source=71b9c2a5f966942c83677c2110efde22

    private static KThread idleThread = null;
	idleThread = new KThread(new Runnable() {
	    public void run() { while (true) yield(); }
	});
报错：
yield outside of switch expression
改成
	idleThread = new KThread(new Runnable() {
	    public void run() { while (true) Thread.yield(); }
	});