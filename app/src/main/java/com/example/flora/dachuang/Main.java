package com.example.flora.dachuang;

import android.content.DialogInterface;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Handler;
import android.text.TextUtils;
import android.widget.ImageView;
import android.widget.SearchView;
import android.widget.TextView;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

import com.baidu.location.LocationClient;
import com.baidu.location.LocationClientOption;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import me.zhanghai.android.materialratingbar.MaterialRatingBar;
import okhttp3.Call;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class Main extends AppCompatActivity {
    private SwipeRefreshLayout mSwipeRefreshLayout;
    private SearchView searchview;
    public LocationClient mLocationClient = null;
    private MyLocationListener myListener = new MyLocationListener();
    private String Response;
    private TextView StoreName1;
    private MaterialRatingBar ratingBar1;
    private ImageView imageView1;
    private TextView Distance1;
    private byte[] DownImage;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        StoreName1 = findViewById(R.id.text1_1);
        ratingBar1 = findViewById(R.id.star1);
        imageView1 = findViewById(R.id.image1);
        Distance1 = findViewById(R.id.text1_3);
        //下面是定位信息的获取，每两秒完成一次定位
        mLocationClient = new LocationClient(getApplicationContext());
        mLocationClient.registerLocationListener(myListener);
        searchview = findViewById(R.id.search_main);
        LocationClientOption option = new LocationClientOption();
        option.setLocationMode(LocationClientOption.LocationMode.Hight_Accuracy);
        option.setCoorType("bd09ll");
        option.setScanSpan(1000);
        option.setOpenGps(true);
        option.setLocationNotify(true);
        option.setIgnoreKillProcess(false);
        option.SetIgnoreCacheException(false);
        option.setWifiCacheTimeOut(5 * 60 * 1000);
        option.setEnableSimulateGps(false);
        mLocationClient.setLocOption(option);
        mLocationClient.start();
        mSwipeRefreshLayout = findViewById(R.id.swipeRefreshLayout);
        mSwipeRefreshLayout.setColorSchemeResources(R.color.blue,R.color.red,R.color.colorPrimary);
        searchview.setOnQueryTextListener(new SearchView.OnQueryTextListener() {
            @Override
            public boolean onQueryTextSubmit(String query) {
                try {
                    if (!TextUtils.isEmpty(query)) {
                        String latitude;
                        String longitude;
                        latitude = String.format("%.2f", myListener.latitude);
                        longitude = String.format("%.2f", myListener.longitude);
                        String url = "http://139.196.100.255:8080/search"; /*在此处改变你的服务器地址*/
                        SearchData(url, "海底捞火锅", latitude, longitude);
                        Thread.sleep(1000);
                        JSONObject jsonResponse = new JSONObject(Response);
                        String success = jsonResponse.getString("messages");
                        if (success.equals("success") ){
                            AlertDialog.Builder listDialog = new AlertDialog.Builder(Main.this);
                            listDialog.setTitle("查找成功");
                            JSONArray mtUsers = jsonResponse.getJSONArray("search result");
                            final String[] items=new String[mtUsers.length()];
                            for (int i=0; i<mtUsers.length(); i++){
                                JSONObject jsonObject = (JSONObject)mtUsers.get(i);
                                items[i] = jsonObject.getString("store");
                            }
                            listDialog.setItems(items, new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialog, int which) {
                                    // Toast.makeText(Main.this,"点击了"+items[which],Toast.LENGTH_SHORT).show();
                                    System.out.println("hahah");
                                }
                            });
                            listDialog.show();
                        }
                        else {
                            AlertDialog dialog1 = new AlertDialog.Builder(Main.this)
                                    .setMessage("查找失败，请输入正确的店名")
                                    .show();

                        }
                        System.out.println(Response);
                    }
                }
                catch (Exception e){
                    AlertDialog dialog1 = new AlertDialog.Builder(Main.this)
                            .setMessage("查找失败，请检查网络连接")
                            .show();
                    System.out.println(e);
                }
                return false;
            }

            @Override
            public boolean onQueryTextChange(String newText) {
                return false;
            }
        });
        //  这里是刷新功能的实现
        mSwipeRefreshLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                //模拟网络请求需要2000毫秒，请求完成，设置setRefreshing 为false
                new Handler().postDelayed(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            //注册监听函数
                            String latitude;
                            String longitude;
                            latitude = String.format("%.2f", myListener.latitude);
                            longitude = String.format("%.2f", myListener.longitude);
                            String url = "http://139.196.100.255:8080/search"; /*在此处改变你的服务器地址*/
                            SearchData(url,"海底捞火锅" ,latitude, longitude);
                            Thread.sleep(1000);
                            JSONObject jsonResponse = new JSONObject(Response);
                            mSwipeRefreshLayout.setRefreshing(false);
                            String success = jsonResponse.getString("messages");
                            if (success.equals("success") ){
                                JSONArray mtUsers = jsonResponse.getJSONArray("search result");
                                JSONObject one = mtUsers.getJSONObject(0);
                                String distance = one.getString("distance");
                                String img_url = one.getString("img_url");
                                String score = one.getString("score");
                                String store = one.getString("store");
                                double distance1 = Double.valueOf(distance);
                                distance1 = distance1 / 1000;
                                //  这里先使用了一个测试值，因为定位不准确，所以距离太长。
                                distance1 = 10.25;
                                distance = String.format("%.2f", distance1);
                                distance = distance + "km";
                                double score1 = Double.valueOf(score);
                                int score2 =(int)score1;
                                downImage(img_url);
                                // BitmapDrawable bitmapDrawable=(BitmapDrawable)(getResources().getDrawable(R.drawable.image1));
                                Bitmap bitmap1 = BitmapFactory.decodeByteArray(DownImage, 0,DownImage.length);
                                imageView1.setImageBitmap(bitmap1);
                                ratingBar1.setRating(score2);
                                StoreName1.setText(store);
                                Distance1.setText(distance);
                                ratingBar1.setIsIndicator(true);

                            }
                        }
                        catch (Exception e){
                            AlertDialog dialog1 = new AlertDialog.Builder(Main.this)
                                    .setMessage("查找失败，请检查网络连接")
                                    .show();
                            System.out.println(e);
                        }
                    }
                }, 2000);
            }
        });
    }


    private void downImage(String path) {
        final String path1 =path;
        new Thread(){
            @Override
            public void run() {
                try {
                    URL url = new URL(path1);
                    HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                    connection.setConnectTimeout(5000);
                    connection.setRequestMethod("GET");
                    int code = connection.getResponseCode();
                    if (code == 200) {// 表示获取成功
                        InputStream is = connection.getInputStream();
                        ByteArrayOutputStream byteArrayOut = new ByteArrayOutputStream();
                        byte[] buffer = new byte[1024];
                        int len;
                        while ((len = is.read(buffer)) != -1) {
                            byteArrayOut.write(buffer, 0, len);
                        }
                        DownImage = byteArrayOut.toByteArray();
                    }
                } catch (Exception e) {
                    AlertDialog dialog1 = new AlertDialog.Builder(Main.this)
                            .setMessage("查找失败，请检查网络连接")
                            .show();
                    System.out.println(e);
                }
            }
        }.start();

    }

    private void SearchData(String url,String storename, String latitude, String longitude){
        OkHttpClient client = new OkHttpClient();
        FormBody.Builder formBuilder = new FormBody.Builder();
        formBuilder.add("storename",  "海底捞火锅");
        formBuilder.add("latitude", latitude);
        formBuilder.add("longitude", longitude);
        Request request = new Request.Builder().url(url).post(formBuilder.build()).build();
        final Call call = client.newCall(request);
        new Thread(new Runnable() {
            @Override
            public void run() {
                Response response = null ;
                try {
                    response = call.execute();
                    if (response.isSuccessful()) {
                        Response = response.body().string();
                        System.out.println(Response);
                    }else {
                        throw new IOException("Unexpected code " + response);
                    }
                } catch (java.io.IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }
}
