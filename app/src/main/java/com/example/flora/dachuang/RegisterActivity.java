package com.example.flora.dachuang;

import android.content.Intent;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.util.Random;

public class RegisterActivity extends AppCompatActivity {

    private static final String VERIFY_CODES = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ";
    private String verifyCode;
    private EditText mEmailView;
    private EditText mPasswordView;
    private EditText mPasswordVerifyView;
    private EditText mVerificationView;
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
                int verifySize = 6;
                verifyCode = generateVerifyCode(verifySize, VERIFY_CODES);
                // TODO: pop up a notice that the code has been sent to the email address above
            }
        });

        Button mSubmit = (Button) findViewById(R.id.register_register_confirm);
        mSubmit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // TODO: Password && username validation
                boolean cancel = false;
                View focusView = null;

                mPasswordView = (EditText) findViewById(R.id.register_pwd);
                String password = mPasswordView.getText().toString();

                mPasswordVerifyView = (EditText) findViewById(R.id.register_pwd_verification);
                String password_verify = mPasswordVerifyView.getText().toString();

                mEmailView = (EditText) findViewById(R.id.register_user_email);
                String email = mEmailView.getText().toString();

                // Check for a valid password.
                if (!TextUtils.isEmpty(password) && !isPasswordValid(password, password_verify)
                        && !TextUtils.isEmpty(password_verify)) {
                    mPasswordView.setError(getString(R.string.error_invalid_password));
                    focusView = mPasswordView;
                    cancel = true;
                }

                // Check for a valid email address.
                if (TextUtils.isEmpty(email)) {
                    mEmailView.setError(getString(R.string.error_field_required));
                    focusView = mEmailView;
                    cancel = true;
                } else if (!isEmailValid(email)) {
                    mEmailView.setError(getString(R.string.error_invalid_email));
                    focusView = mEmailView;
                    cancel = true;
                }

                // TODO: confirm the code entered, if correct, complete register and finish, if not, give warnings
                mVerificationView = (EditText) findViewById(R.id.register_verification_code);
                String verification_code_entered = mVerificationView.getText().toString();
                if (verification_code_entered.equals(verifyCode)) {
                    // TODO: get the registration job done (save in db session) & give notice to the user
                }

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

    /**
     * 使用指定源生成验证码
     * https://www.sojson.com/blog/70.html
     *
     * @param verifySize
     * @param sources
     * @return
     */
    private String generateVerifyCode(int verifySize, String sources) {
        if (sources == null || sources.length() == 0) {
            sources = VERIFY_CODES;
        }
        int codesLen = sources.length();
        Random rand = new Random(System.currentTimeMillis());
        StringBuilder verifyCode = new StringBuilder(verifySize);
        for (int i = 0; i < verifySize; i++) {
            verifyCode.append(sources.charAt(rand.nextInt(codesLen-1)));
        }
        return verifyCode.toString();
    }

    private boolean isEmailValid(String email) {
        //TODO: Replace this with your own logic
        // NOTE: if we don't use the verification code,
        // we can send a verification email to email address here, instead of above.
        return email.contains("@");
    }

    /**
     * 注册密码验证
     * @param password
     * @param password_verify
     * @return
     */
    private boolean isPasswordValid(String password, String password_verify) {
        //TODO: Replace this with your own logic
        return password.length() > 4 && password.equals(password_verify);
    }

}
