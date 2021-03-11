

import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.alibaba.dubbo.rpc.Filter;
import com.alibaba.dubbo.rpc.Invocation;
import com.alibaba.dubbo.rpc.Invoker;
import com.alibaba.dubbo.rpc.Result;
import com.alibaba.dubbo.rpc.RpcContext;
import com.alibaba.dubbo.rpc.RpcException;

public class ServiceDubboConsumerFilter implements Filter {
    private static Logger logger = LoggerFactory.getLogger(ServiceDubboConsumerFilter.class);
    
    @Override
    public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException {
    	if(logger.isDebugEnabled()) {
    		String paramStr = getParamString(invocation);
        	String paramStrOut = paramStr;
        	if(paramStr.length() > ServiceDubboProviderFilter.MAX_REQUEST_OUTSIZE) {
        		paramStrOut = paramStr.substring(0, ServiceDubboProviderFilter.MAX_REAMIN_OUTSIZE);
        	}
    		logger.debug("Dubbo consumer start. method:{}, param:{}", getInterfaceMethod(invoker, invocation), paramStrOut);
    	}
    	long startTime = System.currentTimeMillis();
    	this.appendxxxHeader(invoker, invocation);
    	Result result = null;
    	try {
			result = invoker.invoke(invocation);
		} finally {
			if(logger.isDebugEnabled()) {
				String resultStr = "error";
	        	if(result != null && !result.hasException()) {
	        		Object res = result.getValue();
	        		if(res != null) {
	        			if(res instanceof String) {
	        				resultStr = res.toString();
	        			}else {
	        				resultStr = JsonUtil.toJsonString(res);
	        			}
	        			//此步骤预防日志文件的快速增长
	        			if(resultStr.length() > ServiceDubboProviderFilter.MAX_RESULT_OUTSIZE) {
	        				resultStr = resultStr.substring(0, ServiceDubboProviderFilter.MAX_REAMIN_OUTSIZE);
	        			}
	        		}else {
	        			resultStr = null;
	        		}
	        	}
				logger.debug("Dubbo consumer over.  method:{}, time:{}, result:{}", getInterfaceMethod(invoker, invocation), (System.currentTimeMillis()-startTime) + "ms", resultStr);
	    	}
		}
    	return result;
    }
    
    protected String getInterfaceMethod(Invoker<?> invoker, Invocation invocation) {
    	return invoker.getInterface() + "." + invocation.getMethodName();
    }
    
    protected String getParamString(Invocation invocation) {
    	return JsonUtil.toJsonString(invocation.getArguments());
    }
    
    protected void appendxxxHeader(Invoker<?> invoker, Invocation invocation) {
    	String interf = invoker.getInterface().getName();
    	if(interf.startsWith("com.yyy.xxx.")) {
    		ThreadLocalTokenDTO localDTO = ServiceThreadLocal.getUserthreadlocal().get();
    		if(localDTO != null) {
    			for(Map.Entry<String,String> entity : localDTO.getHeader().entrySet()) {
    				RpcContext.getContext().setAttachment(entity.getKey(), entity.getValue());
    			}
    		}
    		RpcContext.getContext().setAttachment(ServiceDubboProviderFilter.SERVER_INNER, "true");
    	}else if(interf.startsWith("com.yyy.edu.pdc.uc.")) {
    		if( DubboClientFactory.SucHeader != null ) {
    			int size = DubboClientFactory.SucHeader.size();
    			for(int i = 0 ; i < size ; i++) {
    				String[] values = DubboClientFactory.SucHeader.get(i);
    				RpcContext.getContext().setAttachment(values[0], values[1]);
    			}
    		}
    	}
    }
}
