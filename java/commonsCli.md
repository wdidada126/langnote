# commonsCli

```java
import org.apache.commons.cli.*;

public class CommandLineParserTest {
    public static void main(String[] args) throws ParseException {
        Options options = new Options();
        options.addOption("open", true, "-open DBPath");
        options.addOption("create", true, "-create DBPath");
        options.addOption("mem", true, "-mem 64MB");
        CommandLineParser parser = new DefaultParser();
        CommandLine cmd = parser.parse(options,args);

        if(cmd.hasOption("open")) {
            System.out.println(cmd.getOptionValue("open"));
            System.out.println(cmd.getOptionValue("mem"));
            return;
        }
    }
}
```

入参：-open /tmp/mydb
输出：
/tmp/mydb
null
