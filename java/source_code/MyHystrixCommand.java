
import com.netflix.hystrix.HystrixCommand;
import com.netflix.hystrix.HystrixCommandGroupKey;

public class MyHystrixCommand extends HystrixCommand<String> {

    public static void main(String[] args) {
        MyHystrixCommand mMyHystrixCommand = new MyHystrixCommand(null);
        mMyHystrixCommand.execute();
    }
    protected MyHystrixCommand(HystrixCommandGroupKey group) {
        super(group);
    }

    @Override
    protected String run() throws Exception {
        return null;
    }

}
