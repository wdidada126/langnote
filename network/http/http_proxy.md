# http proxy

beijing银行，底座代码，http访问走代理

	private static HttpURLConnection getHttpURLConnection(String uri, String method, String proxy, int port, final String extendData) throws IOException {
		URL url = new URL(uri);
		Proxy proxy = new Proxy(Type.HTTP, new InetSocketAddress(proxy, port));
		HttpURLConnection httpConn = (HttpURLConnection) url.openConnection(proxy);
	}