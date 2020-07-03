# xml

1、
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

2、
xerces

3、
org.xml.sax


	public static void main(String[] args) throws Exception {
		
		SAXParserFactory saxFactory = SAXParserFactory.newInstance();
		SAXParser saxParser = saxFactory.newSAXParser();
		SaxParserXMl spx = new SaxParserXMl();
		saxParser.parse(new File("src/abc.xml"), spx);
		System.out.println(Arrays.toString(spx.getUserList().toArray()));
	}
原文链接：https://blog.csdn.net/is_zhoufeng/article/details/7558074
