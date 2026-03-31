package com.xinguanichuan.password;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.os.Bundle;
import android.view.View;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Toast;

public class MainActivity extends Activity {

    private WebView webView;

    @SuppressLint({"SetJavaScriptEnabled", "AddJavascriptInterface"})
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 全屏沉浸式
        getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_LAYOUT_STABLE |
            View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
        );

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);
        settings.setAllowFileAccess(true);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);

        // 注入 Android 原生接口
        webView.addJavascriptInterface(new AndroidBridge(this), "AndroidBridge");

        // 加载 assets 中的 HTML
        webView.loadUrl("file:///android_asset/index.html");
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    // Android 原生接口类
    public static class AndroidBridge {
        private final Context context;

        AndroidBridge(Context context) {
            this.context = context;
        }

        @JavascriptInterface
        public void copyToClipboard(String text) {
            ClipboardManager clipboard = (ClipboardManager)
                context.getSystemService(Context.CLIPBOARD_SERVICE);
            if (clipboard != null) {
                ClipData clip = ClipData.newPlainText("password", text);
                clipboard.setPrimaryClip(clip);
                // 在主线程显示 Toast
                android.os.Handler handler = new android.os.Handler(
                    android.os.Looper.getMainLooper());
                handler.post(() ->
                    Toast.makeText(context, "已复制到剪贴板", Toast.LENGTH_SHORT).show()
                );
            }
        }
    }
}
