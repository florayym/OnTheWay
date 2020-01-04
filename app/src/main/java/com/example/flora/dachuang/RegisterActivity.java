package com.example.flora.dachuang;

import android.content.Intent;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;

public class RegisterActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        // Set action bar
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        Button mSendVerification = (Button) findViewById(R.id.register_get_verification_code);
        mSendVerification.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO: generate a verification code and sent it via email to the user
            }
        });

        Button mSubmit = (Button) findViewById(R.id.register_register_confirm);
        mSubmit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO: confirm the code entered, if correct, complete register and finish, if not, give warnings
            }
        });

    }
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            // Respond to the action bar's Up/Home button
            case android.R.id.home:
                //NavUtils.navigateUpFromSameTask(this);
                finish();
                // Change slide direction
                overridePendingTransition(R.anim.slide_in_left, R.anim.slide_out_right);
                return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
