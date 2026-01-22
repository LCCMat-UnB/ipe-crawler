package com.epicodus.solitaireboggle;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Random;

public class MainActivity extends AppCompatActivity {
    public static final String TAG = MainActivity.class.getSimpleName();
    private Button mGenerateBoggleLettersButton;
    private Button mCheckWord;
    private TextView mShowLetters;
    private EditText mUserInput;

    public final int maxLetterLength = 7;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mGenerateBoggleLettersButton = (Button) findViewById(R.id.playBoggle);
        mShowLetters = (TextView) findViewById(R.id.showLetters);

        mCheckWord = (Button) findViewById(R.id.checkWord);
        mUserInput = (EditText) findViewById(R.id.userInput);

        mGenerateBoggleLettersButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View view) {
                String setOfCharacters = "abcdefghijklmnopqrstuvwxyz";
                String boggleLetters = "";
                int countVowels = 0;

                do {
                    boggleLetters = "";
                    for (int i = 0; i <= maxLetterLength; i++) {
                        boggleLetters += setOfCharacters.charAt(new Random().nextInt(setOfCharacters.length()-1));
                    }

                    countVowels = 0;
                    for (int i =0; i <= boggleLetters.length() - 1; i++) {
                        char checkEachLetter = boggleLetters.charAt(i);
                        if (checkEachLetter == 'a' || checkEachLetter == 'e' || checkEachLetter == 'i' || checkEachLetter == 'o' || checkEachLetter == 'u') {
                            countVowels++;
                        }
                    }
                } while (countVowels < 2);

                mShowLetters.setText(boggleLetters);
            }
        });

        mCheckWord.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String inputWord = mUserInput.getText().toString();
                Log.d(TAG, inputWord);
                String generatedLetters = mShowLetters.getText().toString();
                Log.d(TAG, generatedLetters);

                Boolean matchWord = false;

                if (inputWord.length() < 3) {
                    Toast.makeText(MainActivity.this, "Need to use at least 3 letters", Toast.LENGTH_LONG).show();
                    mUserInput.setText("");
                } else {


                    int i = 0;


                    do {
                        if (generatedLetters.indexOf(inputWord.charAt(i)) != -1) {
                            matchWord = true;
                        } else {
                            matchWord = false;
                        }
                        i++;
                    } while (!(matchWord == false) && i < inputWord.length()-1);
                    //if not false && haven't gotten to end of word, keep looping




                    if (matchWord == false) {
                        Toast.makeText(MainActivity.this, "You can only use Boggle Letters.", Toast.LENGTH_LONG).show();
                    } else {
                        Toast.makeText(MainActivity.this, "Congratulations! But your boggle word will be checked for validity.", Toast.LENGTH_LONG).show();
                    }
                    mUserInput.setText("");
                }
            }
        });
    }
}
