import java.net.MalformedURLException;
import java.net.URL;

public class URLDomainExtractor {
    public static void main(String[] args) {
        String urlStr = "https://axt-test.601169.cn:1443/#/my-index";//axt-test.601169.cn
        urlStr = "https://axt.bankofbeijing.com.cn/#/login";//axt.bankofbeijing.com.cn
        urlStr = "https://test-api.111hrs361.com/salaryManager/index.html#/witSalary/salaryCalcu";
        urlStr = "https://test-api.hrs361.com/salaryManager/index.html#/witSalary/salaryCalcu";
        try {
            URL url = new URL(urlStr);
            // 获取完整域名
            String domain = url.getHost();
            System.out.println("完整域名: " + domain);

            // 获取包含.601169.cn的部分
            int index = domain.indexOf(".hrs361.com");
            if (index != -1) {
                String targetPart = domain.substring(index);
                System.out.println("hrs361.com部分: " + targetPart);
            } else {
                System.out.println("未找到hrs361.com");
            }
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
    }
}