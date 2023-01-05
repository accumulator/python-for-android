package org.kivy.android;

import android.os.SystemClock;

import java.io.InputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.ArrayList;


import android.view.ViewGroup;
import android.view.KeyEvent;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.util.Log;
import android.widget.Toast;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.PowerManager;
import android.content.Context;
import android.content.pm.PackageManager;
import android.widget.ImageView;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;

import android.widget.AbsoluteLayout;
import android.view.ViewGroup.LayoutParams;

import android.net.Uri;

import org.renpy.android.ResourceManager;

import org.kivy.android.launcher.Project;


import org.qtproject.qt5.android.bindings.QtActivity;

// Required by PythonService class
public class PythonActivity extends QtActivity {
    private static final String TAG = "PythonActivity";

    private ResourceManager resourceManager = null;
    public static PythonActivity mActivity = null;
    public static boolean mBrokenLibraries;
    protected static ViewGroup mLayout;

    public static native void nativeSetenv(String name, String value);

    static {
        // load bootstrap JNI/Python early.
        System.loadLibrary("main");
    }

    public String getAppRoot() {
        return getFilesDir().getAbsolutePath() + "/app";
    }

    public String getEntryPoint(String search_dir) {
        /* Get the main file (.pyc|.pyo|.py) depending on if we
         * have a compiled version or not.
        */
        List<String> entryPoints = new ArrayList<String>();
        entryPoints.add("main.pyo");  // python 2 compiled files
        entryPoints.add("main.pyc");  // python 3 compiled files
        for (String value : entryPoints) {
            File mainFile = new File(search_dir + "/" + value);
            if (mainFile.exists()) {
                return value;
            }
        }
        return "main.py";
    }

    public static void initialize() {
        // The static nature of the singleton and Android quirkyness force us to initialize everything here
        // Otherwise, when exiting the app and returning to it, these variables *keep* their pre exit values
        mLayout = null;
        mBrokenLibraries = false;
    }


    @Override
    public void onCreate(Bundle savedInstanceState) {
        Log.v(TAG, "My onCreate running");
        resourceManager = new ResourceManager(this);

        this.mActivity = this;
//         this.showLoadingScreen();

        super.onCreate(savedInstanceState);
    }

    //----------------------------------------------------------------------------
    // Listener interface for onNewIntent
    //

    public interface NewIntentListener {
        void onNewIntent(Intent intent);
    }

    private List<NewIntentListener> newIntentListeners = null;

    public void registerNewIntentListener(NewIntentListener listener) {
        if ( this.newIntentListeners == null )
            this.newIntentListeners = Collections.synchronizedList(new ArrayList<NewIntentListener>());
        this.newIntentListeners.add(listener);
    }

    public void unregisterNewIntentListener(NewIntentListener listener) {
        if ( this.newIntentListeners == null )
            return;
        this.newIntentListeners.remove(listener);
    }

    @Override
    protected void onNewIntent(Intent intent) {
        if ( this.newIntentListeners == null )
            return;
        this.onResume();
        synchronized ( this.newIntentListeners ) {
            Iterator<NewIntentListener> iterator = this.newIntentListeners.iterator();
            while ( iterator.hasNext() ) {
                (iterator.next()).onNewIntent(intent);
            }
        }
    }

}
