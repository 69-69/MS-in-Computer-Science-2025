package com.assigndevelopers;

import java.util.ArrayList;
import java.util.List;

public class WordFilter {
    // Split text into words and returns them as a List
    public List<String> splitWords(String text) {
        List<String> words = new ArrayList<>();
        String[] wordArray = text.split("\\W+");

        for (String word : wordArray) {
            if (!word.isEmpty()) {
                words.add(word.toLowerCase());
            }
        }
        return words;
    }
}
