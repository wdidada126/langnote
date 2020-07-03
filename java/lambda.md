# lambda

Suppliy


// Java 8之前：
new Thread(new Runnable() {
    @Override
    public void run() {
    System.out.println("Before Java8");
    }
}).start();
new Thread( () -> System.out.println("In Java8, Lambda expression") ).start();


    @Test
    public void makeTest(){
        new Thread(()->{
            System.out.println("aaaaaaa");
        }).start();

        final List<Integer> integers =  Arrays.asList(1,2,3,4,5);
        Callable<Integer> callableObj = () -> {
            int result = integers.stream().mapToInt(i -> i.intValue()).sum();
            return result;
        };
        ExecutorService service =  Executors.newSingleThreadExecutor();
        Future<Integer> future = service.submit(callableObj);
        Integer result=0;
        try {
            result = future.get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        System.out.println("Sum = "+result);
    }