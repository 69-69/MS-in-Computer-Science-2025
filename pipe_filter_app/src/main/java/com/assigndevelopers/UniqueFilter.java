package com.assigndevelopers;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class UniqueFilter {
    // Remove Duplicate words by using a Set
    public Set<String> removeDuplicates(List<String> words) {
        return new HashSet<>(words);
    }
}
