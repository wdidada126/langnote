package https;


/**
 *
 */
public class Okhttp {

    public void test(){
        OkHttpClient client = new OkHttpClient.Builder().build();
        Request request = new Request.Builder().url( "https://www.baidu.com/").build();
        //构造Call对象--其实是AsyncCall对象
        Call call = client.newCall(request);
        //调用Call.enqueue方法进行异步请求
        call.enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                //网络请求失败
                Log.d("lenve", "onFailure: " + e.getMessage());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                //网络请求成功，将请求的图片信息显示的ImageView控件上
                //Bitmap bitmap = BitmapFactory.decodeStream(   response.body().byteStream());
                String s = response.body().toString();
                System.out.println(s);
                Log.i("TestClassLoader",s);
            }
        });

    }
}
