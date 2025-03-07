package com.assigndevelopers;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Set;

public class SortFilter {
    // Sorts the Words in Alphabetical Order
    public List<String> sortWords(Set<String> words) {
        List<String> sortedWords = new ArrayList<>(words);
        Collections.sort(sortedWords);
        return sortedWords;
    }
}
