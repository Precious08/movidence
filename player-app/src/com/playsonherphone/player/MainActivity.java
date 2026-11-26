package com.playsonherphone.player;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.MediaController;
import android.widget.TextView;
import android.widget.VideoView;

public class MainActivity extends Activity {
    private EditText urlField;
    private VideoView videoView;
    private TextView statusView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);

        urlField = new EditText(this);
        urlField.setHint("Paste the video URL");
        urlField.setContentDescription("Video URL field");
        urlField.setSingleLine(true);
        root.addView(urlField, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT));

        Button playButton = new Button(this);
        playButton.setText("Play");
        playButton.setContentDescription("Play button");
        root.addView(playButton, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT));

        statusView = new TextView(this);
        statusView.setText("Ready");
        statusView.setContentDescription("Status");
        root.addView(statusView, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT));

        videoView = new VideoView(this);
        videoView.setContentDescription("Video player");
        MediaController mc = new MediaController(this);
        mc.setAnchorView(videoView);
        videoView.setMediaController(mc);
        root.addView(videoView, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, 0, 1.0f));

        setContentView(root);

        videoView.setOnErrorListener((mp, what, extra) -> {
            statusView.setText("Could not play this file");
            return true;
        });
        videoView.setOnPreparedListener(mp -> statusView.setText("Playing"));

        playButton.setOnClickListener(v -> playFromField());

        Intent intent = getIntent();
        if (intent != null && intent.getData() != null) {
            urlField.setText(intent.getData().toString());
            playFromField();
        }
    }

    private void playFromField() {
        String url = urlField.getText().toString().trim();
        if (url.isEmpty()) {
            statusView.setText("No URL yet");
            return;
        }
        statusView.setText("Loading");
        videoView.setVideoURI(Uri.parse(url));
        videoView.requestFocus();
        videoView.start();
    }
}
